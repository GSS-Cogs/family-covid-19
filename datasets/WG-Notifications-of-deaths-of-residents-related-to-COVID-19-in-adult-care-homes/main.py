# # WG Notifications of deaths of residents related to COVID-19 in adult care homes 

from gssutils import * 
import json 
import numpy as np
import glob

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Notifications of deaths of residents related to COVID-19 in adult care homes"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
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
            %run $file
            tables[OBS_ID] = tidy
# +
from IPython.core.display import HTML

for key, table in tables.items():
    display(HTML(f'<h2>{key}</h2>'))
    display(table)                 

# +
cubes = Cubes('info.json')

cube1 = tables['number-of-notifications-of-deaths-of-adult-care-home-residents-involving-covid-19-both-confirmed-and-suspected-occurring-in-care-homes-by-local-authority-and-day-of-notification'].copy()
cube1.drop(columns=['Local Authority', 'Unit'], inplace=True)
cube1['Notification Date'] = cube1['Notification Date'].map(lambda x: f'day/{x}')
cube1['Value'] = pd.to_numeric(cube1['Value'], downcast='integer')
cube1

# +
cube2 = tables['notifications-of-service-user-deaths-received-from-adult-care-homes'].copy()
cube2.drop(columns=['Measure Type', 'Unit'], inplace=True)
cube2.rename(columns={'Notification Date Range': 'Notification Date'}, inplace=True)

from datetime import datetime
import isodate

def rangeToDuration(r):
    start, end = [datetime.strptime(d.strip(), '%d/%m/%Y') for d in r.split('-')]
    return f'gregorian-interval/{start.isoformat()}/{isodate.duration_isoformat(end - start)}'
    
cube2['Notification Date'] = cube2['Notification Date'].map(rangeToDuration)
pd.
cube2
# -


