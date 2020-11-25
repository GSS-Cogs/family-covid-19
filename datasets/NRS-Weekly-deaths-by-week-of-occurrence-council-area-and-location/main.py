#!/usr/bin/env python
# coding: utf-8

# In[79]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
# # NRS-Weekly-deaths-by-week-of-occurrence-council-area-and-location

from gssutils import *
import json
import re
import string
from dateutil.parser import parse

def right(s, amount):
    return s[-amount:]

def left(s, amount):
    return s[:amount]

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

cubes = Cubes("info.json")

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[80]:


scrape = Scraper(landingPage)
scrape


# In[81]:


scrape.distributions


# In[82]:


dist = scrape.distributions[0]
dist.title = "Weekly deaths by week of occurrence, council area and location"
display(dist)


# In[83]:


pd.set_option('display.float_format', lambda x: '%.2f' % x)

trace = TransformTrace()

tabs = { tab.name: tab for tab in dist.as_databaker() if tab.name.startswith('Data')}
list(tabs)

datasetTitle = info['title']
link = dist.downloadURL

tidied_sheets = {}

for name, tab in tabs.items():

    if 'data' == name.lower():

        columns = ['Period', 'Measurement', 'Gender', 'Values', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Crown Copyright 2020')).expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Data for weekly deaths"))

        period = 'year/2020'

        week_of_occurrence = cell.shift(0, 2).fill(DOWN).is_not_blank() - remove
        #trace.Period('Year to use with Period taken from cell range: {}', var = excelRange(year))

        council = week_of_occurrence.shift(RIGHT)
        #trace.Period('Quarter to use with Period taken from cell range: {}', var = excelRange(quarter))

        location_of_death = council.shift(RIGHT)
        #trace.Measurement('Temporary header name')
        #trace.Measurement('Measurement values found in cell range: {}', var = excelRange(measurement1))

        cause_of_death = location_of_death.shift(RIGHT)
        #trace.Gender('Observations adapted from values found in range: {}', var = excelRange(measurement2))

        observations = cause_of_death.shift(RIGHT)
        #trace.Values('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDimConst('Period', period),
        HDim(week_of_occurrence, 'Week of Occurrence', DIRECTLY, LEFT),
        HDim(council, 'Area', DIRECTLY, LEFT),
        HDim(location_of_death, 'Location of Death', DIRECTLY, LEFT),
        HDim(cause_of_death, 'Cause of Death', DIRECTLY, LEFT),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

tidy_sheet.topandas()


# In[84]:


out = Path('out')
out.mkdir(exist_ok=True)

tidied_tables = {}

for name in tabs:

    if name.lower() == 'data':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df = df.rename(columns={'OBS' : 'Values'})
        trace.Values("Rename 'OBS' column to 'Values'")

        df = df.replace({'Area' : {
            'Aberdeen City': 'S12000033',
            'Aberdeenshire' : 'S12000034',
            'Angus' : 'S12000041',
            'Argyll and Bute' : 'S12000035',
            'Ayrshire and Arran' : 'S08000015',
            'Borders' : 'S08000016',
            'City of Edinburgh' : 'S12000036',
            'Clackmannanshire' : 'S12000005',
            'Dumfries and Galloway' : 'S12000006',
            'Dundee City' : 'S12000042',
            'East Ayrshire' : 'S12000008',
            'East Dunbartonshire' : 'S12000045',
            'East Lothian' : 'S12000010',
            'East Renfrewshire' : 'S12000011',
            'Falkirk' : 'S12000014',
            'Fife' : 'S12000047',
            'Forth Valley ' : 'S08000019',
            'Glasgow City' : 'S12000049',
            'Greater Glasgow and Clyde ' : 'S08000031',
            'Highland' : 'S12000017',
            'Inverclyde' : 'S12000018',
            'Midlothian' : 'S12000019',
            'Moray' : 'S12000020',
            'Na h-Eileanan Siar' : 'S12000013',
            'North Ayrshire' : 'S12000021',
            'North Lanarkshire' : 'S12000050',
            'Orkney Islands' : 'S12000023',
            'Perth and Kinross' : 'S12000048',
            'Renfrewshire' : 'S12000038',
            'SCOTLAND' : 'S92000003',
            'Scottish Borders' : 'S12000026',
            'Shetland Islands' : 'S12000027',
            'South Ayrshire' : 'S12000028',
            'South Lanarkshire' : 'S12000029',
            'Stirling' : 'S12000030',
            'West Dunbartonshire' : 'S12000039',
            'West Lothian' : 'S12000040'}})

        df = df[['Area', 'Period', 'Week of Occurrence', 'Cause of Death', 'Values']]

        cubes.add_cube(scrape, df, dist.title)

        tidied_tables[name] = df


# In[85]:


for name in tidied_tables:
    print('Tab Name: ' +  name)
    print(tidied_tables[name])


# In[86]:


scrape.dataset.family = 'covid-19'
scrape.dataset.issued = parse('25 November 2020').date()

trace.render("spec_v1.html")
cubes.output_all()

