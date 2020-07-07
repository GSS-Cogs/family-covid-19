# # ONS Deaths involving COVID-19, England and Wales 

from gssutils import * 
import json 
from datetime import datetime

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper 

# +
distribution = scraper.distributions[0]


# -

# Note: This dataset has been split up into 6 cubes atm. 
# Joined Table 1 and Table 2
# Joined Tables: 5, 6a, 6b, 6c, 7a, 7b, 7c,  
# then tables 3, 4, 8 and 9 are sperately transformed.  

# +
import glob

py_files = [i for i in glob.glob('*.{}'.format('py'))]

for i in py_files:
    file = "'" + i + "'"
    if file.startswith("'main") == True:
        continue
    %run $file
