# -*- coding: utf-8 -*-
# # MMO Ad hoc statistical release  UK Sea Fisheries Statistics 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

# +
#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper 
# -

tabs = { tab.name: tab for tab in scraper.distribution(latest=True).as_databaker() }
list(tabs)

# +
# %%capture

# %run "table_1.py"
# %run "table_2.py"
# %run "table_3.py"
# %run "table_4.py"
