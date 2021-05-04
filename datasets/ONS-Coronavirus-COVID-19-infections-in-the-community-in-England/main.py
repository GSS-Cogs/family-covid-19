# -*- coding: utf-8 -*-
# # ONS-Coronavirus-COVID-19-infections-in-the-community-in-England

# +
import pandas as pd
from gssutils import *
import json

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

scraper = Scraper(seed='info.json')
scraper

trace = TransformTrace()
cubes = Cubes('info.json')

dist = scraper.distribution(latest=True)
datasetTitle = info['title']
dist
datasetTitle

tabs_name = ['1', '2a', '2b', '3a', '3b', '4a', '4b', '5a', '5b']
tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}
