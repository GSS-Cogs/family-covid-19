# -*- coding: utf-8 -*-
# # ONS-Coronavirus-and-shielding-of-clinically-extremely-vulnerable-people-in-England

# +
import pandas as pd
from gssutils import *
import json
import string

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


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]


def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def excelRange(bag):
    xvalues = []
    yvalues = []
    for cell in bag:
        coordinate = cellLoc(cell)
        xvalues.append(''.join([i for i in coordinate if not i.isdigit()]))
        yvalues.append(int(''.join([i for i in coordinate if i.isdigit()])))
    high = 0
    low = 0
    for i in xvalues:
        if col2num(i) >= high:
            high = col2num(i)
        if low == 0:
            low = col2num(i)
        elif col2num(i) < low:
            low = col2num(i)
        highx = colnum_string(high)
        lowx = colnum_string(low)
    highy = str(max(yvalues))
    lowy = str(min(yvalues))
    return '{' + lowx + lowy + '-' + highx + highy + '}'


# Transform process
for tab in tabs:
    print(tab.name)
    if tab.name == 'Table 1.1':
        columns = ['Period', 'Title', 'Target', 'Age Group', 'Percentage', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        period = tab.excel_ref('A3').is_not_blank()
        trace.Period('Defined from cell value: {}', var=cellLoc(period))

        title = tab.excel_ref('A2').is_not_blank()
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        target = tab.excel_ref('A1').is_not_blank()
        trace.Target('Defined from cell value: {}', var=cellLoc(target))

        age_group = tab.excel_ref('A6:A15').is_not_blank()
        trace.Age_Group('Defined from cell range: {}', var=excelRange(age_group))

        percentage = tab.filter('Percentage').expand(DOWN).is_not_blank()
        trace.Percentage('Defined from cell range: {}', var=excelRange(percentage))

        measure_type = 'Number of those advised to shield, by age'
        trace.Measure_Type('Hardcoded as {}', var=measure_type)

        unit = 'Estimate in thousands'
        trace.Unit('Hardcoded as {}', var=unit)

        observations = tab.filter('Estimate in thousands').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(period, 'Period', CLOSEST, ABOVE),
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(target, 'Target', CLOSEST, ABOVE),
            HDim(age_group, 'Age Group', DIRECTLY, LEFT),
            HDim(percentage, 'Percentage', DIRECTLY, RIGHT),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]