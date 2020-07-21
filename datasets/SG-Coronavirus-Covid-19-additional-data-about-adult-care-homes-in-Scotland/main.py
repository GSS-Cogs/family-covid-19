#!/usr/bin/env python
# coding: utf-8
# %%
#SG-Coronavirus-Covid-19-additional-data-about-adult-care-homes-in-Scotland

# %%


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


# %%


scraper = Scraper(seed='info.json')
scraper.distributions[0].title = "Coronavirus (Covid-19): additional data about adult care homes in Scotland"
scraper


# %%


distribution = scraper.distributions[0]
display(distribution)


# %%


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


# %%


infoData['transform']['transformStage'] = dictiList


# %%

all_tabs = []
postTransNotes = []

pd.set_option('display.float_format', lambda x: '%.2f' % x)

#out = Path('out')
#out.mkdir(exist_ok=True)

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

        #for column in df:
        #    if column in ('Size of Care Home', 'Marker'):
        #        df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        all_tabs.append(df)

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

        #for column in df:
        #    if column in ('Sector', 'Marker'):
        #        df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        all_tabs.append(df)

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
        df = df.replace({'OBS' : {'' : '0'}})

        df = df.drop(['Measure'], axis=1)

        df = df[['Period', 'Local Authority', 'OBS', 'Marker', 'Measure Type', 'Unit']]

        #for column in df:
        #    if column in ('Local Authority', 'Marker'):
        #        df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        all_tabs.append(df)

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

        #for column in df:
        #    if column in ('NHS Board', 'Marker'):
        #        df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        all_tabs.append(df)

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

        df = df[['Period', 'NHS Board', 'Measure', 'People Tested', 'OBS', 'Measure Type', 'Unit']]
        trace.add_column('Measure')
        trace.add_column('OBS')

        #for column in df:
        #    if column in ('NHS Board', 'Measure'):
        #        df[column] = df[column].map(lambda x: pathify(x))

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        all_tabs.append(df)


# %%


infoData['transform']['Post Transform Changes'] = postTransNotes


# %%


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


# %%
trace.output()


# %%
all_tabs[0]['Sector'] = 'All'

# %%
all_tabs[0]['Measure Type'][all_tabs[0]['Measure Type'] == 'Cumulative Count'] = "Per 1000 registered places"
all_tabs[0]['Unit'][all_tabs[0]['Unit'] == 'Per 1000 Care Homes'] = "Cumulative Count"

all_tabs[0]['Measure Type'][all_tabs[0]['Measure Type'] == 'Cumulative Percentage'] = "Adult Care Home"
all_tabs[0]['Unit'][all_tabs[0]['Unit'] == 'Percent'] = "Cumulative Percentage"

all_tabs[0]['Size of Care Home'][all_tabs[0]['Size of Care Home'] == '-60'] = "More than 60"
all_tabs[0]['Size of Care Home'] = all_tabs[0]['Size of Care Home'] + ' Beds'

all_tabs[0]['Period'] = pd.to_datetime(all_tabs[0]['Period']).dt.strftime('%Y-%m-%dT%H:%M:%S')
all_tabs[0]['Period'] = "gregorian-interval/" + all_tabs[0]['Period'] + '/P1D'

all_tabs[0] = all_tabs[0].rename(columns = {'Region' : 'Local Authority'})

# %%
all_tabs[1]['Size of Care Home'] = 'All'

# %%
all_tabs[1]['Measure Type'][all_tabs[1]['Measure Type'] == 'Cumulative Count'] = "Per 1000 registered places"
all_tabs[1]['Unit'][all_tabs[1]['Unit'] == 'Per 1000 Care Homes'] = "Cumulative Count"

all_tabs[1]['Measure Type'][all_tabs[1]['Measure Type'] == 'Cumulative Percentage'] = "Adult Care Home"
all_tabs[1]['Unit'][all_tabs[1]['Unit'] == 'Percent'] = "Cumulative Percentage"

all_tabs[1]['Period'] = pd.to_datetime(all_tabs[1]['Period']).dt.strftime('%Y-%m-%dT%H:%M:%S')
all_tabs[1]['Period'] = "gregorian-interval/" + all_tabs[1]['Period'] + '/P1D'

all_tabs[1] = all_tabs[1].rename(columns = {'Region' : 'Local Authority'})


# %%
all_tabs[2]['Sector'] = 'All'
all_tabs[2]['Size of Care Home'] = 'All'

# %%
all_tabs[2]['Measure Type'][all_tabs[2]['Measure Type'] == 'Cumulative Count'] = "Per 1000 registered places"
all_tabs[2]['Unit'][all_tabs[2]['Unit'] == 'Per 1000 Care Homes'] = "Cumulative Count"

