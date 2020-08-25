# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Table 4

# +
from gssutils import * 
import json 
import numpy as np
import os
from datetime import datetime, timedelta

def week_ending_to_week_beginning_date_time (week_ending_date):
    if len(week_ending_date)  == 10:
        week_ending_date = datetime.strptime(week_ending_date, "%Y-%m-%d")
        week_beginning_date = week_ending_date - timedelta(6)
        week_beginning_date = week_beginning_date.strftime("%Y-%m-%d")
        return 'gregorian-interval/' + week_beginning_date + 'T00:00:00/P7D'
    else:
        return 'year/2020'


# -

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

scrape.distributions = [x for x in scrape.distributions if x.mediaType == Excel]
tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

df = pd.DataFrame()

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
        #savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)

import numpy as np
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df['Period'] =  df["Week Ending"].apply(week_ending_to_week_beginning_date_time)
df['Week Number'] = df.apply(lambda x: x['Week Number'].replace('.0', ''), axis = 1)
df = df.replace('', np.nan, regex=True)

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

tidy = df[['Gender', 'Age', 'Week Number', 'Period', 'Measure Type', 'Unit', 'Marker', 'Value']]
tidy

# +
#destinationFolder = Path('out')
#destinationFolder.mkdir(exist_ok=True, parents=True)

#TITLE = 'Covid-19 Deaths registered each week in Northern Ireland, age by sex'
#OBS_ID = pathify(TITLE)
#GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
#ßtidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# -

notes = """
P Weekly published data are provisional.
1 This data is based on registrations of deaths, not occurrences. The majority of deaths are registered within five days in Northern Ireland.
2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
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
