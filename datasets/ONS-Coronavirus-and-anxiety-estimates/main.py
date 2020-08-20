#!/usr/bin/env python
# coding: utf-8

# In[125]:


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
from datetime import date

def twoDates(startMonth, startDay, endMonth, endDate, year = 2020):
    d0 = date(year, startMonth, startDay)
    d1 = date(year, endMonth, endDate)
    delta = d1 - d0
    print(delta.days)


# In[126]:


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[127]:


scraper = Scraper(landingPage)
scraper


# In[128]:


distribution = scraper.distributions[0]
display(distribution)


# In[129]:


tabs = { tab: tab for tab in distribution.as_databaker() if tab.name != 'Contents' }
for i in tabs:
    print(i.name)


# In[130]:


trace = TransformTrace()

tidied_sheets = []

datasetTitle = distribution.title
link = distribution.downloadURL

for tab in tabs:

    print(tab.name)

    columns = ['Period', 'Loneliness', 'Sex', 'Marital Status', 'Feeling Safe', 'Work Affected', 'Disability', 'Lower CI', 'Upper CI', 'Measure Type', 'Unit']
    trace.start(datasetTitle, tab, columns, link)

    pivot = tab.filter('95% confidence intervals')

    remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(DOWN)

    period = pivot.shift(-1, 3).expand(DOWN).is_not_blank() - remove
    trace.Period('Values given at cell range: {}', var = excelRange(period))

    if tab.name in ['Loneliness']:
        loneliness = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Loneliness('Values given at cell range: {}', var = excelRange(loneliness))
        sex = 'T'
        trace.Sex('Hardcoded for Tab as: {}', var = sex)
        maritalStatus = 'All'
        trace.Marital_Status('Hardcoded for Tab as: {}', var = maritalStatus)
        feelingSafe = 'All'
        trace.Feeling_Safe('Hardcoded for Tab as: {}', var = feelingSafe)
        workAffected = 'All'
        trace.Work_Affected('Hardcoded for Tab as: {}', var = workAffected)
        disability = 'All'
        trace.Disability('Hardcoded for Tab as: {}', var = disability)
    elif tab.name in ['Sex']:
        loneliness = 'All'
        trace.Loneliness('Hardcoded for Tab as: {}', var = loneliness)
        sex = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Sex('Values given at cell range: {}', var = excelRange(sex))
        maritalStatus = 'All'
        trace.Marital_Status('Hardcoded for Tab as: {}', var = maritalStatus)
        feelingSafe = 'All'
        trace.Feeling_Safe('Hardcoded for Tab as: {}', var = feelingSafe)
        workAffected = 'All'
        trace.Work_Affected('Hardcoded for Tab as: {}', var = workAffected)
        disability = 'All'
        trace.Disability('Hardcoded for Tab as: {}', var = disability)
    elif tab.name in ['Marital Status']:
        loneliness = 'All'
        trace.Loneliness('Hardcoded for Tab as: {}', var = loneliness)
        sex = 'T'
        trace.Sex('Hardcoded for Tab as: {}', var = sex)
        maritalStatus = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Marital_Status('Values given at cell range: {}', var = excelRange(maritalStatus))
        feelingSafe = 'All'
        trace.Feeling_Safe('Hardcoded for Tab as: {}', var = feelingSafe)
        workAffected = 'All'
        trace.Work_Affected('Hardcoded for Tab as: {}', var = workAffected)
        disability = 'All'
        trace.Disability('Hardcoded for Tab as: {}', var = disability)
    elif tab.name in ['Feeling safe']:
        loneliness = 'All'
        trace.Loneliness('Hardcoded for Tab as: {}', var = loneliness)
        sex = 'T'
        trace.Sex('Hardcoded for Tab as: {}', var = sex)
        maritalStatus = 'All'
        trace.Marital_Status('Hardcoded for Tab as: {}', var = maritalStatus)
        feelingSafe = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Feeling_Safe('Values given at cell range: {}', var = excelRange(feelingSafe))
        workAffected = 'All'
        trace.Work_Affected('Hardcoded for Tab as: {}', var = workAffected)
        disability = 'All'
        trace.Disability('Hardcoded for Tab as: {}', var = disability)
    elif tab.name in ['Work affected']:
        loneliness = 'All'
        trace.Loneliness('Hardcoded for Tab as: {}', var = loneliness)
        sex = 'T'
        trace.Sex('Hardcoded for Tab as: {}', var = sex)
        maritalStatus = 'All'
        trace.Marital_Status('Hardcoded for Tab as: {}', var = maritalStatus)
        feelingSafe = 'All'
        trace.Feeling_Safe('Hardcoded for Tab as: {}', var = feelingSafe)
        workAffected = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Work_Affected('Values given at cell range: {}', var = excelRange(workAffected))
        disability = 'All'
        trace.Disability('Hardcoded for Tab as: {}', var = disability)
    elif tab.name in ['Disability']:
        loneliness = 'All'
        trace.Loneliness('Hardcoded for Tab as: {}', var = loneliness)
        sex = 'T'
        trace.Sex('Hardcoded for Tab as: {}', var = sex)
        maritalStatus = 'All'
        trace.Marital_Status('Hardcoded for Tab as: {}', var = maritalStatus)
        feelingSafe = 'All'
        trace.Feeling_Safe('Hardcoded for Tab as: {}', var = feelingSafe)
        workAffected = 'All'
        trace.Work_Affected('Hardcoded for Tab as: {}', var = workAffected)
        disability = pivot.shift(DOWN).expand(RIGHT).is_not_blank()
        trace.Disability('Values given at cell range: {}', var = excelRange(disability))

    upper = tab.filter('Upper Interval').fill(DOWN).is_not_blank() - remove
    trace.Upper_CI('Values given at cell range: {}', var = excelRange(upper))

    lower = tab.filter('Lower Interval').fill(DOWN).is_not_blank() - remove
    trace.Lower_CI('Values given at cell range: {}', var = excelRange(lower))

    measure_type= 'Anxiety'
    trace.Measure_Type('Hardcoded as: {}', var = measure_type)

    unit = 'Rating Scale'
    trace.Unit('Hardcoded as: {}', var = unit)

    observations = tab.filter('Mean average').fill(DOWN).is_not_blank() - remove

    tabTitle = tab.filter(contains_string('Average anxiety ratings'))
    print(tabTitle)

    if tab.name in ['Loneliness']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(loneliness, 'Loneliness', CLOSEST, LEFT),
                HDimConst('Sex', sex),
                HDimConst('Marital Status', maritalStatus),
                HDimConst('Feeling Safe', feelingSafe),
                HDimConst('Work Affected', workAffected),
                HDimConst('Disability', disability),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]
    elif tab.name in ['Sex']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Loneliness', loneliness),
                HDim(sex, 'Sex', CLOSEST, LEFT),
                HDimConst('Marital Status', maritalStatus),
                HDimConst('Feeling Safe', feelingSafe),
                HDimConst('Work Affected', workAffected),
                HDimConst('Disability', disability),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]
    elif tab.name in ['Marital Status']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Loneliness', loneliness),
                HDimConst('Sex', sex),
                HDim(maritalStatus, 'Marital Status', CLOSEST, LEFT),
                HDimConst('Feeling Safe', feelingSafe),
                HDimConst('Work Affected', workAffected),
                HDimConst('Disability', disability),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]
    elif tab.name in ['Feeling safe']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Loneliness', loneliness),
                HDimConst('Sex', sex),
                HDimConst('Marital Status', maritalStatus),
                HDim(feelingSafe, 'Feeling Safe', CLOSEST, LEFT),
                HDimConst('Work Affected', workAffected),
                HDimConst('Disability', disability),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]
    elif tab.name in ['Work affected']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Loneliness', loneliness),
                HDimConst('Sex', sex),
                HDimConst('Marital Status', maritalStatus),
                HDimConst('Feeling Safe', feelingSafe),
                HDim(workAffected, 'Work Affected', CLOSEST, LEFT),
                HDimConst('Disability', disability),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]
    elif tab.name in ['Disability']:
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Loneliness', loneliness),
                HDimConst('Sex', sex),
                HDimConst('Marital Status', maritalStatus),
                HDimConst('Feeling Safe', feelingSafe),
                HDimConst('Work Affected', workAffected),
                HDim(disability, 'Disability', CLOSEST, LEFT),
                HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit)
        ]

    print(period.table)

    tidy_sheet = ConversionSegment(tab, dimensions, observations)

    trace.with_preview(tidy_sheet)

    infoTransform(tab.name, cellCont(str(tabTitle)), columns)

    trace.store('anxiety_estimates', tidy_sheet.topandas())


