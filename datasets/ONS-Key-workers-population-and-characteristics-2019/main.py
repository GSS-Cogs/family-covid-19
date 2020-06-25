#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # ONS Key workers reference tables 

from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import re

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]

def cellCont(cell):
    return re.findall(r"'([^']*)'", cell)[0]

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

def decimal(s):
    try:
        float(s)
        if float(s) >= 1:
            return True
        else:
            return False
    except ValueError:
        return False

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 


# In[2]:


scraper = Scraper(landingPage) 
scraper


# In[3]:


distribution = scraper.distributions[0]
display(distribution)


# In[4]:


trace = TransformTrace()

tabs = { tab: tab for tab in distribution.as_databaker() }

tidied_sheets = []

datasetTitle = 'ONS Key Workers Reference Tables'
link = distribution.downloadURL

with open('info.json') as info:
    data = info.read()

infoData = json.loads(data)

infoData['transform']['transformStage'] = {}

for tab in tabs:

    if not tab.name.lower() in ['contents', 'notes', 'var dfn', 'table 13', 'table 15']:#ignore tab 13/15 get it checked

        columns = ['Period', 'ONS Geography Code', 'Workforce Category', 'Workforce Breakdown', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, link)

        if right(tab.name.lower(), 2) in [' 8']:
            cell = tab.filter(contains_string('Table ')).shift(0, 4)
        else:
            cell = tab.filter(contains_string('Table ')).shift(0, 5)

        if right(tab.name.lower(), 3) in [' 1b', ' 7b', 'e 8', ' 9b', '10b', '11b', '12b', '14b', '16b']:
            remove = tab.filter(contains_string('Source:')).shift(UP).expand(RIGHT).expand(LEFT).expand(DOWN)
        elif right(tab.name.lower(), 7) in ['14b (2)']:
            remove = tab.filter(contains_string('Total')).expand(RIGHT).expand(LEFT).expand(DOWN)
        else:
            remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(LEFT).expand(DOWN)

        pivot = cellLoc(cell)

        if right(tab.name.lower(), 2) in [' 8']:
            period = cell.shift(0, -3)
        else:
            period = cell.shift(0, -4)

        trace.Period('Period Range for Tab given at cell value: {}', var = cellLoc(period))  

        if right(tab.name.lower(), 2) in ['17']:
            region = tab.filter(contains_string('Category')).fill(RIGHT).is_not_blank()
        elif right(tab.name.lower(), 2) in ['18', '19']:
            region = cell.expand(DOWN).is_not_blank() - remove
        else:
            region = 'E92000001'

        if isinstance(region, str):
            trace.ONS_Geography_Code('Geo-Code for tab is hard-coded as {}', var = region)
        else:
            trace.ONS_Geography_Code('Values found in range: {}', var = excelRange(region))      

        if right(tab.name.lower(), 2) in [' 8']:
            breakdown = 'Has Dependant Child(s)'
        elif right(tab.name.lower(), 2) in ['17', '18', '19']:
            breakdown = 'Key Workers'
        elif right(tab.name.lower(), 3) in [' 1a']:
            breakdown = 'N/A'
        else:
            breakdown = tab.filter(contains_string('Category')).fill(RIGHT).is_not_blank()

        if isinstance(breakdown, str):
            trace.Workforce_Breakdown('Workforce Breakdown for tab is hard-coded as {}', var = breakdown)
        else:
            trace.Workforce_Breakdown('Values found in range: {}', var = excelRange(breakdown))  

        if right(tab.name.lower(), 2) in ['18']:
            category = tab.filter('City Region').fill(RIGHT).is_not_blank()
        elif right(tab.name.lower(), 2) in ['19']:
            category = tab.filter('Local Authority').fill(RIGHT).is_not_blank()
        else:
            category = cell.expand(DOWN).is_not_blank() - remove

        trace.Workforce_Category('Values found in range: {}', var = excelRange(category))  

        if right(tab.name.lower(), 3) in [' 2a', ' 2b', ' 17']:
            observations = tab.filter('pop.').fill(DOWN).is_not_blank() - remove
        else:
            observations = tab.filter('population').fill(DOWN).is_not_blank() - remove

        measureType = 'Count'

        unit = 'Person'

        trace.Measure_Type('Hardcoded value as: {}', var =  measureType)

        trace.Unit('Hardcoded value as: {}',var = unit) 

        if '(' in tab.name:
            title = cellCont(str(tab.filter(contains_string(str(tab.name[:-4])))))
        else:
            title = cellCont(str(tab.filter(contains_string(str(tab.name)))))

        columnInfo = {'Period' : trace.Period.var,
                      'ONS Geography Code' : trace.ONS_Geography_Code.var,
                      'Workforce Category' : trace.Workforce_Category.var,
                      'Workforce Breakdown' : trace.Workforce_Breakdown.var,
                      'Measure Type' : trace.Measure_Type.var,
                      'Unit' : trace.Unit.var}

        dicti = {'name' : tab.name, 
                 'title' : title, 
                 'columns' : columnInfo}
        
        infoData['transform']['transformStage'][tab.name] = dicti

        with open('infoTest.json', 'w') as info:
            info.write(json.dumps(infoData, indent=4))

        if right(tab.name.lower(), 3) in [' 1a', 'e 8']:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDimConst('ONS Geography Code', region),
                    HDim(category, 'Workforce Category', DIRECTLY, LEFT),
                    HDimConst('Workforce Breakdown', breakdown),
                    HDimConst('Tab', tab.name),
                    HDimConst('Measure Type', measureType), 
                    HDimConst('Unit', unit) 
            ]
        elif right(tab.name.lower(), 2) in ['17']:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(region, 'ONS Geography Code', CLOSEST, LEFT),
                    HDim(category, 'Workforce Category', DIRECTLY, LEFT),
                    HDimConst('Workforce Breakdown', breakdown),
                    HDimConst('Tab', tab.name),
                    HDimConst('Measure Type', measureType), 
                    HDimConst('Unit', unit) 
            ]
        elif right(tab.name.lower(), 2) in ['18', '19']:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(region, 'ONS Geography Code', DIRECTLY, LEFT),
                    HDim(category, 'Workforce Category', CLOSEST, LEFT),
                    HDimConst('Workforce Breakdown', breakdown),
                    HDimConst('Tab', tab.name),
                    HDimConst('Measure Type', measureType), 
                    HDimConst('Unit', unit) 
            ]
        else:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDimConst('ONS Geography Code', region),
                    HDim(category, 'Workforce Category', DIRECTLY, LEFT),
                    HDim(breakdown, 'Workforce Breakdown', CLOSEST, LEFT),
                    HDimConst('Tab', tab.name),
                    HDimConst('Measure Type', measureType), 
                    HDimConst('Unit', unit) 
            ]
            
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store("keyWorkers", tidy_sheet.topandas())

    else:
        continue


