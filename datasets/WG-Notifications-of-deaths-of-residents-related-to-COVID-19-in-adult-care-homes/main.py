# # WG Notifications of deaths of residents related to COVID-19 in adult care homes 

from gssutils import * 
import json 
import numpy as np
import glob
from requests import Session
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from cachecontrol.heuristics import ExpiresAfter

scrape = Scraper(seed="info.json",
                 session=CacheControl(Session(), cache=FileCache('.cache'), heuristic=ExpiresAfter(days=1))
)
scraper = scrape
scraper

dist = scrape.distribution(
    latest=True,
    title=lambda x: x.startswith('Notifications of deaths of residents related to COVID-19')
)
dist

tabs = { tab.name: tab for tab in dist.as_databaker() }
list(tabs)

# +
#Check tab contents is what is expected before continuing. 

expected_tabs = ['Contents','Information','Table_1','Table_2','Table_3','Table_4','Table_5','Table_6','Table_7','Table_8', 'Table_9']
whats_missing = [item for item in tabs if item not in expected_tabs]

tables = {}

# Check firstly there is no tabs missing / removed from latest update
if  len(whats_missing) != 0:
    print(whats_missing)
    raise Exception('Something has been updated in the dataset. Cannot find tab(s) ', whats_missing)
else:
    #nothing missing, check if list is what is expected
    if list(tabs) != expected_tabs: 
        raise Exception('Something has been updated in the dataset. List of tabs expected has changed. expecting ',  expected_tabs , ' but found: ', list(tabs))
    else : 
        #All remains the same, runing trnasformation scripts 
        print ("The lists are identical, running transformation scripts for tab(s) listed. ", list(tabs))
        py_files = [i for i in glob.glob('*.{}'.format('py'))]

        for i in py_files:
            file = "'" + i + "'"
            if file.startswith("'main") == True:
                continue
            %run -i $file
            tables[f'{i[:-3]} - {pathify(expected_title.strip())}'] = tidy
# +
from IPython.core.display import HTML

for key in sorted(tables.keys()):
    display(HTML(f'<h2>{key}</h2>'))
    display(tables[key])                 
# -

merge_cols = ['Notification Date', 'Area Code', 'Location of Death', 'Cause of Death', 'Care Provided', 'Value']
def add_hidden(df):
    for col in merge_cols:
        if col not in df:
            if col == 'Area Code':
                df[col] = 'W92000004'
            else:
                df[col] = 'total'
    return df[merge_cols]


# +
t1 = tables['table_1 - notifications-of-service-user-deaths-received-from-adult-care-homes'].copy()
t1.drop(columns=['Measure Type', 'Unit'], inplace=True)
t1.rename(columns={'Notification Date Range': 'Notification Date'}, inplace=True)

from datetime import datetime
import isodate
from dateutil.parser import parse

def range_to_duration(r):
    start, end = [parse(d.strip(), dayfirst=True) for d in r.split('-')]
    return f'gregorian-interval/{start.isoformat()}/{isodate.duration_isoformat(end - start)}'

t1['Notification Date'] = t1['Notification Date'].map(range_to_duration)
t1['Value'] = pd.to_numeric(t1['Value'], downcast='integer')
t1 = add_hidden(t1)
t1
# -

t2 = tables['table_2 - notifications-of-deaths-of-adult-care-home-residents-with-confirmed-or-suspected-covid-19-by-location-of-death'].copy()
t2.drop(columns=['Measure Type', 'Unit'], inplace=True)
t2.rename(columns={'Notification Date Range': 'Notification Date'}, inplace=True)
t2['Notification Date'] = t2['Notification Date'].map(lambda x: f'gregorian-interval/{x}')
t2['Value'] = pd.to_numeric(t2['Value'], downcast='integer')
t2['Cause of Death'] = 'covid-total'
t2 = add_hidden(t2)
t2

t3 = tables['table_3 - notifications-of-deaths-of-residents-from-adult-care-homes-by-date-of-notification-and-cause'].copy()
#tidy3 = tables['notifications-of-deaths-of-residents-from-adult-care-homes-by-date-of-notification-and-cause'].copy()
t3 = t3[t3['Marker'].isna()]
t3.drop(columns=['Marker', 'Measure Type', 'Unit'], inplace=True)
t3['Value'] = pd.to_numeric(t3['Value'], downcast='integer')
t3.rename(columns={'Notification Day': 'Notification Date'}, inplace=True)
t3['Notification Date'] = t3['Notification Date'].map(lambda x: f'day/{x}')
#t3['Cause of Death'].cat.rename_categories({'total': 'all', 'confirmes': 'covid-confirmed', 'all-deaths-total': 'all'})
t3 = add_hidden(t3)
t3

