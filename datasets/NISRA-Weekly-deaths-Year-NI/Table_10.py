# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 
#
# ### Sheet : Table 10

# +
from gssutils import * 
import json 
import numpy as np
import os
from datetime import datetime, timedelta

def week_ending_to_week_beginning_date_time (week_ending_date):
    if len(week_ending_date)  == 10:
        week_ending_date = datetime.strptime(week_ending_date, "%Y-%m-%d")
        week_beginning_date = week_ending_date - timedelta(7)
        week_beginning_date = week_beginning_date.strftime("%Y-%m-%d")
        return 'gregorian-interval/' + week_beginning_date + 'T00:00:00/P7D'
    else:
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
    if name == 'Table 10':
        week_of_death = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        week_ending = tab.excel_ref('B5').expand(DOWN).is_not_blank()
        place_of_death = tab.excel_ref('C4').expand(RIGHT)
        unit = 'Count' #or %, will be filtered after 
        measure_type = 'Deaths'
        observations = place_of_death.fill(DOWN).is_not_blank()
        Dimensions = [
            HDim(week_of_death,'Week of Death',DIRECTLY,LEFT),
            HDim(week_ending,'Week Ending',DIRECTLY,LEFT),
            HDim(place_of_death,'Place of Death',DIRECTLY,ABOVE),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]
        c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
        #savepreviewhtml(c1, fname=tab.name + " Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)

# +

df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df['Marker'] = df['Marker'].map(lambda x: "not-applicable" if x == "-" else "provisional")
f1=((df['Place of Death'] =='% of all Covid-19 Deaths') | (df['Place of Death'] =='% of all Covid-19 Hospital Deaths') )
df.loc[f1,'Unit'] = 'Percent'
df.loc[f1,'Measure Type'] = 'Percentage'
df['Period'] =  df["Week Ending"].apply(week_ending_to_week_beginning_date_time)
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
        df[column] = df[column].str.rstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Week of Death', 'Week Ending', 'Place of Death', 'Measure Type', 'Unit', 'Marker', 'Value']]
tidy

destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)
TITLE = 'Covid 19 deaths of care home residents in Northern Ireland, by place of death, in Northern Ireland'
OBS_ID = pathify(TITLE)
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

notes = """
P Weekly published data are provisional.
1 This data is based on the actual date of death, from those deaths registered by GRO up to 1st July 2020. All data in this table are subject to change, as some deaths will have occurred but haven’t been registered yet.
2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.							
3 Care home residents have been identified where either (a) the death occurred in a care home, or (b) the death occurred elsewhere but the place of usual residence of the deceased was recorded as a care home. It should be noted that the statistics will not capture those cases where a care home resident died in hospital or another location and the usual address recorded on their death certificate is not a care home.
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