# In[5]:


pd.set_option('display.float_format', lambda x: '%.0f' % x)

df = trace.combine_and_trace(datasetTitle, "keyWorkers").fillna('')

df = df.reset_index(drop=True)

df['Period'] = df.apply(lambda x: x['Period'].replace('United Kingdom, ', '') if 'United Kingdom, ' in x['Period'] else x['Period'], axis = 1)

df = df.replace({'DATAMARKER' : {
    '-' : 'Supressed due to small sample size'}})

df['Workforce Breakdown'] = df.apply(lambda x: str(x['Workforce Breakdown']) + ' aged under 4' if 'Table 9' in x['Tab'] else x['Workforce Breakdown'], axis = 1)

df['Workforce Breakdown'] = df.apply(lambda x: str(x['Workforce Breakdown']) + ' aged under 15' if 'Table 10' in x['Tab'] else x['Workforce Breakdown'], axis = 1)

df['Workforce Breakdown'] = df.apply(lambda x: 'Travel to work via ' + str(x['Workforce Breakdown']) if 'Table 14a' in x['Tab'] else x['Workforce Breakdown'], axis = 1)

df['Workforce Breakdown'] = df.apply(lambda x: 'Travel to work via ' + str(x['Workforce Breakdown']) if 'Table 14b' in x['Tab'] else x['Workforce Breakdown'], axis = 1)

df = df.drop(['Tab'], axis = 1)

df = df[['Period', 'ONS Geography Code', 'Workforce Category', 'Workforce Breakdown', 'Measure Type', 'Unit', 'OBS', 'DATAMARKER']]

df


# In[6]:


notes = """
All counts are individually rounded to the nearest thousand. Totals may not add exactly due to this rounding.
The definition of disability used is consistent with the core definition of disability under the Equality Act 2010. A person is considered to be disabled if they self-report a physical or mental health condition or illness lasting or expecting to last 12 months or more which reduces their ability to carry out day-to-day activities.
Respondents who did not provide disability status have been excluded.
"""


# In[7]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[8]:


for column in df:
    if column in ('Workforce Breakdown', 'Workforce Category'):
        df[column] = df[column].map(lambda x: pathify(x))


# In[9]:


out = Path('out')
out.mkdir(exist_ok=True)

title = pathify(datasetTitle)

scraper.dataset.comment = notes

import os

df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()

df

