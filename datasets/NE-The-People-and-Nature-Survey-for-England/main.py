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


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]


# Transform process
for tab in tabs:
    trace.start(datasetTitle, tab, columns, dist.downloadURL)
    question = tab.excel_ref('A1')
    trace.Question('Question details at cell value: {}', var=cellLoc(question))

    answer = tab.excel_ref('A4').expand(DOWN).is_not_blank()
    trace.Answer('Answer details at cell value: {}', var=cellLoc(answer))

    value_type = tab.excel_ref('B2').expand(RIGHT).is_not_blank()
    trace.Value_Type('Value Type details at cell value: {}', var=cellLoc(value_type))

    measure_type = 'Percentage'
    trace.Measure_Type('Hardcoded value as: Percentage')

    unit = 'Percent'
    trace.Unit('Hardcoded value as: Percent')

    period = tab.excel_ref('B1')
    trace.Period('Period details at cell value: {}', var=cellLoc(period))

    base_unit = tab.excel_ref('A2')
    trace.Base_Unit('Base Unit details at cell value: {}', var=cellLoc(base_unit))

    unweighted_base_size = tab.excel_ref('B3')
    trace.Unweighted_base_size('Unweighted base size details at cell value: {}', var=cellLoc(unweighted_base_size))

    observations = tab.excel_ref('B4').expand(DOWN).expand(RIGHT).is_not_blank()