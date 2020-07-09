# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Table 11

# +
from gssutils import * 
import json 
import numpy as np
import os
from datetime import datetime, timedelta

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    if len(date_string)  == 10:
        return 'gregorian-day/' + date_string 
    elif len(date_string)  == 0:
        return 'year/2020'


# -

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

df = pd.DataFrame()

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Table 11':
        date = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        place_of_death = tab.excel_ref('B4').expand(RIGHT)
        marker = 'Provisional'
        unit = 'Count' #or Cumulative count, will be filtered after 
        measure_type = 'Deaths'
        observations = place_of_death.fill(DOWN).is_not_blank()
        Dimensions = [
            HDim(date,'Date',DIRECTLY,LEFT),
            HDim(place_of_death,'Place of Death',DIRECTLY,ABOVE),
            HDimConst('DATAMARKER', marker),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]
        c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
        #savepreviewhtml(c1, fname=tab.name + " Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)

df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
f1=((df['Place of Death'] =='Cumulative Total'))
df.loc[f1,'Unit'] = 'Cumulative Count'
df['Period'] =  df["Date"].apply(date_time)
df = df.replace('', np.nan, regex=True)

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Place of Death'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].str.rstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Period', 'Place of Death', 'Measure Type', 'Unit', 'Marker', 'Value']]
tidy

destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)
TITLE = 'Covid-19 death occurrences by date and place of death in Northern Ireland'
OBS_ID = pathify(TITLE)
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

notes = """
P Weekly published data are provisional.
1 This data is based on the actual date of death, from those deaths registered by GRO up to 1st July 2020. All data in this table are subject to change, as some deaths will have occurred but haven’t been registered yet.  The first covid-19 death in Northern Ireland occurred on 18th March 2020.
2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
3Includes deaths in care homes only. Care home residents who have died in a different location will be counted elsewhere in this table.
4 The 'Other' category includes deaths at a residential address which was not the usual address of the deceased and all other places.
"""

######## BELOW COMMENT OUT FOR NOW ######
"""
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = TITLE

#scraper.dataset.description = scraper.dataset.description + notes

scraper.dataset.family = 'covid-19'
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
"""
