# -*- coding: utf-8 -*-
# # ONS-Deaths-involving-COVID-19-UK

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

dist = scraper.distribution(latest=True, mediaType=Excel)
datasetTitle = info['title']
dist
datasetTitle

tabs_name = ['Table 1', 'Table 2', 'Table 3', 'Table 4']
tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}