all_tabs[2]['Measure Type'][all_tabs[2]['Measure Type'] == 'Cumulative Percentage'] = "Adult Care Home"
all_tabs[2]['Unit'][all_tabs[2]['Unit'] == 'Percent'] = "Cumulative Percentage"

all_tabs[2]['Period'] = pd.to_datetime(all_tabs[2]['Period']).dt.strftime('%Y-%m-%dT%H:%M:%S')
all_tabs[2]['Period'] = "gregorian-interval/" + all_tabs[2]['Period'] + '/P1D'

# %%
all_tabs[3]['Sector'] = 'All'
all_tabs[3]['Size of Care Home'] = 'All'

# %%
all_tabs[3]['Measure Type'][all_tabs[3]['Measure Type'] == 'Cumulative Count'] = "Per 1000 registered places"
all_tabs[3]['Unit'][all_tabs[3]['Unit'] == 'Per 1000 Care Homes'] = "Cumulative Count"

all_tabs[3]['Measure Type'][all_tabs[3]['Measure Type'] == 'Cumulative Percentage'] = "Adult Care Home"
all_tabs[3]['Unit'][all_tabs[3]['Unit'] == 'Percent'] = "Cumulative Percentage"

all_tabs[3]['Period'] = pd.to_datetime(all_tabs[3]['Period']).dt.strftime('%Y-%m-%dT%H:%M:%S')
all_tabs[3]['Period'] = "gregorian-interval/" + all_tabs[3]['Period'] + '/P1D'

# %%
#### I know theres probably one line of code that does this but i got carried away lol!
dtes = all_tabs[4]['Period'].str.split("-", n = 1, expand = True)
dtes[1] = dtes[1].str.replace('(¹)','')
dtes[1] = dtes[1].str.replace('(²)','')
dtes[1] = dtes[1].str.replace('(³)','')
dtes[1] = dtes[1].str.replace('(⁴)','')
dtes[1] = dtes[1].str.replace('(4)','')
dtes[1] = dtes[1].str.strip()
dtes[0] = dtes[0].str.strip()
#²³¹⁰ⁱ⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ]

# Get the year from the second date and attach it to the first date!!!!!
dtes2 = dtes[1].str.split(" ", n = 2, expand = True)
dtes[2] = dtes2[2]
dtes[0] = dtes[0] + ' ' + dtes[2]
del dtes2
del dtes[2]
dtes[2] = pd.to_datetime(dtes[0])
dtes[3] = pd.to_datetime(dtes[1])

dtes[4] = (dtes[3]-dtes[2]).astype('timedelta64[D]')
# Only getting 6 days back but assuming it is 7 to represent a full week
dtes[4] = (dtes[4] + 1).astype(int).astype(str)
dtes[5] = 'gregorian-interval/'
dtes[6] = 'T00:00:00/P'
dtes[7] = 'D'
dtes[8] = (dtes[5] + dtes[2].dt.strftime('%Y-%m-%dT%H:%M:%S') + '/P' + dtes[4] + dtes[7])#.replace('/P0 ', '/P')

dtes.head(10)
all_tabs[4]['Period'] = dtes[8]

# %%
all_tabs[3] = all_tabs[3].rename(columns = {'NHS Board' : 'Local Authority'})
all_tabs[4] = all_tabs[4].rename(columns = {'Measure' : 'COVID-19 Confirmed'})

# %%
all_tabs[0]['Marker'] = ''
all_tabs[1]['Marker'] = ''
all_tabs[4]['Marker'] = ''
all_tabs[4].head(5)

# %%
all_tabs[0] = all_tabs[0][['Period', 'Local Authority', 'Size of Care Home', 'Sector', 'Measure Type', 'Unit', 'Marker', 'OBS']]
all_tabs[1] = all_tabs[1][['Period', 'Local Authority', 'Size of Care Home', 'Sector', 'Measure Type', 'Unit', 'Marker', 'OBS']]
all_tabs[2] = all_tabs[2][['Period', 'Local Authority', 'Size of Care Home', 'Sector', 'Measure Type', 'Unit', 'Marker', 'OBS']]
all_tabs[3] = all_tabs[3][['Period', 'Local Authority', 'Size of Care Home', 'Sector', 'Measure Type', 'Unit', 'Marker', 'OBS']]

# %%
# Pull the mapping files into DataFrames
geogsHB = pd.read_csv('../../Reference/scottish-health-board-mapping.csv') 
geogsCA = pd.read_csv('../../Reference/scottish-council-areas-mapping.csv') 

