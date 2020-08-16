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


# TODO - when we're happy his works, move it into gss-utils!
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

def get_weekly_date(issued):
    """
    Where no observation level date has been inlcuded, use the issued date of the data to get
    the week in question
    """
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

def handler_cumulative_cases_by_age_and_sex(df):
    """
    Makes appropriate changes for the source dataset titles 'Cumulative Cases By Age and Sex'
    """
    rate_df = df.drop("TotalCases", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    rate_df["Unit Of Measure"] = "Cases"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df = total_case_df.rename(columns={"TotalCases": "Value"})
    total_case_df["Measure Type"] = "Count"
    total_case_df["Unit Of Measure"] = "Cases"
    
    df = pd.concat([rate_df, total_case_df])
    
    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df
    

def handler_daily_and_cumulative_cases(df):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily and Cumulative Cases - Scottish Health and Social Care Open Data
    """
    daily_df = df.drop("CumulativeCases", axis=1)
    daily_df["Case Type"] = "Daily"
    daily_df = daily_df.rename(columns={"DailyCases": "Value"})
        
    cumulative_df = df.drop("DailyCases", axis=1)
    cumulative_df["Case Type"] = "Cumulative"
    cumulative_df = cumulative_df.rename(columns={"CumulativeCases": "Value"})

    df = pd.concat([daily_df, cumulative_df])

    df["Measure Type"] = "Count"
    df["Unit Of Measure"] = "Cases"
    
    return df


def handler_cumulative_cases_by_deprivation(df):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases by Deprivation - Scottish Health and Social Care Open Data
    """
    
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    df["Measure Type"] = "Count"
    df["Unit Of Measure"] = "Cases"
    
    return df


def handler_daily_covid19_hospital_admissions(df):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data
    """
    df = df.rename(columns={"SaveDayAverage": "Value"})
    return df


def handler_cumulative_covid19_hospital_admissions_by_age_sex(df):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data
    """
    rate_df = df.drop("NumberAdmitted", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df = total_case_df.rename(columns={"NumberAdmitted": "Value"})
    total_case_df["Measure Type"] = "NumberAdmitted"
    
    df = pd.concat([rate_df, total_case_df])
    
    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df

def handler_cumulative_covid19_hospital_admissions_by_deprivation(df):
    """
    Makes appropriate changes for the source dataset:
    Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Deprivation - Scottish Health and Social Care Open Data
    """
    
    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df

def handler_daily_icu_admissions_for_new_covid19_patients(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily ICU Admissions for new COVID-19 Patients - Scottish Health and Social Care Open Data
    """
    
    rate_df = df.drop("NumberAdmitted", axis=1)
    rate_df = rate_df.rename(columns={"SevenDayAverage": "Value"})
    rate_df["Measure Type"] = "SevenDayAverage"
    
    total_case_df = df.drop("SevenDayAverage", axis=1)
    total_case_df = total_case_df.rename(columns={"NumberAdmitted": "Value"})
    total_case_df["Measure Type"] = "NumberAdmitted"
    
    df = pd.concat([rate_df, total_case_df])
    
    return df

def handler_cumulative_admissions_to_icu(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Admissions to ICU - Scottish Health and Social Care Open Data
    """
    
    # Pivot multiple obs columns
    rate_df = df.drop("NumberAdmitted", axis=1)
    rate_df = rate_df.rename(columns={"RateAdmitted": "Value"})
    rate_df["Measure Type"] = "RateAdmitted"
    
    total_case_df = df.drop("RateAdmitted", axis=1)
    total_case_df = total_case_df.rename(columns={"NumberAdmitted": "Value"})
    total_case_df["Measure Type"] = "NumberAdmitted"
    
    df = pd.concat([rate_df, total_case_df])
    
    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df

def handler_daily_nhs24_covid19_calls(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily NHS24 COVID-19 Calls - Scottish Health and Social Care Open Data
    """
    df = df.rename(columns={"NHS24CovidCalls": "Value"})
    return df


def handler_daily_consultations_by_contact_type(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Daily Consultations by Contact Type - Scottish Health and Social Care Open Data
    """
    df = df.rename({"NumberOfConsultation": "Value"})
    return df

def handler_daily_sas_incidents(df):
    """  
    Weekly COVID-19 Statistical Data in Scotland - Daily SAS Incidents - Scottish Health and Social Care Open Data
    """

    columns_to_pivot = ["AllSASIncidents", "COVIDAll", "COVIDAttended", "COVIDConveyed"]
    
    return df

def handler_cumulative_suspected_covid19_sas_incidents_by_age(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Age - Scottish Health and Social Care Open Data
    """
    
    # Pivot multiple obs columns
    rate_df = df.drop("Incidents", axis=1)
    rate_df = rate_df.rename(columns={"Rate": "Value"})
    rate_df["Measure Type"] = "Rate"
    
    total_case_df = df.drop("Rate", axis=1)
    total_case_df = total_case_df.rename(columns={"Incidents": "Value"})
    total_case_df["Measure Type"] = "Incidents"
    total_case_df["RateQF"] = ""   # dont apply rate markers to incidents
    
    df = pd.concat([rate_df, total_case_df])
    df = df.rename(columns={"RateQF": "Marker"})
    
    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df

def handler_cumulative_suspected_covid19_sas_incidents_by_deprivation(df):
    """
    Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Deprivation - Scottish Health and Social Care Open Data
    """

    # Set a period, then format appropriately
    df["Period"] = distro.issued
    df["Period"] = df["Period"].apply(get_weekly_date)
    
    return df



# +
from gssutils import *

scrapers.scraper_list = [('https://www.opendata.nhs.scot', opendata_nhs)]
scraper = Scraper(seed="info.json")
scraper
# +

# A certain amount of nonsense to focus the scraper on each distribution in turn
for distro_title in [x.title for x in scraper.distributions]:
    
    # Note: filter by desription as they're reusing the same title more than once for different data ...
    distro = scraper.distribution(title=distro_title)
    
    df = distro.as_pandas().fillna("")
    
    # Everything needs the same date handling
    for col in df.columns.values.tolist():
        if col == "Date":
            df[col] = df[col].apply(format_daily_dates)
            
    # Everything needs the same qualifier handling
    for col in df.columns.values.tolist():
        if col.strip().endswith("QF"):
            df[col] = df[col].apply(get_pathified_qualifier)
    
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
        import sys
        sys.exit(1)

    # Handle
    df = handlers[distro.title](df)
    
    # Shorter output title
    otitle = distro.title.replace("Weekly COVID-19 Statistical Data in Scotland - ", "")
    otitle = otitle.replace(" - Scottish Health and Social Care Open Data", "")
    otitle = otitle.strip()
    df.to_csv("./out/{}.csv".format(pathify(otitle.strip())), index=False)

    distro.as_pandas().fillna("").to_csv("./out/{}_OLD.csv".format(pathify(otitle.strip())), index=False)



# -




