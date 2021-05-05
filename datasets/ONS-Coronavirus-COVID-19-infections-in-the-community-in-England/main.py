# -*- coding: utf-8 -*-
# # ONS-Coronavirus-COVID-19-infections-in-the-community-in-England

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

dist = scraper.distribution(latest = True, mediaType = Excel)
datasetTitle = info['title']
dist
datasetTitle

tabs_name = ['1a', '1b', '2a', '2b', '2c', '2d']

if len(set(tabs_name)-{x.name for x in tabs}) != 0:
    raise ValueError(f'Aborting. A tab named {set(tabs_name)-{x.name for x in tabs}} required but not found')
tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}


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
    if tab.name == '1a':
        columns = ['distancing', 'odds ratio', 'lower interval', 'upper interval', 'positive sample count',
                   'total sample count', 'period', 'title']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.title('Defined from cell value: {}', var=cellLoc(title))

        period = tab.excel_ref('A10').expand(DOWN).is_not_blank() & tab.excel_ref('A16').expand(UP).is_not_blank()
        trace.period('Defined from cell range: {}', var=excelRange(period))

        odds_ratio = tab.filter('Odds Ratio').expand(DOWN).is_not_blank()
        trace.odds_ratio('Defined from cell value: {}', var=excelRange(odds_ratio))

        lower_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.lower_interval('Defined from cell value: {}', var=excelRange(lower_interval))

        upper_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.upper_interval('Defined from cell value: {}', var=excelRange(upper_interval))

        positive_sample_count = tab.filter('Number of people testing positive').expand(DOWN).is_not_blank()
        trace.positive_sample_count('Defined from cell value: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people in sample').expand(DOWN).is_not_blank()
        trace.total_sample_count('Defined from cell value: {}', var=excelRange(total_sample_count))

        distancing = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
        trace.distancing('Defined from cell range: {}', var = excelRange(distancing))

        observations = tab.excel_ref('B10').expand(DOWN).expand(RIGHT).is_not_blank()

        dimensions = [
            HDim(distancing, 'distancing', DIRECTLY, ABOVE),
            HDim(period, 'period', DIRECTLY, LEFT),
            HDim(odds_ratio, 'odds_ratio', DIRECTLY, ABOVE),
            HDim(lower_interval, 'lower_interval', DIRECTLY, ABOVE),
            HDim(upper_interval, 'upper_interval', DIRECTLY, ABOVE),
            HDim(positive_sample_count, 'positive_sample_count', DIRECTLY, ABOVE),
            HDim(total_sample_count, 'total_sample_count', DIRECTLY, ABOVE),
            HDimConst('title', title)
        ]
