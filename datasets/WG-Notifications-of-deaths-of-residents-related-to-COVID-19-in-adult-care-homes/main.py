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
            tables[pathify(expected_title.strip())] = tidy
# +
from IPython.core.display import HTML

for key, table in tables.items():
    display(HTML(f'<h2>{key}</h2>'))
    display(table)                 
# -

tidy1 = tables['number-of-notifications-of-deaths-of-adult-care-home-residents-involving-covid-19-both-confirmed-and-suspected-occurring-in-care-homes-by-local-authority-and-day-of-notification'].copy()
tidy1.drop(columns=['Local Authority', 'Unit'], inplace=True)
tidy1['Notification Date'] = tidy1['Notification Date'].map(lambda x: f'day/{x}')
tidy1['Value'] = pd.to_numeric(tidy1['Value'], downcast='integer')
tidy1['Care Provided'] = 'total'
tidy1['Cause of Death'] = 'total'
tidy1

# +
tidy2 = tables['notifications-of-service-user-deaths-received-from-adult-care-homes'].copy()
display(tidy2)
tidy2.drop(columns=['Measure Type', 'Unit'], inplace=True)
tidy2.rename(columns={'Notification Date Range': 'Notification Date'}, inplace=True)

from datetime import datetime
import isodate
from dateutil.parser import parse

def range_to_duration(r):
    start, end = [parse(d.strip()) for d in r.split('-')]
    return f'gregorian-interval/{start.isoformat()}/{isodate.duration_isoformat(end - start)}'

tidy2['Notification Date'] = tidy2['Notification Date'].map(range_to_duration)
tidy2['Value'] = pd.to_numeric(tidy2['Value'], downcast='integer')
tidy2['Area Code'] = 'W92000004'
tidy2['Cause of Death'] = 'total'
tidy2
# -

tidy3 = tables['notifications-of-deaths-of-residents-from-adult-care-homes-by-date-of-notification-and-cause'].copy()
tidy3 = tidy3[tidy3['Marker'].isna()]
tidy3.drop(columns=['Marker', 'Measure Type', 'Unit'], inplace=True)
tidy3['Value'] = pd.to_numeric(tidy3['Value'], downcast='integer')
tidy3.rename(columns={'Notification Day': 'Notification Date'}, inplace=True)
tidy3['Notification Date'] = tidy3['Notification Date'].map(lambda x: f'day/{x}')
tidy3['Care Provided'] = 'total'
tidy3['Area Code']  = 'W92000004'
tidy3

# +
#cubes = Cubes('info.json')
#cubes.add_cube(scraper, pd.concat([tidy1, tidy2, tidy3], sort=False), scraper.dataset.title)
#cubes.output_all()

# +
import os
from urllib.parse import urljoin

out = Path('out')
out.mkdir(exist_ok=True)
pd.concat([tidy1, tidy2, tidy3], sort=False).drop_duplicates().to_csv(out / 'observations.csv', index = False)
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


