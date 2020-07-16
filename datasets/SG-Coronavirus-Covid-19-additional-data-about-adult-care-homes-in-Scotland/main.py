#!/usr/bin/env python
# coding: utf-8

# In[364]:


from gssutils import *
import pandas as pd
import json
import string
import re

def right(s, amount):
    return s[-amount:]

def left(s, amount):
    return s[:amount]

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def decimal(s):
    try:
        float(s)
        if float(s) >= 1:
            return False
        else:
            return True
    except ValueError:
        return True

def cellCont(cell):
    return re.findall(r"'([^']*)'", str(cell))[0]

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]

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

def dicti(tabName, tabTitle, tabColumns):
    columnInfo = {}

    for i in tabColumns:
        underI = i.replace(' ', '_')
        columnInfo[i] = getattr(getattr(trace, underI), 'var')

    dicti = {'name' : tabName,
             'title' : tabTitle,
             'columns' : columnInfo}

    return dicti

def dictiComment(tabName, tabTitle, tabColumns):
    columnInfo = {}

    for i in tabColumns:
        underI = i.replace(' ', '_')
        columnInfo[i] = re.findall('"([^"]*)"', str(getattr(getattr(trace, underI), 'comments')))

    dicti = {'name' : tabName,
             'columns' : columnInfo}

    return dicti


# In[365]:


scraper = Scraper(seed='info.json')
scraper.distributions[0].title = "Coronavirus (Covid-19): additional data about adult care homes in Scotland"
scraper


# In[366]:


distribution = scraper.distributions[0]
display(distribution)


# In[367]:


trace = TransformTrace()

tidied_sheets = {}

tabs = { tab: tab for tab in distribution.as_databaker() }

datasetTitle = scraper.distributions[0].title
link = distribution.downloadURL

dictiList = []

with open('info.json') as info:
    data = info.read()

infoData = json.loads(data)

infoData['transform']['transformStage'] = {}

