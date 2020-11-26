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
datasetTitle = 'Number of deaths due to COVID-19 by date of death, England and Wales'
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


# +
trace = TransformTrace()
tab = next(t for t in tabs.values() if t.name.startswith('Table 4'))
print(tab.name)

datacube_name = "Number of deaths due to COVID-19 by date of death, England and Wales"
columns=['Period', 'All causes 2020', 'Five year average', 'Measure Type', 'Unit']
trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)

period = tab.filter(contains_string('Date')).shift(0,1).expand(DOWN).is_not_blank()
trace.Period('Period detailed at cell value: {}', var = cellLoc(period))

all_causes_2020 = tab.filter(contains_string('All causes -  2020')).shift(0,1).expand(DOWN).is_not_blank()
trace.All_causes_2020('All causes -  2020 detailed at cell value: {}', var = cellLoc(all_causes_2020))

five_year_average = tab.filter(contains_string('5-year average')).shift(0,1).expand(DOWN).is_not_blank()
trace.Five_year_average('5-year average detailed at cell value: {}', var = cellLoc(five_year_average))

observations = tab.filter(contains_string('Deaths due to COVID-19')).shift(0,1).expand(DOWN).is_not_blank()

measure_type = 'Count'
trace.Measure_Type('Hardcoded value as: Count')
unit = 'Deaths'
trace.Unit('Hardcoded value as: Deaths')

dimensions = [
    HDim(period, 'Period', DIRECTLY, LEFT),
    HDim(all_causes_2020, 'All causes 2020', DIRECTLY, RIGHT),
    HDim(five_year_average, 'Five year average', DIRECTLY, RIGHT),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())

# -


df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
tidy = df[['Period', 'Value', 'All causes 2020', 'Five year average', 'Measure Type', 'Unit']]

# +
#from IPython.core.display import HTML
#for col in df:
#    if col not in ['Value']:
#        df[col] = df[col].astype('category')
#        display(HTML(f"<h2>{col}</h2>"))
#        display(df[col].cat.categories) 
# -


# Notes taken from Table 

notes = """
1. England and Wales includes deaths of non-residents
2. Based on boundaries as of May 2020
3. COVID-19 defined as ICD10 codes U07.1 and U07.2
4. Based on the date a death occurred rather than when a death was registered
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
#tidy


# -


