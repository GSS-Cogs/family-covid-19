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
        columns = ['Title', 'Period', 'Social Distance Ability', 'Odds Ratio', 'Lower Confidence Interval',
                   'Upper Confidence Interval', 'Positive Sample Count', 'Total Sample Count']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        period = tab.excel_ref('A10').expand(DOWN).is_not_blank() & tab.excel_ref('A16').expand(UP).is_not_blank()
        trace.Period('Defined from cell range: {}', var=excelRange(period))

        social_distance = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
        trace.Social_Distance_Ability('Defined from cell range: {}', var=excelRange(social_distance))

        odds_ratio = tab.filter('Odds Ratio').expand(DOWN).is_not_blank()
        trace.Odds_Ratio('Defined from cell range: {}', var=excelRange(odds_ratio))

        lower_confidence_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.Lower_Confidence_Interval('Defined from cell range: {}', var=excelRange(lower_confidence_interval))

        upper_confidence_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.Upper_Confidence_Interval('Defined from cell range: {}', var=excelRange(upper_confidence_interval))

        positive_sample_count = tab.filter('Number of people testing positive').expand(DOWN).is_not_blank()
        trace.Positive_Sample_Count('Defined from cell range: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people in sample').expand(DOWN).is_not_blank()
        trace.Total_Sample_Count('Defined from cell range: {}', var=excelRange(total_sample_count))

        observations = tab.excel_ref('B10').expand(DOWN).expand(RIGHT).is_not_blank()

        dimensions = [
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(social_distance, 'Social Distance Ability', CLOSEST, LEFT),
            HDim(odds_ratio, 'Odds Ratio', DIRECTLY, ABOVE),
            HDim(lower_confidence_interval, 'Lower Confidence Interval', DIRECTLY, ABOVE),
            HDim(upper_confidence_interval, 'Upper Confidence Interval', DIRECTLY, ABOVE),
            HDim(positive_sample_count, 'Positive Sample Count', DIRECTLY, ABOVE),
            HDim(total_sample_count, 'Total Sample Count', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'dataframe_table_{tab.name}', tidy_sheet.topandas())

    if tab.name == '1b':
        columns = ['Title', 'Period', 'Mode of Travel', 'Odds Ratio', 'Lower Confidence Interval',
                   'Upper Confidence Interval', 'Positive Sample Count', 'Total Sample Count']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        period = tab.excel_ref('A10').expand(DOWN).is_not_blank() & tab.excel_ref('A16').expand(UP).is_not_blank()
        trace.Period('Defined from cell range: {}', var=excelRange(period))

        mode_travel = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
        trace.Mode_of_Travel('Defined from cell range: {}', var=excelRange(mode_travel))

        odds_ratio = tab.filter('Odds Ratio').expand(DOWN).is_not_blank()
        trace.Odds_Ratio('Defined from cell range: {}', var=excelRange(odds_ratio))

        lower_confidence_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.Lower_Confidence_Interval('Defined from cell range: {}', var=excelRange(lower_confidence_interval))

        upper_confidence_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.Upper_Confidence_Interval('Defined from cell range: {}', var=excelRange(upper_confidence_interval))

        positive_sample_count = tab.filter('Number of people testing positive').expand(DOWN).is_not_blank()
        trace.Positive_Sample_Count('Defined from cell range: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people in sample').expand(DOWN).is_not_blank()
        trace.Total_Sample_Count('Defined from cell range: {}', var=excelRange(total_sample_count))

        observations = tab.excel_ref('B10').expand(DOWN).expand(RIGHT).is_not_blank()

        dimensions = [
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(mode_travel, 'Mode of Travel', CLOSEST, LEFT),
            HDim(odds_ratio, 'Odds Ratio', DIRECTLY, ABOVE),
            HDim(lower_confidence_interval, 'Lower Confidence Interval', DIRECTLY, ABOVE),
            HDim(upper_confidence_interval, 'Upper Confidence Interval', DIRECTLY, ABOVE),
            HDim(positive_sample_count, 'Positive Sample Count', DIRECTLY, ABOVE),
            HDim(total_sample_count, 'Total Sample Count', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'dataframe_table_{tab.name}', tidy_sheet.topandas())