for tab in tabs:

    if left(tab.name.lower(), 7) in ['table 1', 'table 2']:

        if tab.name.lower().startswith('table 1'):
            columns = ['Period','Region','Size of Care Home', 'Measure Type','Unit']
        else:
            columns = ['Period','Region','Sector', 'Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Notes:')).expand(DOWN).expand(UP).expand(RIGHT)

        cell = tab.filter('Date')

        period = cell.fill(DOWN).is_not_blank()
        trace.Period('Values found in range: {}', var = excelRange(period))

        breakdown = cell.fill(RIGHT).is_not_blank() - remove
        if tab.name.lower().startswith('table 1'):
            trace.Size_of_Care_Home('Values found in range: {}', var = excelRange(breakdown))
        else:
            trace.Sector('Values found in range: {}', var = excelRange(breakdown))

        measure = cell.shift(1, -1).expand(RIGHT).is_not_blank() - remove

        region = 'Scotland'
        trace.Region('Hardcoded as: {}', var = region)

        trace.Measure_Type('Hard Coded as: {}', var = 'Cumulative Count')

        trace.Unit('Hard Coded as: {}', var = 'Per 1000 Care Homes')

        tabTitle = tab.filter(contains_string('Table '))

        dictiList.append(dicti(tab.name, cellCont(tabTitle), columns))

        observations = breakdown.fill(DOWN)

        if tab.name.lower().startswith('table 1'):
            dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Region', region),
                HDim(breakdown, 'Size of Care Home', DIRECTLY, ABOVE),
                HDim(measure, 'Measure', CLOSEST, LEFT),
                HDimConst('Measure Type', 'Cumulative Count'),
                HDimConst('Unit', 'Per 1000 Care Homes')
                ]
        elif tab.name.lower().startswith('table 2'):
            dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Region', region),
                HDim(breakdown, 'Sector', DIRECTLY, ABOVE),
                HDim(measure, 'Measure', CLOSEST, LEFT),
                HDimConst('Measure Type', 'Cumulative Count'),
                HDimConst('Unit', 'Per 1000 Care Homes')
                ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())

    elif tab.name.lower().startswith('table 3'):

        columns = ['Period','Local Authority','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Notes:')).expand(DOWN).expand(UP).expand(RIGHT)

        cell = tab.filter('Local Authority')

        locAuth = cell.fill(DOWN).is_not_blank()
        trace.Local_Authority('Values found in range: {}', var = excelRange(locAuth))

        period = cell.fill(RIGHT).is_not_blank() - remove
        trace.Period('Values found in range: {}', var = excelRange(period))

        measure = cell.shift(1, -1).expand(RIGHT).is_not_blank() | tab.filter(contains_string('Cumulative %')) - remove

        trace.Measure_Type('Hard Coded as: {}', var = 'Cumulative Count')

        trace.Unit('Hard Coded as: {}', var = 'Per 1000 Care Homes')

        tabTitle = tab.filter(contains_string('Table '))

        dictiList.append(dicti(tab.name, cellCont(tabTitle), columns))

        observations = locAuth.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, ABOVE),
                HDim(locAuth, 'Local Authority', DIRECTLY, LEFT),
                HDim(measure, 'Measure', CLOSEST, ABOVE),
                HDimConst('Measure Type', 'Cumulative Count'),
                HDimConst('Unit', 'Per 1000 Care Homes')
            ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())

    elif tab.name.lower().startswith('table 4'):

        columns = ['Period','NHS Board','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Notes:')).expand(DOWN).expand(UP).expand(RIGHT)

        cell = tab.filter('NHS Board')

        board = cell.fill(DOWN).is_not_blank()
        trace.NHS_Board('Values found in range: {}', var = excelRange(board))

        period = cell.fill(RIGHT).is_not_blank() - remove
        trace.Period('Values found in range: {}', var = excelRange(period))

        measure = cell.shift(1, -1).expand(RIGHT).is_not_blank() | tab.filter(contains_string('Cumulative %')) - remove

        trace.Measure_Type('Hard Coded as: {}', var = 'Cumulative Count')

        trace.Unit('Hard Coded as: {}', var = 'Per 1000 Care Homes')

        tabTitle = tab.filter(contains_string('Table '))

        dictiList.append(dicti(tab.name, cellCont(tabTitle), columns))

        observations = board.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, ABOVE),
                HDim(board, 'NHS Board', DIRECTLY, LEFT),
                HDim(measure, 'Measure', CLOSEST, ABOVE),
                HDimConst('Measure Type', 'Cumulative Count'),
                HDimConst('Unit', 'Per 1000 Care Homes')
            ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())

    elif tab.name.lower().startswith('table 5'):

        columns = ['Period','NHS Board', 'People Tested','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Source:')).expand(DOWN).expand(RIGHT)

        cell = tab.filter('NHS Board')

        board = cell.fill(DOWN).is_not_blank() - remove
        trace.NHS_Board('Values found in range: {}', var = excelRange(board))

        period = cell.fill(RIGHT).is_not_blank() - remove
        trace.Period('Values found in range: {}', var = excelRange(period))

        measure = cell.shift(1, 1).expand(RIGHT).is_not_blank()

        tested = cell.shift(1, 2).expand(RIGHT).is_not_blank()
        trace.People_Tested('Values found in range: {}', var = excelRange(tested))

        trace.Measure_Type('Hard Coded as: {}', var = 'Count')

        trace.Unit('Hard Coded as: {}', var = 'Person')

        tabTitle = tab.filter(contains_string('Table '))

        dictiList.append(dicti(tab.name, cellCont(tabTitle), columns))

        observations = board.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', CLOSEST, LEFT),
                HDim(board, 'NHS Board', DIRECTLY, LEFT),
                HDim(measure, 'Measure', CLOSEST, LEFT),
                HDim(tested, 'People Tested', DIRECTLY, ABOVE), #Needs a better header
                HDimConst('Measure Type', 'Count'),
                HDimConst('Unit', 'Person')
            ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())


# In[368]:


infoData['transform']['transformStage'] = dictiList


# In[369]:


postTransNotes = []

pd.set_option('display.float_format', lambda x: '%.2f' % x)

out = Path('out')
out.mkdir(exist_ok=True)

