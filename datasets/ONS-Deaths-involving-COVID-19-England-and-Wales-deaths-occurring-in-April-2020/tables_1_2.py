# # ONS Deaths involving COVID-19, England and Wales 

from gssutils import * 
import json 
from datetime import datetime

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper 

distribution = scraper.distributions[0]
distribution

# +
datasetTitle = 'Number of deaths by leading causes groupings and due to COVID-19, England and Wales'
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

month_look_up = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 
                  'July':'07','August':'08','September':'09', 'October':'10','November':'11', 'December':'12'}
def date_time(time_value):
    date_string = time_value.strip()
    if len(date_string)  == 2:
        return 'month/2020-' + date_string


# -

for tab in tabs:
    
    datacube_name = "Number of deaths by leading causes groupings and due to COVID-19, England and Wales"
    
    if tab.name.lower() == 'table 1':

        columns=["ICD 10 Codes", "Cause of death groups","Country","Period", 'Age Group', 'Sex', "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
        
        icd_10_codes = tab.filter(contains_string('ICD-10 codes')).shift(0,1).expand(DOWN).is_not_blank()
        trace.ICD_10_Codes('ICD-10 codes detailed at cell value: {}', var = cellLoc(icd_10_codes))
                   
        cause_of_death_groups = tab.filter(contains_string('Cause of death groups')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Cause_of_death_groups('Cause of death groups detailed at cell value: {}', var = cellLoc(cause_of_death_groups))
            
        country = tab.filter(contains_string('England and Wales')).expand(RIGHT).is_not_blank()
        trace.Country('Country detailed at cell value: {}', var = cellLoc(country))
            
        period_month = tab.filter(contains_string('Cause of death groups')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Period('Period detailed at cell value: {}', var = cellLoc(period_month))
            
        measure_type = 'Count'
        trace.Measure_Type('Hardcoded value as: Count')
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: Deaths')
        sex = 'All'
        trace.Sex('Hardcoded value as: All')
        age_group = 'All'
        trace.Age_Group('Hardcoded value as: All')
            
        observations = period_month.fill(DOWN).is_not_blank()
        dimensions = [
            HDim(period_month, 'Period', DIRECTLY, ABOVE),
            HDim(country, 'Country', CLOSEST, LEFT),
            HDim(cause_of_death_groups, 'Cause of death groups', DIRECTLY, LEFT),
            HDim(icd_10_codes, 'ICD 10 Codes', DIRECTLY, LEFT),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Sex', sex),
            HDimConst('Age Group', age_group),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
       # savepreviewhtml(tidy_sheet)
        trace.store("Deaths_involving_COVID19_England_Wales", tidy_sheet.topandas())  
    
    if tab.name.lower() == 'table 2':
        
        columns=["Age Group", "Sex","Country","Period", "ICD 10 Codes", "Cause of death groups" "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
    
        ref_cell = tab.filter(contains_string('All ages'))
        age_group = ref_cell.expand(DOWN).is_not_blank()
        trace.Age_Group('Age Group detailed at cell value: {}', var = cellLoc(age_group))
            
        sex_ref_cell = tab.filter(contains_string('Persons'))
        sex = sex_ref_cell.expand(RIGHT).is_not_blank()
        trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))
            
        measure_ref_cell = tab.filter(contains_string('Number of deaths'))
        measure_type = measure_ref_cell.expand(RIGHT).is_not_blank()
        #trace.Measure_Type('Measure Type detailed at cell value: {}', var = cellLoc(measure_type))
            
        period_month_ref_cell = tab.filter(contains_string('March'))
        period_month = period_month_ref_cell.expand(RIGHT).is_not_blank()
        trace.Period('Period detailed at cell value: {}', var = cellLoc(period_month))
        
        country_type = ['England and Wales', 'England', 'Wales']
        country = tab.excel_ref('B10').expand(DOWN).one_of(country_type)
        trace.Country('Country detailed at cell value: {}', var = cellLoc(country))
        observations = sex.expand(RIGHT).expand(DOWN).is_not_blank() - country.expand(RIGHT) - sex
        
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: Deaths, will be filtered out to be either deaths or percent')
        
        icd_10_codes = 'U07.1-U07.2'
        trace.ICD_10_Codes('Hardcoded value as: U07.1-U07.2 ( Table 2: COVID-19 defined as ICD10 codes U07.1 and U07.2)')
                   
        cause_of_death_groups = 'Coronavirus'
        #trace.Cause_of_death_groups('Hardcoded value as: Coronavirus ( Table 2: COVID-19 defined as ICD10 codes U07.1 and U07.2)')
  
        dimensions = [
            HDim(period_month, 'Period', CLOSEST, LEFT),
            HDim(measure_type, 'Measure Type', CLOSEST, LEFT),
            HDim(sex, 'Sex', DIRECTLY, ABOVE),
            HDim(country, 'Country', CLOSEST, ABOVE),
            HDim(age_group, 'Age Group', DIRECTLY, LEFT),
            HDimConst('Unit', unit),
            HDimConst('ICD 10 Codes', icd_10_codes),
            HDimConst('Cause of death groups', cause_of_death_groups),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
       # savepreviewhtml(tidy_sheet)
        trace.store("Deaths_involving_COVID19_England_Wales", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datacube_name, "Deaths_involving_COVID19_England_Wales")
trace.add_column("Value")
trace.Value("Rename databaker column OBS to Value")
df.rename(columns={'OBS': 'Value'}, inplace=True)
trace.Period("Formating period column to month/{year}-{month}")
df['Period'] = df['Period'].apply(lambda x: month_look_up[x])
df["Period"] = df["Period"].apply(date_time)

tidy = df[['Period', 'Cause of death groups', 'Value', 'ICD 10 Codes', "Age Group", "Sex", 'Country', 'Measure Type', 'Unit' ]]

trace.Country("Remove any prefixed whitespace from all values in column and pathify")
trace.Cause_of_death_groups("Remove any prefixed whitespace from all values in column and pathify")
trace.Sex("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Country', 'Cause of death groups', "Sex"):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
tidy['Value'] = tidy['Value'].astype(int)
# -
from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 


# Notes taken from Table 

notes = """
1. Excluding meningitis and meningococcal diseases (A39), sepsis due to haemophilus influenzae (A41.3), rabies (A82), certain mosquito-borne diseases (A83) and yellow fever (A95).
2. In England and Wales, a conclusion of suicide cannot be returned for children under the age of 10 years.
3. England and Wales includes deaths of non-residents. England and Wales separately excludes deaths of non-residents
4. Based on boundaries as of May 2020
5. Based on the date a death occurred rather than when a death was registered
5. : Rates are not available where there are less than 3 deaths
6. Age-specific rates where there were fewer than 20 deaths are unreliable and denoted with a u
"""

# Output Tidy data

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
scraper.dataset.comment = notes
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
scraper.dataset.family = 'covid-19'

import os
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
trace.output()
tidy

