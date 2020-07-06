# -*- coding: utf-8 -*-
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

# +
datasetTitle = "Number of deaths by date of occurrence and whether they were registered within 7 days of date of death."
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



# +
trace = TransformTrace()
tab = next(t for t in tabs.values() if t.name.startswith('Table 9'))
print(tab.name)

datacube_name = "Number of deaths due to COVID-19 by date of death, England and Wales"
columns=['Period', 'Death Cause', 'Registered Death Information', 'Measure Type', 'Unit']
trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)

period = tab.filter(contains_string('Date of occurrence')).shift(0,1).expand(DOWN).is_not_blank()
trace.Period('Period detailed at cell value: {}', var = cellLoc(period))

death_cause_all = tab.filter(contains_string('All causes of death')).is_not_blank()
trace.Death_Cause('Death Cause detailed at cell value: {}', var = cellLoc(death_cause_all))

death_cause_covid = tab.filter(contains_string('Death involving COVID-19')).is_not_blank()
trace.Death_Cause('Death Cause detailed at cell value: {}', var = cellLoc(death_cause_all))

reg_death_info_all = tab.filter(contains_string('Date of occurrence')).shift(1,0).expand(RIGHT).is_not_blank() - death_cause_covid.shift(-1,1).expand(RIGHT)
trace.Registered_Death_Information('Death Cause detailed at cell value: {}', var = cellLoc(reg_death_info_all))


reg_death_info_covid = death_cause_covid.shift(-1,1).expand(RIGHT)
trace.Registered_Death_Information('Death Cause detailed at cell value: {}', var = cellLoc(reg_death_info_covid))


observations = reg_death_info_all.fill(DOWN).is_not_blank()

measure_type = 'Count'
trace.Measure_Type('Hardcoded value as: Count, Median and percentage will be filtered out after transformation')
unit = 'Deaths'
trace.Unit('Hardcoded value as: Deaths')

dimensions = [
    HDim(period, 'Period', DIRECTLY, LEFT),
    HDim(death_cause_all, 'Death Cause', CLOSEST, ABOVE),
    HDim(reg_death_info_all, 'Registered Death Information', DIRECTLY, ABOVE),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())

observations = reg_death_info_covid.fill(DOWN).is_not_blank()


dimensions = [
    HDim(period, 'Period', DIRECTLY, LEFT),
    HDim(death_cause_covid, 'Death Cause', CLOSEST, ABOVE),
    HDim(reg_death_info_covid, 'Registered Death Information', DIRECTLY, ABOVE),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")


df = df.replace({'DATAMARKER' : {
    'z' : 'no death registrations involving COVID-19'}})

f1=((df['Registered Death Information'] =="% registered in 7 days"))
df.loc[f1,'Measure Type'] = 'Percentage'

f1=((df['Registered Death Information'] =="Median registration delay (days)"))
df.loc[f1,'Measure Type'] = 'Median'


tidy = df[[ 'Value', 'Period', 'Death Cause', 'Registered Death Information', 'Measure Type', 'Unit', 'DATAMARKER']]

tidy
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 


# Notes taken from Table 

notes = """
1. 'z' denotes days where there were no death registrations involving COVID-19.
2. Based on deaths occurring between March and May 2020 rather than deaths registered in March to May 2020.
3. Deaths involving COVID-19 rather than deaths where COVID-19 was the underlying cause of death.
4. Figures are provisional.
5. Figures include deaths of non-residents.
6. Including deaths registered up until 6 June 2020.
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


# -


