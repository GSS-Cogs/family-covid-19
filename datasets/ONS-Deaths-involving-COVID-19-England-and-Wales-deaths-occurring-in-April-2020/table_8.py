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
datasetTitle = "Average number of pre-existing conditions recorded on the death certificate, deaths involving COVID-19."

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
tab = next(t for t in tabs.values() if t.name.startswith('Table 8'))
print(tab.name)

datacube_name = "Number of deaths due to COVID-19 by date of death, England and Wales"
columns=['Period', 'Sex', 'Age Group', 'Country', 'Measure Type', 'Unit']
trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)

sex = tab.filter(contains_string('Sex')).shift(0,1).expand(DOWN).is_not_blank()
trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))

age_group = tab.filter(contains_string('Age group')).shift(0,1).expand(DOWN).is_not_blank()
trace.Age_Group('Age Group detailed at cell value: {}', var = cellLoc(age_group))

country = tab.filter(contains_string('Age group')).shift(1,0).expand(RIGHT).is_not_blank()
trace.Country('Country detailed at cell value: {}', var = cellLoc(country))

observations = country.fill(DOWN).is_not_blank()

measure_type = 'Average'
trace.Measure_Type('Hardcoded value as: Count')
unit = 'Deaths'
trace.Unit('Hardcoded value as: Deaths')

dimensions = [
    #HDim(period, 'Period', DIRECTLY, LEFT),
    HDim(sex, 'Sex', DIRECTLY, LEFT),
    HDim(age_group, 'Age Group', DIRECTLY, LEFT),
    HDim(country, 'Country', DIRECTLY, ABOVE),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


#


# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
tidy = df[[ 'Value', 'Sex', 'Age Group', 'Country', 'Measure Type', 'Unit']]

temporal_date = 'gregorian-interval/2020-03-01T00:00:00/P3M'


# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 


# Notes taken from Table 

notes = """
1. Figures include deaths of non-residents.
2. Figures are provisional.
3. Based on deaths involving COVID-19 (ICD-10 codes U07.1 and U07.2) rather than deaths where COVID-19 was the underlying cause of death.
4. Deaths occurring between March and May 2020 rather than deaths registered between March and May 2020.
5. Including deaths registered up until 6 June 2020.
6. Based on boundaries as of May 2020
"""

# Output Tidy data

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
scraper.dataset.comment = notes
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
scraper.dataset.family = 'covid-19'
temporal_date = 'gregorian-interval/2020-03-01T00:00:00/P3M'
import os
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
trace.output()
tidy



# -


