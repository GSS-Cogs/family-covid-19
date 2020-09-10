# +
# Temp scraper here.
# TODO - move it into gss-utils

from gssutils import *
from gssutils.metadata.dcat import Distribution
from gssutils.metadata.mimetype import CSV
from dateutil.parser import parse
from lxml import html 
import json
import pandas as pd

trace = TransformTrace()
comments = {} # per tab, capture some nuances

# TODO - when we're happy this works, move it into gss-utils!
def opendata_nhs(scraper, tree):

    # TODO - this feels more like a catalogue than a list of distributions, investigate
    
    # Populate the dataset
    details = tree.xpath('//tr/td[@class="dataset-details"]')
    
    dates = tree.xpath('//span[@class="automatic-local-datetime"]/text()')
    date_updated = parse(" ".join([x.replace("\n", "").replace("(BST)", "").strip() for x in dates[0].split(" ")]))
    date_created = parse(" ".join([x.replace("\n", "").replace("(BST)", "").strip() for x in dates[1].split(" ")]))
    
    # Populate distributions
    distro_resources = tree.xpath('//li[@class="resource-item"]')
    for dr in distro_resources:
        
        download = dr.xpath('div/ul/li/a[contains(@class, "resource-url-analytics")]/@href')[0]
            
        # Need to go to the preview page for full description and title as they've helpfully truncated both...
        preview_url = "https://www.opendata.nhs.scot" + dr.xpath('div/ul[@class="dropdown-menu"]/li/a/@href')[0]
        r = scraper.session.get(preview_url)
        if r.status_code != 200:
            raise Exception("Unable to follow url to get full description, url: '{}', status code '{}'.".format(preview_url, r.status_code))
            
        preview_tree = html.fromstring(r.text)
        description1 = preview_tree.xpath('//div[contains(@class, "prose notes")]/p/text()')[0]
        # Some (but not all) descriptions have some additional itallic information
        try:
            description2 = preview_tree.xpath('//div[contains(@class, "prose notes")]/p/em/text()')[0]
        except IndexError:
            description2 = ""
        
        description = description1 + "\n\n" + description2
        description.strip("\n")
        
        title = preview_tree.xpath('//title/text()')[0]
        this_distribution = Distribution(scraper)

        this_distribution.issued = date_updated
        this_distribution.downloadURL = download
        this_distribution.mediaType = CSV

        this_distribution.title = title.strip()
        this_distribution.description = description

        scraper.distributions.append(this_distribution)



# -


# # Statistical Qualifiers
#
# The data makes use of "statistical qualifiers" (data markers to us). Rather than hard code them we're going to pull hte table in each tranform (in case something changes).

# +

# note - got download link from page: https://www.opendata.nhs.scot/dataset/statistical-qualifiers/resource/b80f9af0-b115-4245-b591-fb22775226c4
stat_qualifier_df = pd.read_csv("https://www.opendata.nhs.scot/dataset/2b6f00ec-fee3-4828-9303-89f31b436d2a/resource/b80f9af0-b115-4245-b591-fb22775226c4/download/statisticalqualifiers24052019.csv", encoding = "ISO-8859-1")
stat_qualifier_df

# +
pathified_qualifiers = dict(zip(stat_qualifier_df["Qualifier"], stat_qualifier_df["QualifierName"].apply(pathify)))

from pprint import pprint
pprint(pathified_qualifiers)

def get_pathified_qualifier(marker):
    """
    For a given data marker/qualifier, get the pathified version of its qualifier name
    """
    if marker != "":
        try:
            marker = pathified_qualifiers[marker]
        except Exception as e:
            raise Exception("Unable to find qualifier for data marker {} in {}" \
                            .format(marker, json.dumps(pathified_qualifiers, indent=2))) from e
    return marker


# -

# ## Helpers & Handlers

# +

# Unsure how to describe this in the tracer at time of writing so using a variable (so I don't have to change it in twenty places when I decide)
WEEKLY_HANDLING_DESC = "No date provided against observations. Set as the issued date"

