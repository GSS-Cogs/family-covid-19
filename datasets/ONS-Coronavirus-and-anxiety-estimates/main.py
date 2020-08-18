#!/usr/bin/env python
# coding: utf-8

# In[321]:


from gssutils import *
import pandas as pd
import json
import os
import string
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

def infoTransform(tabName, tabTitle, tabColumns):

    dictList = []

    with open('info.json') as info:
        data = info.read()

    infoData = json.loads(data)

    columnInfo = {}

    for i in tabColumns:
        underI = i.replace(' ', '_')
        columnInfo[i] = getattr(getattr(trace, underI), 'var')

    dicti = {'name' : tabName,
             'title' : tabTitle,
             'columns' : columnInfo}

    if infoData.get('transform').get('transformStage') == None:
        infoData['transform']['transformStage'] = []
        dictList.append(dicti)
    else:
        dictList = infoData['transform']['transformStage']
        index = next((index for (index, d) in enumerate(dictList) if d["name"] == tabName), None)
        if index is None :
            dictList.append(dicti)
        else:
            dictList[index] = dicti

    infoData['transform']['transformStage'] = dictList

    with open('info.json', 'w') as info:
        info.write(json.dumps(infoData, indent=4).replace('null', '"Not Applicable"'))

def infoComments(tabName, tabColumns):

    with open('info.json') as info:
        data = info.read()

    infoData = json.loads(data)

    columnInfo = {}

    for i in tabColumns:
        comments = []
        underI = i.replace(' ', '_')
        for j in getattr(getattr(trace, underI), 'comments'):
            if j == []:
                continue
            else:
                comments.append(':'.join(str(j).split(':', 3)[3:])[:-2].strip().lstrip('\"').rstrip('\"'))
        columnInfo[i] = comments

    columnInfo = {key:val for key, val in columnInfo.items() if val != ""}
    columnInfo = {key:val for key, val in columnInfo.items() if val != []}

    dicti = {'name' : tabName,
             'columns' : columnInfo}

    dictList = infoData['transform']['transformStage']
    index = next((index for (index, d) in enumerate(dictList) if d["name"] == tabName), None)
    if index is None :
        print('Tab not found in Info.json')
    else:
        dictList[index]['postTransformNotes'] = dicti

    with open('info.json', 'w') as info:
        info.write(json.dumps(infoData, indent=4).replace('null', '"Not Applicable"'))

def infoNotes(notes):

    with open('info.json') as info:
        data = info.read()

    infoData = json.loads(data)

    infoData['transform']['Stage One Notes'] = notes

    with open('info.json', 'w') as info:
        info.write(json.dumps(infoData, indent=4).replace('null', '"Not Applicable"'))


# In[322]:


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[323]:


scraper = Scraper(landingPage)
scraper


# In[324]:


distribution = scraper.distributions[0]
display(distribution)


# In[325]:


tabs = { tab: tab for tab in distribution.as_databaker() if tab.name != 'Contents' }
for i in tabs:
    print(i.name)


# In[326]:


trace = TransformTrace()

tidied_sheets = []

datasetTitle = distribution.title
link = distribution.downloadURL

for tab in tabs:

    columns = ['Period', 'Breakdown Category', 'Breakdown Response', 'Sample Size', 'Lower CI', 'Upper CI', 'Value', 'Measure Type', 'Unit']
    trace.start(datasetTitle, tab, columns, link)

    pivot = tab.filter('95% confidence intervals')

    remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(DOWN)

    period = pivot.shift(-1, 3).expand(DOWN).is_not_blank() - remove
    trace.Period('Values given at cell range: {}', var = excelRange(period))

    breakdown = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
    trace.Breakdown_Response('Values given at cell range: {}', var = excelRange(breakdown))

    upper = tab.filter('Upper Interval').fill(DOWN).is_not_blank() - remove
    trace.Upper_CI('Values given at cell range: {}', var = excelRange(upper))

    lower = tab.filter('Lower Interval').fill(DOWN).is_not_blank() - remove
    trace.Lower_CI('Values given at cell range: {}', var = excelRange(lower))

    measure_type= 'Average Anxiety'
    trace.Measure_Type('Hardcoded as: {}', var = measure_type)

    unit = '0 to 10 Scale'
    trace.Unit('Hardcoded as: {}', var = unit)

    breakdownCategory = tab.name
    trace.Breakdown_Category('Values taken from Tab Names: {}', var = breakdownCategory)

    observations = tab.filter('Mean average').fill(DOWN).is_not_blank() - remove

    tabTitle = tab.filter(contains_string('Average anxiety ratings'))

    dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Breakdown Category', breakdownCategory),
                HDim(breakdown, 'Breakdown Response', CLOSEST, LEFT),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
    ]

    tidy_sheet = ConversionSegment(tab, dimensions, observations)

    main = tidy_sheet.topandas()

    main["Breakdown Response"] = main["Breakdown Response"].str.lower()

    indexNames = main[ main['Lower CI'] == 'x' ].index
    main.drop(indexNames, inplace = True)

    pivot = tab.filter('Sample Size')

    period = tab.filter('95% confidence intervals').shift(-1, 3).expand(DOWN).is_not_blank() - remove

    breakdown = pivot.shift(DOWN).expand(RIGHT).is_not_blank()

    observations = breakdown.fill(DOWN).is_not_blank() - remove
    trace.Sample_Size('Values taken from: {}', excelRange(observations))

    dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(breakdown, 'Breakdown Response', CLOSEST, LEFT)
    ]

    tidy_sheet = ConversionSegment(tab, dimensions, observations)
    savepreviewhtml(tidy_sheet, fname="Preview.html")

    samples = tidy_sheet.topandas()

    samples = samples.rename(columns = {'OBS' : 'Sample Size'})

    samples["Breakdown Response"] = samples["Breakdown Response"].str.lower()

    samples = samples.replace({'Breakdown Response' : {
        'ocassionally' : 'occasionally',
        'not, work being affected' : 'not, my work is being affected',
        'work being affected' : 'my work is being affected'}})

    merged_left = pd.merge(left=main, right=samples, how='left', left_on=['Period', 'Breakdown Response'], right_on=['Period', 'Breakdown Response'])

    trace.with_preview(tidy_sheet)

    infoTransform(tab.name, cellCont(str(tabTitle)), columns)

    trace.store('anxiety_estimates', merged_left)


# In[327]:


out = Path('out')
out.mkdir(exist_ok=True)

df = trace.combine_and_trace(datasetTitle, 'anxiety_estimates').fillna('')

df = df.reset_index(drop=True)

df = df.rename(columns={'OBS' : 'Value'})

df = df[['Period', 'Breakdown Category', 'Breakdown Response', 'Sample Size', 'Lower CI', 'Upper CI', 'Value', 'Measure Type', 'Unit']]

for column in df:
    if column in ('Period', 'Breakdown Category', 'Breakdown Response', 'Measure Type', 'Unit'):
        df[column] = df[column].map(lambda x: pathify(x))

df.drop_duplicates().to_csv(out / 'observations.csv', index = False)


# In[328]:


notes = """
Respondents were asked “Overall, how anxious did you feel yesterday?” and answered on a scale of 0 to 10, where 0 is “not at all” and 10 is “completely”.
Broken down by "How often do you feel lonely?", Gender, Marital Status, "How safe or unsafe do you feel in your home since the Coronavirus (COVID-19) outbreak?", Whether their work is affected, and Disability.
Comparisons must be made with caution as these estimates are provided from a sample survey. As such, confidence intervals are produced to present the sampling variability which should be taken into account when assessing change, as true differences may not exist.
"""

infoNotes(notes)

trace.output()

df

