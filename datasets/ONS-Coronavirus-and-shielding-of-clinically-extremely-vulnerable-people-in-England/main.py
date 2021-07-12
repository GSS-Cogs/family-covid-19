# -*- coding: utf-8 -*-
# # ONS-Coronavirus-and-shielding-of-clinically-extremely-vulnerable-people-in-England

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

tabs_name = ['Contents', 'Definitions']
tabs = {tab: tab for tab in dist.as_databaker() if tab.name not in tabs_name}