t4 = tables['table_4 - notifications-of-deaths-of-adult-care-home-residents-with-confirmed-or-suspected-covid-19-by-location-of-death-and-date-of-notification'].copy()
t4.drop(columns=['Measure Type', 'Unit'], inplace=True)
t4.rename(columns={'Notification Date Range': 'Notification Date'}, inplace=True)
t4['Value'] = pd.to_numeric(t4['Value'], downcast='integer')
t4['Notification Date'] = t4['Notification Date'].map(lambda x: f'day/{x}')
t4['Cause of Death'] = 'covid-total'
t4 = add_hidden(t4)
t4

t5 = tables['table_5 - notifications-of-deaths-of-adult-care-home-residents-by-location-of-death-and-date-of-notification'].copy()
t5.drop(columns=['Measure Type', 'Unit'], inplace=True)
t5['Value'] = pd.to_numeric(t5['Value'], downcast='integer')
t5['Notification Date'] = t5['Notification Date'].map(lambda x: f'day/{x}')
# assume this is all deaths, not just COVID-19 related.
t5 = add_hidden(t5)
t5

t6 = tables['table_6 - number-of-notifications-of-deaths-of-adult-care-home-residents-involving-covid-19-both-confirmed-and-suspected-occurring-in-care-homes-by-local-authority-and-day-of-notification'].copy()
t6.drop(columns=['Local Authority', 'Unit'], inplace=True)
t6['Notification Date'] = t6['Notification Date'].map(lambda x: f'day/{x}')
t6['Value'] = pd.to_numeric(t6['Value'], downcast='integer')
t6['Cause of Death'] = 'covid-total'
t6['Location of Death'] = 'at-the-service'
t6 = add_hidden(t6)
t6

t7 = tables['table_7 - number-of-notifications-of-deaths-of-adult-care-home-residents-involving-covid-19-both-confirmed-and-suspected-occurring-in-any-location-by-local-authority-and-day-of-notification'].copy()
t7.drop(columns=['Local Authority', 'Unit'], inplace=True)
t7['Notification Date'] = t7['Notification Date'].map(lambda x: f'day/{x}')
t7['Value'] = pd.to_numeric(t7['Value'], downcast='integer')
t7['Cause of Death'] = 'covid-total'
t7 = add_hidden(t7)
t7

t8 = tables['table_8 - number-of-notifications-of-deaths-of-adult-care-home-residents-by-local-authority-and-day-of-notification'].copy()
t8.drop(columns=['Local Authority', 'Unit'], inplace=True)
t8['Notification Date'] = t8['Notification Date'].map(lambda x: f'day/{x}')
t8['Value'] = pd.to_numeric(t8['Value'], downcast='integer')
# assuming all causes
t8 = add_hidden(t8)
t8

t9 = tables['table_9 - number-of-notifications-of-deaths-of-adult-care-home-residents-occuring-in-care-homes-by-local-authority-and-day-of-notification'].copy()
t9.drop(columns=['Local Authority', 'Unit'], inplace=True)
t9['Notification Date'] = t9['Notification Date'].map(lambda x: f'day/{x}')
t9['Value'] = pd.to_numeric(t9['Value'], downcast='integer')
# assuming all causes
t9['Location of Death'] = 'at-the-service'
t9 = add_hidden(t9)
t9

# +
t1['table'] = 1
t2['table'] = 2
t3['table'] = 3
t4['table'] = 4
t5['table'] = 5
t6['table'] = 6
t7['table'] = 7
t8['table'] = 8
t9['table'] = 9
merged = pd.concat([t1, t2, t3, t4, t5, t6, t7, t8, t9], sort=False).drop_duplicates()
merged = merged.drop_duplicates(subset=merged.columns.difference(['table']))
merged

#cubes = Cubes('info.json')
#cubes.add_cube(scraper, merged), scraper.dataset.title)
#cubes.output_all()

# +
out = Path('out')
out.mkdir(exist_ok=True)

merged[merged.duplicated(subset=merged.columns.difference(['table', 'Value']))].to_csv(out / 'multi-valued-observations.csv')
merged.drop(columns=['table'], inplace=True)
merged = merged.drop_duplicates(subset=merged.columns.difference(['table', 'Value']), keep='last')

# +
import os
from urllib.parse import urljoin

out = Path('out')
out.mkdir(exist_ok=True)
merged.to_csv(out / 'observations.csv', index = False)
scraper.dataset.family = 'covid-19'

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / 'observations.csv')
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / 'observations.csv-metadata.json')
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -


