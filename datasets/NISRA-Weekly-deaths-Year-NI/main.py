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
import glob

py_files = [i for i in glob.glob('*.{}'.format('py'))]

for i in py_files:
    file = "'" + i + "'"
    if file.startswith("'main") == True:
        continue
    %run $file

