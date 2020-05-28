# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Weekly Deaths_2020

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
# Registration Week, Week Ending, Registered Death Type, Measure Type, Unit, Marker, Value

for name, tab in tabs.items():
    if 'Contents' in name or 'Background' in name or 'Definitions' in name:
        continue
    if name == 'Weekly Deaths_2020':
        registration_week = tab.excel_ref('A4').expand(DOWN).is_not_blank()
        week_ending = tab.excel_ref('B4').expand(DOWN).is_not_blank()
        registered_death_type = tab.excel_ref('C3').expand(RIGHT)
        unit = 'Count'
        measure_type = 'Deaths'
        observations = week_ending.fill(RIGHT).is_not_blank()
        Dimensions = [
            HDim(registration_week,'Registration Week',DIRECTLY,LEFT),
            HDim(week_ending,'Week Ending',DIRECTLY,LEFT),
            HDim(registered_death_type,'Registered Death Type',DIRECTLY,ABOVE),
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

######### Format Week Ending (Period column) ##############
    
df = df.replace({'Marker' : {'-' : 'NULL', np.nan : 'Provisional' } } )

df = df.replace({'Registered Death Type' : {'Range' : 'Minimum in Previous 5 years', 
                                            '' : 'Maximum in Previous 5 years', 
                                            'Covid-193 deaths registered in week (2020P)' : 'Covid-19 deaths registered in week (2020P)',
                                            'Respiratory2 deaths registered in week (2020P)' : 'Respiratory deaths registered in week (2020P)',
                                            'Average number of respiratory2 deaths registered in corresponding week over previous 5 years (2015 to 2019P)' : 'Average number of respiratory deaths registered in corresponding week over previous 5 years (2015 to 2019P)'
                                               }})
f1=((df['Registered Death Type'] =='Minimum in Previous 5 years') | (df['Registered Death Type'] =='Maximum in Previous 5 years'))
df.loc[f1,'Marker'] = ''

df['Registration Week'] = df.apply(lambda x: x['Registration Week'].replace('.0', ''), axis = 1)
df = df.replace('', np.nan, regex=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Registered Death Type'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Registration Week', 'Week Ending', 'Registered Death Type', 'Measure Type', 'Unit', 'Marker', 'Value']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Deaths registered each week in Northern Ireland 2020'
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

#Respiratory deaths include any death where terms directly relating to respiratory causes were mentioned anywhere on the death certificate (this includes COVID-19 deaths). This is not directly comparable to the ONS figures relating to ‘deaths where the underlying cause was respiratory disease’.

#COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
#"""
#scraper.dataset.description = scraper.dataset.description + additional_metadata

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
# -

tidy
