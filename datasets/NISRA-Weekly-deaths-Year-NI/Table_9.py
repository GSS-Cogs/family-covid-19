# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet 9  : Covid 19 deaths12 of care home residents3 in Northern Ireland, by place of death, 2020P

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

df = pd.DataFrame()

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Table 9':
        week_of_death = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        week_ending = tab.excel_ref('B5').expand(DOWN).is_not_blank()
        place_of_death = tab.excel_ref('C4').expand(RIGHT)
        marker = 'Provisional'
        unit = 'Count' #Or percent
        measure_type = 'Deaths' # or percentage 
        observations = place_of_death.fill(DOWN).is_not_blank()
        Dimensions = [
            HDim(week_of_death,'Week of Death',DIRECTLY,LEFT),
            HDim(week_ending,'Week Ending',DIRECTLY,LEFT),
            HDim(place_of_death,'Place of Death',DIRECTLY,ABOVE),
            HDimConst('DATAMARKER', marker),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]
        c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + " Preview.html")
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
f1=((df['Place of Death'] =='% of all Covid-19 Hospital Deaths') | (df['Place of Death'] =='% of all Covid-19 Deaths'))
df.loc[f1,'Measure Type'] = 'percentage'
df.loc[f1,'Unit'] = 'percent'

df['Week of Death'] = df.apply(lambda x: x['Week of Death'].replace('.0', ''), axis = 1)
df = df.replace('', np.nan, regex=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Place of Death'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Week of Death', 'Week Ending', 'Place of Death', 'Measure Type', 'Unit', 'Marker', 'Value']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Covid-19 Death of care home residents in Northern Irelandby week of death and Place of Death' 
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

# +
######## BELOW COMMENT OUT FOR NOW ######


#from gssutils.metadata import THEME
#scraper.set_base_uri('http://gss-data.org.uk')
#scraper.set_dataset_id(f'{GROUP_ID}/{OBS_ID}')
#scraper.dataset.title = TITLE

## Adding short metadata to description
#additional_metadata = """ Weekly published data are provisional.

#1 This data is based on the actual date of death, from those deaths registered by GRO up to 27th May 2020. All data in this table are subject to change, as some deaths will have occurred but haven’t been registered yet.

#2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.

#3 Care home residents have been identified where either (a) the death occurred in a care home, or (b) the death occurred elsewhere but the place of usual residence of the deceased was recorded as a care home. It should be noted that the statistics will not capture those cases where a care home resident died in hospital or another location and the usual address recorded on their death certificate is not a care home. 

#"""

#scraper.dataset.description = scraper.dataset.description + additional_metadata

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
# -

tidy