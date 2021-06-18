# -*- coding: utf-8 -*-
# # ONS-Deaths-involving-COVID-19-UK

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

tabs_name = ['Table 1', 'Table 2', 'Table 3', 'Table 4']
tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}

if len(set(tabs_name)-{x.name for x in tabs}) != 0:
    raise ValueError(f'Aborting. A tab named {set(tabs_name)-{x.name for x in tabs}} required but not found')


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
    if tab.name == 'Table 1':
        columns = ['Period', 'Country', 'Persons', 'Males', 'Females', 'Measurement', 'Rate', 'Lower 95 Percent CI',
                   'Upper 95 Percent CI', 'Percentage of all deaths', 'Difference between 2020 and average',
                   'Percentage difference', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        period = '2020-03-01T00:00:00/P2M'
        trace.Period('Hardcoded as {}', var=period)

        country = tab.excel_ref('A7:A25').is_not_blank()
        trace.Country('Defined from cell range: {}', var=excelRange(country))

        persons = tab.filter('Persons').is_not_blank()
        trace.Persons('Defined from cell value: {}', var=cellLoc(persons))

        males = tab.filter('Males').is_not_blank()
        trace.Males('Defined from cell value: {}', var=cellLoc(males))

        females = tab.filter('Females').is_not_blank()
        trace.Females('Defined from cell value: {}', var=cellLoc(females))

        measurement = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
        trace.Measurement('Defined from cell range: {}', var=excelRange(measurement))

        rate = tab.filter('Rate').expand(DOWN).is_not_blank()
        trace.Rate('Defined from cell range: {}', var=excelRange(rate))

        percentage_all_deaths = tab.filter('Percentage of all deaths').expand(DOWN).is_not_blank()
        trace.Percentage_of_all_deaths('Defined from cell range: {}', var=excelRange(percentage_all_deaths))

        lower_95_percent_ci = tab.filter('Lower 95% CI').expand(DOWN).is_not_blank()
        trace.Lower_95_Percent_CI('Defined from cell range: {}', var=excelRange(lower_95_percent_ci))

        upper_95_percent_ci = tab.filter('Upper 95% CI').expand(DOWN).is_not_blank()
        trace.Upper_95_Percent_CI('Defined from cell range: {}', var=excelRange(upper_95_percent_ci))

        percentage_all_deaths = tab.filter('Percentage of all deaths').expand(DOWN).is_not_blank()
        trace.Percentage_of_all_deaths('Defined from cell range: {}', var=excelRange(percentage_all_deaths))

        difference_2020_and_average = tab.filter('Difference between 2020 and average').expand(DOWN).is_not_blank()
        trace.Difference_between_2020_and_average('Defined from cell range: {}',
                                                  var=excelRange(difference_2020_and_average))

        percentage_difference = tab.filter('Percentage difference').expand(DOWN).is_not_blank()
        trace.Percentage_difference('Defined from cell range: {}', var=excelRange(percentage_difference))

        measure_type = measurement
        trace.Measure_Type('Defined from cell range: {}', var=excelRange(measure_type))

        unit = 'Number of deaths'
        trace.Unit('Hardcoded as {}', var=unit)

        observations = tab.filter('Number of deaths').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(country, 'Country', DIRECTLY, LEFT),
            HDim(persons, 'Persons', CLOSEST, ABOVE),
            HDim(males, 'Males', CLOSEST, ABOVE),
            HDim(females, 'Females', CLOSEST, ABOVE),
            HDim(measurement, 'Measurement', DIRECTLY, ABOVE),
            HDim(rate, 'Rate', DIRECTLY, RIGHT),
            HDim(lower_95_percent_ci, 'Lower 95 Percent CI', DIRECTLY, RIGHT),
            HDim(upper_95_percent_ci, 'Upper 95 Percent CI', DIRECTLY, RIGHT),
            HDim(percentage_all_deaths, 'Percentage of all deaths', DIRECTLY, RIGHT),
            HDim(difference_2020_and_average, 'Difference between 2020 and average', DIRECTLY, RIGHT),
            HDim(percentage_difference, 'Percentage difference', DIRECTLY, RIGHT),
            HDim(measure_type, 'Measure Type', DIRECTLY, ABOVE),
            HDimConst('Unit', unit),
            HDimConst('Period', period)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_1', tidy_sheet.topandas())
