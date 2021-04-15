# -*- coding: utf-8 -*-
# # NE-The-People-and-Nature-Survey-for-England

# +
import pandas as pd
from gssutils import *
import json

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

scraper = Scraper(seed='info.json')
scraper

distribution = scraper.distribution(latest=True)
distribution

trace = TransformTrace()
cubes = Cubes("info.json")

dist = scraper.distribution(mediaType=ODS)
xls = pd.ExcelFile(dist.downloadURL, engine="odf")
with pd.ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet, index = False)
    writer.save()
tabs = loadxlstabs("data.xls")

datasetTitle = info["title"]
tabs_name = ['Q1', 'Q2', 'Q4b', 'Q4e', 'Q6', 'Q34b', 'Q49a', 'Q49b', 'Q59a']
columns=['Question', 'Answer', 'Value Type', 'Measure Type', 'Unit', 'Period', 'Base Unit', 'Unweighted base size']

tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}