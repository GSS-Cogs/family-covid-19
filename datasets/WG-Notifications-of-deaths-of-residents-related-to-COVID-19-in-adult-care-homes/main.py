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

# -