for tab in tabs:

    if tab.name.lower().startswith('table 1'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Size of Care Home'] = df.apply(lambda x: right(x['Size of Care Home'], len(x['Size of Care Home']) - 6), axis = 1)
        trace.Size_of_Care_Home("Remove 'Beds:' from every entry, leaving only the numbers")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if decimal(float(x['OBS'])) == True else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS('Multiple values by 100 if they are Percentages to correct from Excel formatting')

        df['Measure Type'] = df.apply(lambda x: 'Cumulative Percentage' if '%' in x['Measure'] else x['Measure Type'], axis = 1)
        trace.Measure_Type("Update Measure Type to 'Cumulative Percentage' for percentage values")

        df['Unit'] = df.apply(lambda x: 'Percent' if 'Cumulative Percentage' in x['Measure Type'] else x['Unit'], axis = 1)
        trace.Unit("Update Unit to 'Percent' for percentage values")

        df = df.drop(['Measure'], axis=1)

        df = df[['Period', 'Region', 'Size of Care Home', 'OBS', 'Measure Type', 'Unit']]

        for column in df:
            if column in ('Size of Care Home', 'Marker'):
                df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)

    elif tab.name.lower().startswith('table 2'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if decimal(float(x['OBS'])) == True else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS('Multiple values by 100 if they are Percentages to correct from Excel formatting')

        df['Measure Type'] = df.apply(lambda x: 'Cumulative Percentage' if '%' in x['Measure'] else x['Measure Type'], axis = 1)
        trace.Measure_Type("Update Measure Type to 'Cumulative Percentage' for percentage values")

        df['Unit'] = df.apply(lambda x: 'Percent' if 'Cumulative Percentage' in x['Measure Type'] else x['Unit'], axis = 1)
        trace.Unit("Update Unit to 'Percent' for percentage values")

        df = df.drop(['Measure'], axis=1)

        df = df[['Period', 'Region', 'Sector', 'OBS', 'Measure Type', 'Unit']]

        for column in df:
            if column in ('Sector', 'Marker'):
                df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)

    elif tab.name.lower().startswith('table 3'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if decimal(x['OBS']) == True else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS('Multiple values by 100 if they are Percentages to correct from Excel formatting')

        df['Measure Type'] = df.apply(lambda x: 'Cumulative Percentage' if '%' in x['Measure'] else x['Measure Type'], axis = 1)
        trace.Measure_Type("Update Measure Type to 'Cumulative Percentage' for percentage values")

        df['Unit'] = df.apply(lambda x: 'Percent' if 'Cumulative Percentage' in x['Measure Type'] else x['Unit'], axis = 1)
        trace.Unit("Update Unit to 'Percent' for percentage values")

        df = df.rename(columns = {'DATAMARKER' : 'Marker'})
        trace.add_column('Marker')

        df = df.replace({'Marker' : {'*' : 'Statistical Disclosure Applied'}})
        trace.Marker("Change * DataMarker to 'Statistical Disclosure Applied'")

        df = df.drop(['Measure'], axis=1)

        df = df[['Period', 'Local Authority', 'OBS', 'Marker', 'Measure Type', 'Unit']]

        for column in df:
            if column in ('Local Authority', 'Marker'):
                df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)

    elif tab.name.lower().startswith('table 4'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if decimal(x['OBS']) == True else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS('Multiple values by 100 if they are Percentages to correct from Excel formatting')

        df['Measure Type'] = df.apply(lambda x: 'Cumulative Percentage' if '%' in x['Measure'] else x['Measure Type'], axis = 1)
        trace.Measure_Type("Update Measure Type to 'Cumulative Percentage' for percentage values")

        df['Unit'] = df.apply(lambda x: 'Percent' if 'Cumulative Percentage' in x['Measure Type'] else x['Unit'], axis = 1)
        trace.Unit("Update Unit to 'Percent' for percentage values")

        df = df.rename(columns = {'DATAMARKER' : 'Marker'})
        trace.add_column('Marker')

        df = df.replace({'Marker' : {'*' : 'Statistical Disclosure Applied'}})
        trace.Marker("Change * DataMarker to 'Statistical Disclosure Applied'")

        df = df[['Period', 'NHS Board', 'OBS', 'Marker', 'Measure Type', 'Unit']]

        for column in df:
            if column in ('NHS Board', 'Marker'):
                df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)

    elif tab.name.lower().startswith('table 5'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df = df.replace({'Period' : {
            'w/c 15th June 2020 ¹' : 'w/c 15th June 2020',
            'w/c 22nd June 2020 ²' : 'w/c 22nd June 2020',
            'w/c 29th June 2020 ³' : 'w/c 29th June 2020'}})
        trace.Period("Remove superscript ('1,2,3') tags from Period values (add relevant notes to notes section)")

        df = df[['Period', 'NHS Board', 'Measure', 'OBS', 'Measure Type', 'Unit']]
        trace.add_column('Measure')
        trace.add_column('OBS')

        for column in df:
            if column in ('NHS Board', 'Measure'):
                df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)


# In[370]:


infoData['transform']['Post Transform Changes'] = postTransNotes


# In[371]:


notes = """
Size of care homes is determined by number of beds.
Cumulative numbers are counts since data was first reported and will include cases which are no longer active
'w/c 15th June 2020' Based on return of 966 of Scotland's 1,080 adult care homes
'w/c 22nd June 2020' Based on return of 987 of Scotland's 1,080 adult care homes
'w/c 29th June 2020' Based on return of 1,006 of Scotland's 1,080 adult care homes
"""

infoData['transform']['Stage One Notes'] = notes

with open('infoStageOne.json', 'w') as info:
        info.write(json.dumps(infoData, indent=4).replace('null', '"Not Applicable"'))


# In[372]:


trace.output()

df

