# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

# +
# %%capture

# %run "Table_1.py"
# %run "Table_2.py"
# %run "Table_3.py"
# %run "Table_4.py"
# %run "Table_5.py"
# %run "Table_6.py"
# %run "Table_7.py"
# %run "Table_8.py"
# %run "Table_9.py"
# %run "Table_10.py"



