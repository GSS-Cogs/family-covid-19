#!/usr/bin/env python
# coding: utf-8
# %%

# %%


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
def decimal(s):
    try:
        float(s)
        if float(s) >= 1:
            return False
        else:
            return True
    except ValueError:
        return True
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


# %%


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# %%
#scraper = Scraper(landingPage)
scraper = Scraper(seed="info.json")
scraper.dataset.title = 'ONS Coronavirus and Homeworking in the UK'
scraper


# %%
distribution = scraper.distributions[0]
display(distribution)


# %%


trace = TransformTrace()

tidied_sheets = []

datasetTitle = distribution.title
link = distribution.downloadURL

tabs = { tab: tab for tab in distribution.as_databaker() if tab.name in ['1', '2', '3']}

for tab in tabs:

    if tab.name in ['1', '2', '3']:

        columns = ['Period', 'Breakdown Category', 'Breakdown', 'Value', 'Marker', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, link)

        pivot = tab.filter('UK (%) NSA')

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(RIGHT).expand(DOWN)

        period = pivot.shift(DOWN)
        trace.Period("Values given at cell range: {}", var = excelRange(period))

        if tab.name in ['1']:
            breakdownCategory = 'Homeworkers worked hours in reference week'
        elif tab.name in ['2', '3']:
            breakdownCategory = cellCont(str(pivot.shift(-2, 1)))
        trace.Breakdown_Category("Hardcoded for tab as: {}", var = breakdownCategory)

        breakdown = pivot.shift(-2, 3).expand(DOWN).is_not_blank() - remove
        trace.Breakdown("Values given at cell range: {}", var = excelRange(breakdown))

        measureType = 'percentage'
        trace.Measure_Type('Hardcoded as: {}', var = measureType)

        unit = 'percent'
        trace.Unit('Hardcoded as: {}', var = unit)

        observations = breakdown.fill(RIGHT).is_not_blank()

        dimensions = [
                HDim(period, 'Period', DIRECTLY, ABOVE),
                HDimConst('Breakdown Category', breakdownCategory),
                HDim(breakdown, 'Breakdown', DIRECTLY, LEFT),
                HDimConst('Measure Type', measureType),
                HDimConst('Unit', unit)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        tabTitle = tab.filter('Contents').shift(1, 1)

        infoTransform(tab.name, cellCont(str(tabTitle)), columns)

        trace.store('Homeworking', tidy_sheet.topandas())


# %%


df = trace.combine_and_trace(datasetTitle, 'Homeworking').fillna('')

df = df.reset_index(drop=True)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

df['Period'] = df.apply(lambda x: 'April' if 'April' in x['Period'] else x['Period'], axis = 1)
trace.Period("Replace 'April(%)' with 'April'")

df['Breakdown'] = df.apply(lambda x: 'Ages ' + str(x['Breakdown']) if RepresentsInt(right(pathify(x['Breakdown']), 2)) == True else x['Breakdown'], axis = 1)
trace.Breakdown("Add 'Ages ' to numbered age value to make value clear")

df = df.rename(columns={'OBS' : 'Value',
                        'DATAMARKER' : 'Marker'})

df = df.replace({'Breakdown' : {
            'More hours than usual2' : 'worked More hours than usual',
            'Less hours than usual2' : 'worked Less hours than usual',
            'Same hours as usual2' : 'worked Same hours as usual',
            '1 Managers, Directors And Senior Officials' : 'Managers, Directors And Senior Officials',
            '2 Professional Occupations' : 'Professional Occupations',
            '3 Associate Professional And Technical Occupations' : 'Associate Professional And Technical Occupations',
            '4 Administrative And Secretarial Occupations' : 'Administrative And Secretarial Occupations',
            '5 Skilled Trades Occupations' : 'Skilled Trades Occupations',
            '6 Caring, Leisure And Other Service Occupations' : 'Caring, Leisure And Other Service Occupations',
            '7 Sales And Customer Service Occupations' : 'Sales And Customer Service Occupations',
            '8 Process, Plant And Machine Operatives' : 'Process, Plant And Machine Operatives',
            '9 Elementary Occupations' : 'Elementary Occupations',
            'Ethnic Minority3' : 'Ethnic Minority',
            'Ages 65+' : 'Ages 65 Plus'},
                 'Breakdown Category' : {
            'Proportion doing any work at home2' : 'Proportion doing any work at home',
            'Proportion doing any work at home due to COVID-192' : 'Proportion doing any work at home due to COVID-19'},
                 'DATAMARKER' : {
            '*' : 'Sample too small for reliable estimate'
                 }})
trace.Breakdown("Replace 'More hours than usual2' : 'worked More hours than usual'")
trace.Breakdown("Replace 'Less hours than usual2' : 'worked Less hours than usual'")
trace.Breakdown("Replace 'Same hours as usual2' : 'worked Same hours as usual'")
trace.Breakdown("Replace '1 Managers, Directors And Senior Officials' : 'Managers, Directors And Senior Officials'")
trace.Breakdown("Replace '2 Professional Occupations' : 'Professional Occupations'")
trace.Breakdown("Replace '3 Associate Professional And Technical Occupations' : 'Associate Professional And Technical Occupations'")
trace.Breakdown("Replace '4 Administrative And Secretarial Occupations' : 'Administrative And Secretarial Occupations'")
trace.Breakdown("Replace '5 Skilled Trades Occupations' : 'Skilled Trades Occupations'")
trace.Breakdown("Replace '6 Caring, Leisure And Other Service Occupations' : 'Caring, Leisure And Other Service Occupations'")
trace.Breakdown("Replace '7 Sales And Customer Service Occupations' : 'Sales And Customer Service Occupations'")
trace.Breakdown("Replace '8 Process, Plant And Machine Operatives' : 'Process, Plant And Machine Operatives'")
trace.Breakdown("Replace '9 Elementary Occupations' : 'Elementary Occupations'")
trace.Breakdown("Replace 'Ethnic Minority3' : 'Ethnic Minority'")
trace.Breakdown("Replace 'Ages 65+' : 'Ages 65 Plus'}")
trace.Breakdown_Category("Replace 'Proportion doing any work at home2' : 'Proportion doing any work at home'")
trace.Breakdown_Category("Replace 'Proportion doing any work at home due to COVID-192' : 'Proportion doing any work at home due to COVID-19'")
trace.Marker("Replace '*' : 'Sample too small for reliable estimate'")

for column in df:
    if column in ('Period', 'Breakdown Category', 'Breakdown', 'Marker', 'Measure Type', 'Unit'):
        df[column] = df[column].map(lambda x: pathify(x.strip()))

df = df[['Period', 'Breakdown Category', 'Breakdown', 'Value', 'Marker', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)

df.drop_duplicates().to_csv(out / 'observations.csv', index = False)

df


# %%


notes = """
A homeworker refers to a person who did any working from home in the reference week.
More, less and same hours are calculated based on a respondent's answer to both actual and usual hours worked in the reference week.
Homeworking rates are calculated as follows: 100*(number doing any work from home in the reference week)/(number of persons in employment).
Ethnic Minority includes all people stating their ethnicity as 'Mixed', 'Indian', 'Pakistani', 'Bangladeshi', 'Chinese', 'Black/African/Caribbean' or 'Other'.
Homeworking due to Covid-19 rates are calculated as follows: 100*(number stating their main reason for working from home was a reason related to Covid-19)/(number doing any work from home in the reference week).
"""

infoNotes(notes)

trace.output()

df

