#!/usr/bin/env python
# coding: utf-8

# In[161]:


#!/usr/bin/env python
# coding: utf-8
# %%


# In[162]:



#!/usr/bin/env python
# coding: utf-8


# In[163]:



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
scrape = Scraper(landingPage)

dist = scrape.distributions[0]
dist.title = "Weekly deaths by week of occurrence, council area and location"
display(dist)


# In[164]:



pd.set_option('display.float_format', lambda x: '%.2f' % x)

trace = TransformTrace()

tabs = { tab.name: tab for tab in dist.as_databaker() if tab.name.startswith('Data')}
list(tabs)

datasetTitle = info['title']
link = dist.downloadURL

tidied_sheets = {}

for name, tab in tabs.items():

    if 'data' == name.lower():

        columns = ['Week of Occurrence', 'Area', 'Location of Death', 'Cause of Death', 'Value']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Crown Copyright 2020')).expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Data for weekly deaths"))

        week_of_occurrence = cell.shift(0, 2).fill(DOWN).is_not_blank() - remove
        trace.Week_of_Occurrence('Dimension found in cell range: {}', var = excelRange(week_of_occurrence))

        area = week_of_occurrence.shift(RIGHT)
        trace.Area('Dimension found in cell range: {}', var = excelRange(area))

        location_of_death = area.shift(RIGHT)
        trace.Location_of_Death('Dimension found in cell range: {}', var = excelRange(location_of_death))

        cause_of_death = location_of_death.shift(RIGHT)
        trace.Cause_of_Death('Dimension found in cell range: {}', var = excelRange(cause_of_death))

        observations = cause_of_death.shift(RIGHT)
        trace.Values('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDim(week_of_occurrence, 'Week of Occurrence', DIRECTLY, LEFT),
        HDim(area, 'Area', DIRECTLY, LEFT),
        HDim(location_of_death, 'Location of Death', DIRECTLY, LEFT),
        HDim(cause_of_death, 'Cause of Death', DIRECTLY, LEFT),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        trace.store(name, tidy_sheet.topandas())


# In[165]:



out = Path('out')
out.mkdir(exist_ok=True)

tidied_tables = {}

for name in tabs:

    if name.lower() == 'data':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df = df.rename(columns={'OBS' : 'Value'})
        trace.Values("Rename 'OBS' column to 'Value'")

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

        trace.Area("Convert to Council Area ONS Geography Codes")

        df['Week of Occurrence'] = df.apply(lambda x:  'week/2020-' + x['Week of Occurrence'], axis = 1)
        trace.Week_of_Occurrence("Add 'week/2020-' to Values")

        COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

        for col in df.columns.values.tolist():
            if col in COLUMNS_TO_NOT_PATHIFY:
                continue
            try:
                df[col] = df[col].apply(pathify)
            except Exception as err:
                raise Exception('Failed to pathify column "{}".'.format(col)) from err

        df = df[['Week of Occurrence', 'Area', 'Location of Death', 'Cause of Death', 'Value']]

        cubes.add_cube(scrape, df, dist.title)

        tidied_tables[name] = df


# In[166]:


scrape.dataset.family = 'covid-19'
scrape.dataset.issued = parse('25 November 2020').date()
scrape.dataset.comment = 'Weekly Covid-19 and Non-Covid-19 deaths by week of occurrence, council area and location'
scrape.dataset.description = """Weekly Covid-19 and Non-Covid-19 deaths by week of occurrence, council area and location
		This data is from user requests for ad-hoc analysis related to COVID-19 deaths data. As these data may be useful for others, we are making them available to download for any users of our data."""

trace.render("spec_v1.html")
cubes.output_all()


# In[167]:


tidied_tables['Data'].head(20)

