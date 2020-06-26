# # ONS Counts and ratios of coronavirus-related deaths by ethnic group, England and Wales 

from gssutils import * 
import json 
from datetime import datetime

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage)  
scraper

distribution = scraper.distributions[0]

# +
datasetTitle = 'ONS Counts and ratios of coronavirus-related deaths by ethnic group, England and Wales'
tabs = { tab: tab for tab in distribution.as_databaker() }
tidied_sheets = []
trace = TransformTrace()
df = pd.DataFrame()

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]

def date_time(time_value):
    date_string = time_value.strip().split(':')[2]
    date_range = date_string[:-7]
    return date_range

def start_date(time_value):
    date_string = time_value.strip().split('to')[0]
    day = date_string.strip().split(' ')[0]
    month = date_string.strip().split(' ')[1]
    year = date_string.strip().split(' ')[2]
    start_date_string = day + '-' + month + '-' + year
    formated_date = datetime.strptime(start_date_string, '%d-%B-%Y')
    return formated_date.strftime('%Y-%m-%d')

def end_date(time_value):
    date_string = time_value.strip().split('to')[1]
    day = date_string.strip().split(' ')[0]
    month = date_string.strip().split(' ')[1]
    year = date_string.strip().split(' ')[2]
    end_date_string = day + '-' + month + '-' + year
    formated_date = datetime.strptime(end_date_string, '%d-%B-%Y')
    return formated_date.strftime('%Y-%m-%d')

def date_duration (start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return abs((end_date - start_date).days)


# -

for tab in tabs:
   
    if not tab.name.lower() in ['contents', 'definitions']:#TABS TO IGNORE
        
        datacube_name = "ONS Counts and ratios of coronavirus-related deaths by ethnic group, England and Wales"
        columns=["Period", "Ethnicity","Sex","Ageband", "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
       
        ethnicity = tab.filter(contains_string('Ethnicity')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Ethnicity('Ethnicity Range detailed at cell value: {}', var = cellLoc(ethnicity))
        
        sex = tab.filter(contains_string('Sex')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))
        
        age_band = tab.filter(contains_string('Ageband')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Ageband('Ageband at cell value: {}', var = cellLoc(age_band))
        
        observations = age_band.fill(RIGHT).is_not_blank()
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: People')
        
        #Define measure type 
        if right(tab.name.lstrip().rstrip().lower(), 1) in ['1']:
            period_druation_in_tab = tab.filter(contains_string('Table 1')).is_not_blank()
            trace.Period('Period Duration at cell value: {}', var = cellLoc(period_druation_in_tab))
            measure_type = 'Count'
            trace.Measure_Type('Hardcoded value as: Count for ' + tab.name)
        elif right(tab.name.lstrip().rstrip().lower(), 1) in ['2']:
            period_druation_in_tab = tab.filter(contains_string('Table 2')).is_not_blank()
            trace.Period('Period Duration at cell value: {}', var = cellLoc(period_druation_in_tab))
            measure_type = 'Ratio'
            trace.Measure_Type('Hardcoded value as: Ratio' + tab.name)
 
        dimensions = [
            HDim(period_druation_in_tab, 'Period', CLOSEST, LEFT),
            HDim(ethnicity, 'Ethnicity', DIRECTLY, LEFT),
            HDim(sex, 'Sex', DIRECTLY, LEFT),
            HDim(age_band, 'Age band', DIRECTLY, LEFT),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())  
    else:
        continue

df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS': 'Value'}, inplace=True)
df["Period"] = df["Period"].apply(date_time)
df['Start Date'] = df["Period"].apply(start_date)
df['End Date'] = df["Period"].apply(end_date)
intervalOfOrderPeriods = date_duration(df['Start Date'].iloc[0], df['End Date'].iloc[0])
df["Period"] = 'gregorian-interval/' + df['Start Date'] + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D'
temporal_date = df['Period'].iloc[1]
df.drop(['Start Date', 'End Date'], axis=1, inplace=True)

df = df[['Ethnicity', 'Sex', 'Age band', 'Value', 'Measure Type', 'Unit']]

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)

for column in df:
    if column in ("Ethnicity","Sex"):
        df[column] = df[column].map(lambda x: pathify(x))

notes = """
1 Causes of death was defined using the International Classification of Diseases, Tenth Revision (ICD-10) codes U07.1 and U07.2. Figures include deaths where coronavirus (COVID-19) was the underlying cause or was mentioned on the death certificate as a contributory factor. Figures do not include neonatal deaths (deaths under 28 days).
2 Figures are for persons usually resident in England and Wales, based on 2011 Census enumerations, and not known to have died before 2 March 2020.
3 Figures are for deaths occurring between 2 March 2020 and 10 April 2020. Figures only include deaths that were registered by 17 April 2020. More information on registration delays can be found on the ONS website: 
https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/2018
4 Ratios measure the contribution of covid-19 deaths and is calculated by dividing Covid-19 deaths by non Covid-19 deaths that occurred in the analysis period 2 March to 10 April 2020 among the linked study population. 
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
scraper.dataset.comment = notes
scraper.dataset.temporal = "http://reference.data.gov.uk/id/" + temporal_date
import os
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()
df
# -