# %%
all_tabs[0]['Local Authority'][all_tabs[0]['Local Authority'] == 'SCOTLAND'] = 'Scotland'
all_tabs[1]['Local Authority'][all_tabs[1]['Local Authority'] == 'SCOTLAND'] = 'Scotland'
all_tabs[2]['Local Authority'][all_tabs[2]['Local Authority'] == 'SCOTLAND'] = 'Scotland'
all_tabs[3]['Local Authority'][all_tabs[3]['Local Authority'] == 'SCOTLAND'] = 'Scotland'
all_tabs[4]['NHS Board'][all_tabs[4]['NHS Board'] == 'SCOTLAND'] = 'Scotland'

# %%
# Map the Geography codes
all_tabs[0]['Local Authority'] = all_tabs[0]['Local Authority'].map(geogsCA.set_index('Category')['Code'])
all_tabs[1]['Local Authority'] = all_tabs[1]['Local Authority'].map(geogsCA.set_index('Category')['Code'])
all_tabs[2]['Local Authority'] = all_tabs[2]['Local Authority'].map(geogsCA.set_index('Category')['Code'])
all_tabs[3]['Local Authority'] = all_tabs[3]['Local Authority'].map(geogsHB.set_index('Category')['Code'])
all_tabs[4]['NHS Board2'] = all_tabs[4]['NHS Board'].map(geogsHB.set_index('Category')['Code'])

# %%
joined_dat1 = pd.concat([all_tabs[0],all_tabs[1],all_tabs[2],all_tabs[3]])
joined_dat2 = pd.concat([all_tabs[4]])

# %%
#joined_dat1.head(10)

# %%
joined_dat1 = joined_dat1.rename(columns = {'OBS' : 'Value'})
joined_dat2 = joined_dat2.rename(columns = {'OBS' : 'Value'})
joined_dat1 = joined_dat1.rename(columns = {'Local Authority' : 'Geography Code'})
joined_dat2 = joined_dat2.rename(columns = {'NHS Board' : 'NHS Board Code'})

# %%
joined_dat1['Geography Code'] = joined_dat1['Geography Code'].apply(pathify) 
joined_dat1['Size of Care Home'] = joined_dat1['Size of Care Home'].apply(pathify) 
joined_dat1['Size of Care Home'][joined_dat1['Size of Care Home'] == '-60-beds'] = 'more-than-60-beds'
joined_dat1['Sector'] = joined_dat1['Sector'].apply(pathify)
joined_dat1['Measure Type'] = joined_dat1['Measure Type'].apply(pathify)
joined_dat1['Unit'] = joined_dat1['Unit'].apply(pathify)

joined_dat2['NHS Board Code'] = joined_dat2['NHS Board Code'].apply(pathify) 
joined_dat2['COVID-19 Confirmed'] = joined_dat2['COVID-19 Confirmed'].apply(pathify) 
joined_dat2['People Tested'] = joined_dat2['People Tested'].apply(pathify)

# %%
######################################################################
######################################################################
## REMOVE MULTIPLE UNITS FOR NOW UNTIL CAN BE PROCESSED IN JENKINS ###
#print(joined_dat.count())
joined_dat1 = joined_dat1[joined_dat1['Unit'] == 'Cumulative Count'] 
#print(joined_dat.count())
######################################################################
######################################################################
#joined_dat1.head(10)

# %%
# Output the data to CSV
csvName = 'suspected-covid-19-cases-observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat1.drop_duplicates().to_csv(out / csvName, index = False)

# %%
scraper.dataset.family = 'covid-19'
scraper.dataset.description = 'SG Coronavirus COVID-19 additional data about adult care homes in Scotland - Suspected COVID-19 Cases.\n ' + notes

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name)) + '-' + pathify(csvName)
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
scraper.dataset.title = 'SG Covid-19 additional data about adult care homes - Suspected COVID-19 Cases'
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

# %%
# Output the data to CSV
#csvName = 'residents-and-staff-tested-for-covid-19-observations.csv'
#out = Path('out')
#out.mkdir(exist_ok=True)
#joined_dat2.drop_duplicates().to_csv(out / csvName, index = False)

# %%
"""
scraper.dataset.family = 'covid-19'
scraper.dataset.description = 'SG Coronavirus COVID-19 additional data about adult care homes in Scotland - Residents and Staff Tested.\n ' + notes

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name)) + '-' + pathify(csvName)
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
scraper.dataset.title = 'SG Covid-19 additional data about adult care homes - Residents and Staff Tested'
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
"""

# %%

# %%

# %%
