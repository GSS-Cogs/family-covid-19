# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Weekly_Deaths_Age by Sex

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
# 	Gender, Age, Week Number, Week Ending, Measure Type, Unit, Marker, Value
#     
#     A - Gender
# 	B - Age (Codelist)
# 	C3:V3 - Week Number
# 	C4:V4 - Week Ending (Friday) - C3:4 to be given just the year or a date range
# 	Measure Type = Deaths
# 	Unit - Count
# 	Put Provisional in Marker column
#

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Weekly_Deaths_Age by Sex':
        gender = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        age = tab.excel_ref('B5').expand(DOWN).is_not_blank()
        week_number = tab.excel_ref('C3').expand(RIGHT) - tab.excel_ref('W3').expand(RIGHT)
        week_ending = tab.excel_ref('C4').expand(RIGHT) - tab.excel_ref('W4').expand(RIGHT)
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


# +
import numpy as np
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df = df.replace({'Week Ending' : {'' : 'year/2020'}})

######### Format Week Ending (Period column) #######

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

TITLE = 'Deaths registered each week in Northern Ireland'
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

#"""
#scraper.dataset.description = scraper.dataset.description + additional_metadata

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
# -