def get_weekly_date(issued):
    """
    Where no observation level date has been inlcuded, use the issued date of the data to get
    the week in question
    """
    
    # TODO - pull it out, not a lot of point in parsing the same date for every tab
    issued = "week/" + issued.strftime("%Y-%U")
    
    return issued
    
def format_daily_dates(date):
    """
    Where the data has a specific daily datelisted (in the form '20201201', i.e the 1st December 2020)
    convert to appropriately formatted period.
    """
    # Confirm the input is what we think it is
    try:
        int(date) # Cast it, make sure it fits as an int
        date = str(date) 
    except Exception as e:
        raise Exception("Aborting, expected the provided date '{}' to be an integer sequence of 8 digits".format(date_string)) from e
        
    # 20200729
    year = date[:4]
    month = date[4:-2]
    day = date[-2:]
    
    # day/{year}-{month}-{day}
    return "day/{}-{}-{}".format(year, month, day)

def handler_cumulative_cases_by_age_and_sex(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset titles 'Cumulative Cases By Age and Sex'
    """
    
    trace.Measure_Type("Move Rate and Total cases to Value column, differentiate them via Measure Type as: {}", var=["Rate", "Count"])
    trace.Unit_of_Measure("Set to Cases")
    rate_df = df#.drop("TotalCases", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    rate_df["Unit Of Measure"] = "Cases"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df["RateQF"] = ""
    total_case_df = total_case_df.rename(columns={"TotalCases": "Value"})
    total_case_df["Measure Type"] = "Count"
    total_case_df["Unit Of Measure"] = "Cases"
    
    df = pd.concat([rate_df, total_case_df])
    
    trace.add_column("Marker")
    trace.Marker("Renamed RateQF to Marker")
    df = df.rename(columns={"RateQF": "Marker"})
    
    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df, trace, comments_for_cube
    

def handler_daily_and_cumulative_cases(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily and Cumulative Cases - Scottish Health and Social Care Open Data
    """
    
    trace.add_column("Case Type")
    trace.Case_Type("Added a 'Case Type' dimension so we can differentiate between a daily count of" \
                   + "cases and a cumulative count of cases")
    daily_df = df.drop("CumulativeCases", axis=1)
    daily_df["Case Type"] = "Daily"
    daily_df = daily_df.rename(columns={"DailyCases": "Value"})
        
    cumulative_df = df.drop("DailyCases", axis=1)
    cumulative_df["Case Type"] = "Cumulative"
    cumulative_df = cumulative_df.rename(columns={"CumulativeCases": "Value"})

    df = pd.concat([daily_df, cumulative_df])

    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Cases")
    df["Unit of Measure"] = "Cases"
    
    return df, trace, comments_for_cube


def handler_cumulative_cases_by_deprivation(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases by Deprivation - Scottish Health and Social Care Open Data
    """
    
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Cases")
    df["Unit of Measure"] = "Cases"
    
    return df, trace, comments_for_cube


def handler_daily_covid19_hospital_admissions(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data
    """

    trace.Measure_Type("Move NumberAdmitted and SevenDayAverage cases to Value column, differentiate them via Measure Type as: {}", var=["SevenDayAverage", "Count"])
    trace.Unit_of_Measure("Set to Admissions")
    
    seven_day_df = df.drop("NumberAdmitted", axis=1)
    seven_day_df = seven_day_df.rename(columns={"SevenDayAverage": "Value"})
    seven_day_df["Measure Type"] = "SevenDayAverage"
    seven_day_df["Unit of Measure"] = "Admissions"
    
    num_df = df.drop("SevenDayAverage", axis=1)
    num_df = num_df.rename(columns={"NumberAdmitted": "Value"})
    num_df["Measure Type"] = "Count"
    num_df["Unit of Measure"] = "Admissions"

    df = pd.concat([seven_day_df, num_df])
    
    return df, trace, comments_for_cube


def handler_cumulative_covid19_hospital_admissions_by_age_sex(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data
    """
    
    trace.Measure_Type("Move NumberAdmitted and Rate cases to Value column, differentiate them via Measure Type as: {}", var=["SevenDayAverage", "Rate"])
    trace.Unit_of_Measure("Cases")
    
    rate_df = df.drop("NumberAdmitted", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    rate_df["Unit Of Measure"] = "Cases"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df = total_case_df.rename(columns={"NumberAdmitted": "Value"})
    total_case_df["Measure Type"] = "Count"
    total_case_df["Unit Of Measure"] = "Cases"
    
    df = pd.concat([rate_df, total_case_df])
    trace.add_column("Marker")
    trace.Marker("Renamed RateQF to Marker, as it not only applies to Rate observations (i.e contents of Value)")
    df.rename(columns={"RateQF":"Marker"})
    
    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df, trace, comments_for_cube


def handler_cumulative_covid19_hospital_admissions_by_deprivation(df, trace, comments_for_cube):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Deprivation - Scottish Health and Social Care Open Data
    """
    
    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Cases")
    df["Unit of Measure"] = "Cases"
    
    return df, trace, comments_for_cube


def handler_daily_icu_admissions_for_new_covid19_patients(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily ICU Admissions for new COVID-19 Patients - Scottish Health and Social Care Open Data
    """
    
    trace.Measure_Type("Move NumberAdmitted and SevenDayAverage admissions to Value column, differentiate them via Measure Type as: {}", var=["SevenDayAverage", "Count"])
    trace.Unit_of_Measure("Admissions")
    
    seven_day_df = df.drop("NumberAdmitted", axis=1)
    seven_day_df = seven_day_df.rename(columns={"SevenDayAverage": "Value"})
    seven_day_df["Measure Type"] = "SevenDayAverage"
    seven_day_df["Unit of Measure"] = "Admissions"
    
    num_df = df.drop("SevenDayAverage", axis=1)
    num_df = num_df.rename(columns={"NumberAdmitted": "Value"})
    num_df["Measure Type"] = "Count"
    num_df["Unit of Measure"] = "Admissions"
    
    df = pd.concat([seven_day_df, num_df]) 
    
    return df, trace, comments_for_cube


def handler_cumulative_admissions_to_icu(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Admissions to ICU - Scottish Health and Social Care Open Data
    """
    
    trace.Measure_Type("Move NumberAdmitted and Rate Admitted admissions to Value column, differentiate them via Measure Type as: {}", var=["Rate", "Count"])
    trace.Unit_of_Measure("Admissions")
    
    # Pivot multiple obs columns
    rate_df = df.drop("NumberAdmitted", axis=1)
    rate_df = rate_df.rename(columns={"RateAdmitted": "Value"})
    rate_df["Measure Type"] = "Rate"
    rate_df["Unit of Measure"] = "Admissions"
    
    total_case_df = df.drop("RateAdmitted", axis=1)
    total_case_df = total_case_df.rename(columns={"NumberAdmitted": "Value"})
    total_case_df["Measure Type"] = "Count"
    total_case_df["Unit of Measure"] = "Admissions"
    
    df = pd.concat([rate_df, total_case_df])
    
    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df, trace, comments_for_cube


def handler_daily_nhs24_covid19_calls(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily NHS24 COVID-19 Calls - Scottish Health and Social Care Open Data
    """
    
    trace.add_column("NHS24CovidCalls")
    trace.NHS24CovidCalls("Renamed to Value")
    
    df = df.rename(columns={"NHS24CovidCalls": "Value"})
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Phone Calls")
    df["Unit of Measure"] = "Phone Calls"
    
    return df, trace, comments_for_cube


def handler_daily_consultations_by_contact_type(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily Consultations by Contact Type - Scottish Health and Social Care Open Data
    """
    
    trace.add_column("NumberOfConsultations")
    trace.NumberOfConsultations("Renamed to Value")
    
    df = df.rename(columns={"NumberOfConsultations": "Value"})
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Consulations")
    df["Unit of Measure"] = "Consultations"
    
    return df, trace, comments_for_cube


def handler_daily_sas_incidents(df, trace, comments_for_cube):
    """  
    Weekly COVID-19 Statistical Data in Scotland - Daily SAS Incidents - Scottish Health and Social Care Open Data
    """

    column_details = [
        "AllSASIncidents",
        "COVIDAll",
        "COVIDAttended",
        "COVIDConveyed"
    ]
    
    slices = []
    
    trace.add_column("Incident Type")
    trace.Incident_Type("Created an 'Incident Type' column and pivotted the following column into it: '{}'.".format(column_details))
    
    for col in column_details:
        temp_df = df.copy()
        cols_to_drop = [x for x in column_details if x != col]
        temp_df = temp_df.drop(cols_to_drop, axis=1)
        temp_df = temp_df.rename(columns={col: "Value"})
        temp_df["Incident Type"] = col
        slices.append(temp_df.copy())
        
    df = pd.concat(slices)
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Incidents")
    df["Unit of Measure"] = "Incidents"
    
    return df, trace, comments_for_cube

def handler_cumulative_suspected_covid19_sas_incidents_by_age(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Age - Scottish Health and Social Care Open Data
    """

    trace.Measure_Type("Move Incidents and Rate to Value column, differentiate them via Measure Type as: {}", var=["Rate", "Count"])
    trace.Unit_of_Measure("Incidents")
    
    # Pivot multiple obs columns
    rate_df = df.drop("Incidents", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    rate_df["Unit of Measure"] = "Incidents"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df = total_case_df.rename(columns={"Incidents": "Value"})
    total_case_df["Measure Type"] = "Count"
    total_case_df["Unit of Measure"] = "Incidents"
    total_case_df["RateQF"] = ""   # dont apply rate markers to incidents
    
    df = pd.concat([rate_df, total_case_df])
    
    trace.add_column("Marker")
    trace.Marker("Renamed RateQF to Marker, as it not only applies to Rate observations (i.e contents of Value)")
    df = df.rename(columns={"RateQF": "Marker"})
    
    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df, trace, comments_for_cube


def handler_cumulative_suspected_covid19_sas_incidents_by_deprivation(df, trace, comments_for_cube):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Deprivation - Scottish Health and Social Care Open Data
    """

    # Set a period, then format appropriately
    trace.Period(WEEKLY_HANDLING_DESC)
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    trace.Measure_Type("Set to Count")
    df["Measure Type"] = "Count"
    
    trace.Unit_of_Measure("Set to Incidents")
    df["Unit of Measure"] = "Incidents"
    
    trace.ALL("Renamed Incidents column to Value")
    df = df.rename(columns={"Incidents": "Value"})
    
    return df, trace, comments_for_cube



# +
from gssutils import *

scrapers.scraper_list = [('https://www.opendata.nhs.scot', opendata_nhs)]
scraper = Scraper(seed="info.json")
scraper
# +
all_dat = []
# A certain amount of nonsense to focus the scraper on each distribution in turn
for distro_title in [x.title for x in scraper.distributions]:
    
    distro = scraper.distribution(title=distro_title)
    df = distro.as_pandas().fillna("")
    
    # Shorter output title
    otitle = distro_title.replace("Weekly COVID-19 Statistical Data in Scotland - ", "")
    otitle = otitle.replace(" - Scottish Health and Social Care Open Data", "")
    otitle = otitle.strip()
    
    # Columns vary so for the trace we'll start with the minimum columns and apply as needed
    columns = ["Period", "Value", "Measure Type", "Unit of Measure"] + [x for x in df.columns.values.tolist() if x.endswith("QF")]
    trace.start(otitle, distro_title, columns, distro.downloadURL)
    
    # Everything needs the same date handling
    for col in df.columns.values.tolist():
        if col == "Date":
            df[col] = df[col].apply(format_daily_dates)
            df.rename({"Date": "Period"})
            trace.Period("Converted Period to /day format.")
            
    # Everything needs the same qualifier handling
    for col in df.columns.values.tolist():
        if col.strip().endswith("QF"):
            df[col] = df[col].apply(get_pathified_qualifier)
            trace.multi([col], "Applied pathified qualifiers lookup (i.e data markers).")
    
    # Define handlers
    handlers = { 'Weekly COVID-19 Statistical Data in Scotland - Cumulative Admissions to ICU - Scottish Health and Social Care Open Data': handler_cumulative_admissions_to_icu,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Age, Sex - Scottish Health and Social Care Open Data': handler_cumulative_covid19_hospital_admissions_by_age_sex,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Deprivation - Scottish Health and Social Care Open Data': handler_cumulative_covid19_hospital_admissions_by_deprivation,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases By Age and Sex - Scottish Health and Social Care Open Data': handler_cumulative_cases_by_age_and_sex,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases by Deprivation - Scottish Health and Social Care Open Data': handler_cumulative_cases_by_deprivation,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Age - Scottish Health and Social Care Open Data': handler_cumulative_suspected_covid19_sas_incidents_by_age,
                 'Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Deprivation - Scottish Health and Social Care Open Data': handler_cumulative_suspected_covid19_sas_incidents_by_deprivation,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data': handler_daily_covid19_hospital_admissions,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily Consultations by Contact Type - Scottish Health and Social Care Open Data': handler_daily_consultations_by_contact_type,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily ICU Admissions for new COVID-19 Patients - Scottish Health and Social Care Open Data': handler_daily_icu_admissions_for_new_covid19_patients,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily NHS24 COVID-19 Calls - Scottish Health and Social Care Open Data': handler_daily_nhs24_covid19_calls,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily SAS Incidents - Scottish Health and Social Care Open Data': handler_daily_sas_incidents,
                 'Weekly COVID-19 Statistical Data in Scotland - Daily and Cumulative Cases - Scottish Health and Social Care Open Data': handler_daily_and_cumulative_cases
               }
    
    if distro.title.strip() not in handlers.keys():
        raise Exception("The distribution '{}' is new or something has been renamed - cannot identify a handler for it.".format(distro.title.strip()))

    #out = Path('out')
    #out.mkdir(exist_ok=True)
    
    # ----- IMPORTANT -----
    # uncomment the below to ouput the before as well as the after (these ones are confusing, it helps a lot)
    #df.to_csv(out / "{}_OLD.csv".format(pathify(otitle.strip())), index=False)
    
    # Capture any comments for the spec
    comments[distro_title] = []
    
    # Handle
    df, trace, _ = handlers[distro.title](df, trace, comments[distro_title])
    all_dat.append(df)
    # Output
    #df.to_csv(out / "{}.csv".format(pathify(otitle.strip())), index=False)
    
#trace.output()

# -
spec_me = False
if spec_me:
    # use the tracer to write some simple markdown for spec (because I'm lazy)
    lines = ["----------### Stage 1. Transform", ""]
    for title, details in trace._create_output_dict().items():
        for cube_title, cubes in details.items():   # ['sourced_from', 'id', 'tab', 'column_actions']
            lines.append("#### " + cube_title)
            lines.append("") 
            for cube in cubes:
                lines.append("#### Sheet: " + cube["tab"])
                lines.append("")
                for column in cube["column_actions"]:
                    lines.append("{}".format(column["column_label"]))
                    for comment in [",".join(list(x.values())) for x in column["actions"]]:
                        lines.append("- "+comment)
                    lines.append("")
                lines.append("#### Table structure")
                lines.append(", ".join([x["column_label"] for x in cube["column_actions"]]))
                if cube["tab"] in comments:
                    lines.append("")
                    if len(comments[cube["tab"]]) > 0:
                        lines.append("#### DE notes")
                        for comment in comments[cube["tab"]]:
                            lines.append(comment)
                lines.append("")
            lines.append("-----")

    for l in lines:
        print(l)

all_dat[0] = all_dat[0][['Date','Country','Case Type','Value']]

# +
#all_dat[0].head(60)

# +
#for c in all_dat[0].columns:
#    print(c)
#    print(all_dat[0][c].unique())
#    print("##############################################")

# +
import os
from urllib.parse import urljoin

out = Path('out')
out.mkdir(exist_ok=True)
all_dat[0].drop_duplicates().to_csv(out / 'observations.csv', index = False)
scraper.dataset.issued = ''
scraper.dataset.family = 'covid-19'
scraper.dataset.comment = 'Daily and cumulative number of confirmed positive cases of COVID-19 in Scotland'
dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scraper.dataset.family}/' + Path(os.getcwd()).name))
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / 'observations.csv')
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / 'observations.csv-metadata.json')
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -






