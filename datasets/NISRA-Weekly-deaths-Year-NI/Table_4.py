# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Covid-19_Deaths_age by sex

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

df = pd.DataFrame()

# ##### Table Structure 
# 	Gender, Age, Week Number, Week Ending, Measure Type, Unit, Marker, Value
#

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Table 4':
        gender = tab.excel_ref('A6').expand(DOWN).is_not_blank()
        age = tab.excel_ref('B6').expand(DOWN).is_not_blank()
        week_number = tab.excel_ref('C4').expand(RIGHT) #- tab.excel_ref('W3').expand(RIGHT)
        week_ending = tab.excel_ref('C5').expand(RIGHT) #- tab.excel_ref('W4').expand(RIGHT)
        marker = 'Provisional'
        unit = 'Count'
        measure_type = 'Deaths'
        observations = week_ending.fill(DOWN).is_not_blank()
        
        Dimensions = [
            HDim(gender,'Gender',CLOSEST,ABOVE),
            HDim(age,'Age',DIRECTLY,LEFT),
            HDim(week_number,'Week Number',DIRECTLY,ABOVE),
            HDim(week_ending,'Week Ending',DIRECTLY,ABOVE),
            HDimConst('DATAMARKER', marker),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]
        c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)


def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    if len(date_string)  == 10:
        return 'gregorian-day/' + date_string + 'T00:00/P7D'
    elif len(date_string)  == 0:
        return 'year/2020'



# +
import numpy as np
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

df["Week Ending"] = df["Week Ending"].apply(date_time)

df['Week Number'] = df.apply(lambda x: x['Week Number'].replace('.0', ''), axis = 1)
df = df.replace('', np.nan, regex=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Gender'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Gender', 'Age', 'Week Number', 'Week Ending', 'Measure Type', 'Unit', 'Marker', 'Value']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Covid-19 Deaths registered each week in Northern Ireland, age by sex'
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# -

tidy

# +
######## BELOW COMMENT OUT FOR NOW ######


#from gssutils.metadata import THEME
#scraper.set_base_uri('http://gss-data.org.uk')
#scraper.set_dataset_id(f'{GROUP_ID}/{OBS_ID}')
#scraper.dataset.title = TITLE

## Adding short metadata to description
#additional_metadata = """ Weekly published data are provisional.

#This data is based on registrations of deaths, not occurrences. The majority of deaths are registered within five days in Northern Ireland.

#COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.

#"""
#scraper.dataset.description = scraper.dataset.description + additional_metadata

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
# -