# In[131]:


out = Path('out')
out.mkdir(exist_ok=True)

df = trace.combine_and_trace(datasetTitle, 'anxiety_estimates').fillna('')

df = df.reset_index(drop=True)

df = df.rename(columns={'OBS' : 'Value'})

df['Opinions and Lifestyle Survey'] = df.apply(lambda x: left(x['Period'], 10), axis = 1)

df['Period'] = df.apply(lambda x: str(x['Period']).strip(), axis = 1)

df = df.replace({'Period' : {
        'OPN Lite 1 (20th Mar – 29th Mar)' : 'gregorian-interval/2020-03-20T00:00:00/P9D',
        'OPN Lite 2 (27th Mar – 5th Apr)' : 'gregorian-interval/2020-03-27T00:00:00/P9D',
        'OPN Lite 3 (3rd Apr – 12th Apr)' : 'gregorian-interval/2020-04-03T00:00:00/P9D',
        'OPN Lite 4 (9th Apr – 19th Apr)' : 'gregorian-interval/2020-04-09T00:00:00/P10D',
        'OPN Lite 5 (17th Apr – 26th Apr)' : 'gregorian-interval/2020-04-17T00:00:00/P9D',
        'OPN Lite 6 (24th Apr – 3rd May)' : 'gregorian-interval/2020-04-24T00:00:00/P9D',
        'OPN Lite 7 (30th Apr - 10th May)' : 'gregorian-interval/2020-04-30T00:00:00/P11D'},
                'Sex' : {
        'Male' : 'M',
        'Female' : 'F'}})

df = df[['Period', 'Loneliness', 'Sex', 'Marital Status', 'Feeling Safe', 'Work Affected', 'Disability', 'Value', 'Lower CI', 'Upper CI', 'Measure Type', 'Unit']]

for column in df:
    if column in ('Period', 'Loneliness', 'Sex', 'Marital Status', 'Feeling Safe', 'Work Affected', 'Disability', 'Measure Type', 'Unit'):
        df[column] = df[column].map(lambda x: pathify(x))

df.drop_duplicates().to_csv(out / 'observations.csv', index = False)


# In[132]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[133]:


notes = """
Respondents were asked “Overall, how anxious did you feel yesterday?” and answered on a scale of 0 to 10, where 0 is “not at all” and 10 is “completely”.
Broken down by "How often do you feel lonely?", Gender, Marital Status, "How safe or unsafe do you feel in your home since the Coronavirus (COVID-19) outbreak?", Whether their work is affected, and Disability.
Comparisons must be made with caution as these estimates are provided from a sample survey. As such, confidence intervals are produced to present the sampling variability which should be taken into account when assessing change, as true differences may not exist.
"""

infoNotes(notes)

trace.output()

df

