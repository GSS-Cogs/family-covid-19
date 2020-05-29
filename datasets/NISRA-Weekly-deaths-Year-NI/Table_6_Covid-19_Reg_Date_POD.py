# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Covid-19_Reg Date & POD

from gssutils import * 
import json 

# +
#info = json.load(open('info.json')) 
#landingPage = info['landingPage'] 
#landingPage 

# +
#### Add transformation script here #### 

#scraper = Scraper(landingPage) 
#scraper.select_dataset(latest=True) 
#scraper 
# -

data = loadxlstabs("./source/Weekly_Deaths.xls") 

tabs = {tab.name: tab for tab in data}
list(tabs)

df = pd.DataFrame()

# ##### Table Structure 
# Week of Death, Week Ending, Place of Death, Measure Type, Unit, Marker, Value
#
#     A - Week of Death
# 	B - Week Ending (Friday)
# 	C3:H3 - Place of Death (Codelist)
# 	Measure Type = Deaths
# 	Unit - Count
# 	Put Provisional in Marker column
#

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Covid-19 Reg Date & POD':
        week_of_death = tab.excel_ref('A4').expand(DOWN).is_not_blank()
        week_ending = tab.excel_ref('B4').expand(DOWN).is_not_blank()
        place_of_death = tab.excel_ref('C3').expand(RIGHT)
        marker = 'Provisional'
        unit = 'Count'
        measure_type = 'Deaths'
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

# +
import numpy as np
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

######### Format Week Ending (Period column) ##############

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

TITLE = 'Covid-19 Deaths registered in Northern Ireland by Place of Death'
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

#1 This data is based on registrations of deaths, not occurrences. The majority of deaths are registered within five days in Northern Ireland.

#2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.

#3 Includes deaths in care homes only. Care home residents who have died in a different location will be counted elsewhere in this table. 

#4 The 'Other' category includes deaths at a residential address which was not the usual address of the deceased and all other places.

#"""

#scraper.dataset.description = scraper.dataset.description + additional_metadata

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
# -

tidy
