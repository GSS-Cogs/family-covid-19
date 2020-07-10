# # WG Notifications of deaths of residents related to COVID-19 in adult care homes 

from gssutils import * 
import json 
import numpy as np

if is_interactive():
    from requests import Session
    from cachecontrol import CacheControl
    from cachecontrol.caches.file_cache import FileCache
    from cachecontrol.heuristics import ExpiresAfter
    scrape = Scraper(seed="info.json",
                     session=CacheControl(Session(), cache=FileCache('.cache'), heuristic=ExpiresAfter(days=1))
    )
    dist = scrape.distribution(
        latest=True,
        title=lambda x: x.startswith('Notifications of deaths of residents related to COVID-19')
    )
    tabs = { tab.name: tab for tab in dist.as_databaker() }
list(tabs)


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]

tab_name_expected = 'Table_3'
ref_cell_expected = 'Suspected'
title_to_include = 'Notifications of deaths of residents from adult care homes by date of notification and cause'
df = pd.DataFrame()
# -

#Check the tab/sheet has expected name before continuing. 
if (tab_name_expected in tabs) != True:
    raise Exception(tab_name_expected + " not found. Something has changed with the naming of sheets within this dataset")
else:
    tab = tabs[tab_name_expected]
    #Checking the title of the sheet in question is what is expected.
    title_of_tab = tab.excel_ref('A1')
    title_of_tab = str(title_of_tab)
    expected_title = title_to_include #Change this as needed / dataset is updated
    if expected_title in title_of_tab:
        print('correct tab title found, ')
        try: 
            ref_cell = tab.filter(ref_cell_expected)
            print(ref_cell)
            ref_cell.assert_one()
            print('ref cell "' +  ref_cell_expected + '" found. begining transformation...') 
        except:
            raise Exception("Expected ref cell not found")
    
        #Define Dimensions and transform 
        notification_day = ref_cell.shift(-3,0).expand(DOWN).is_not_blank()
        notification_year = ref_cell.shift(-3, -2).expand(RIGHT).is_not_blank()
        #Due to the 'Cause of Death' dimension being across two rows, I identify them seperately then will add them together. 
        cause_of_death_1 = ref_cell.shift(-2,-1).expand(RIGHT)
        cause_of_death_2 = ref_cell.shift(-2,0).expand(RIGHT)
        measure_type = 'Deaths'
        unit = 'Count'
        observations = cause_of_death_2.fill(DOWN).is_not_blank()
        #savepreviewhtml(observations)
        dimensions = [
            HDim(notification_day, 'Notification Day', DIRECTLY, LEFT),
            HDim(notification_year, 'Notification Year', CLOSEST, LEFT),
            HDim(cause_of_death_1, 'Cause of Death', DIRECTLY, ABOVE),
            HDim(cause_of_death_2, 'Cause of Death 2', DIRECTLY, ABOVE),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)   
df


# +
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df['Cause of Death'] =  df['Cause of Death'] + ' ' +  df['Cause of Death 2'] 
df.drop('Cause of Death 2', axis=1, inplace=True)

from datetime import date
def to_date(row):
    year = row['Notification Year']
    return f"{year}{row['Notification Day'][4:]}"


df['Notification Year'] = pd.to_numeric(df['Notification Year'], downcast='integer')
df['Notification Day'] = df.apply(to_date, axis=1)
df.drop('Notification Year', axis=1, inplace=True)
#df['Notification Year'] = df.apply(lambda x: x['Notification Year'].replace('.0', ''), axis = 1)

## Anticipating the two 'totals' in the dimension 'Cause of Death' will cause a duplicate key error ##

df = df.replace('', np.nan, regex=True)
df
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Cause of Death'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Notification Day', 'Cause of Death', 'Measure Type', 'Unit', 'Value', 'Marker']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Notifications of deaths of residents from adult care homes by date of notification and cause'
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# -

tidy


