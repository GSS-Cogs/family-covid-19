#!/usr/bin/env python
# coding: utf-8
# %%

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


scraper = Scraper(landingPage)
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

for tab in tabs:

    if tab.name in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:

        columns = ['Period', 'Survey Measure Type', 'Lower CI', 'Upper CI', 'Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        if tab.name in ['4', '5']:
            cell = tab.filter('Contents').shift(0,5)
        else:
            cell = tab.filter('Contents').shift(0, 4)

        remove = tab.filter('Notes:').expand(RIGHT).expand(DOWN)

        if tab.name in ['8']:
            period = tab.filter('Contents').shift(0, 3)
            trace.Period("Value for tab found at: {}", var = cellCont(period))
            trace.add_column('Region')
            region = cell.fill(DOWN).is_not_blank() - remove
            trace.Region("Values found in range: {}", var = excelRange(region))
            trace.add_column('Population Size')
            population = tab.filter('Population size').expand(DOWN).is_not_blank() - remove
            trace.Population_Size("Values found in range: {}", var = excelRange(population))
        elif tab.name in ['9']:
            period = cell.shift(DOWN).fill(DOWN).is_not_blank() - remove
            trace.Period("Values found in range: {}", var = excelRange(period))
            region = cell.expand(RIGHT).is_not_blank()
            trace.add_column('Region')
            trace.Region("Values found in range: {}", var = excelRange(region))
        elif tab.name in ['10']:
            period = tab.filter('Contents').shift(0, 3)
            trace.Period("Value for tab found at: {}", var = cellCont(period))
            trace.add_column('Total Blood Test Sample')
            sample = cell.shift(1, 2)
            trace.Total_Blood_Test_Sample("Value for tab found at: {}", var = excelRange(sample))
        else:
            period = cell.fill(DOWN).is_not_blank() - remove
            trace.Period("Values found in range: {}", var = excelRange(period))

        if tab.name in ['3']:
            measure = cell.shift(DOWN).expand(RIGHT).is_not_blank()
        elif tab.name in ['6', '7']:
            measure = cell.expand(RIGHT).is_not_blank() | cell.shift(DOWN).expand(RIGHT).is_not_blank()
        elif tab.name in ['8']:
             measure = cell.expand(RIGHT).is_not_blank() - population
        elif tab.name in ['9']:
            measure = cell.shift(DOWN).expand(RIGHT).is_not_blank()
        elif tab.name in ['10']:
            measure = cell.expand(DOWN).is_not_blank() - remove
        else:
            measure = cell.expand(RIGHT).is_not_blank()
        trace.Survey_Measure_Type("Values found in range: {}", var = excelRange(measure))

        if tab.name in ['10']:
            lower = tab.filter('Lower').fill(DOWN) - remove
        else:
            lower = tab.filter('Lower').fill(DOWN).is_not_blank() - remove
        trace.Lower_CI("Values found in range: {}", var = excelRange(lower))

        if tab.name in ['10']:
            upper = tab.filter('Upper').fill(DOWN) - remove
        else:
            upper = tab.filter('Upper').fill(DOWN).is_not_blank() - remove
        trace.Upper_CI("Values found in range: {}", var = excelRange(upper))

        if tab.name in ['8']:
            observations = region.fill(RIGHT).is_not_blank() - upper - lower - population
        elif tab.name in ['10']:
            observations = measure.fill(RIGHT).is_not_blank() - upper - lower - sample - tab.filter(contains_string('ratio')).expand(RIGHT)
        else:
            observations = period.fill(RIGHT).is_not_blank() - tab.filter(contains_string(' in ')).expand(RIGHT) - upper - lower

        if tab.name in ['2']:
            measureType = 'Percentage'
            trace.Measure_Type("Hardcoded as: {}", var = measureType)
        else:
            measureType = 'temp'
            trace.Measure_Type("Temporarily added as: {}", var = measureType)

        if tab.name in ['2']:
            unit = 'Percent'
            trace.Unit("Hardcoded as: {}", var = unit)
        else:
            unit = 'temp'
            trace.Unit("Temporarily added as: {}", var = unit)

        tabTitle = tab.filter(contains_string('Table ')).shift(DOWN)

        infoTransform(tab.name, cellCont(tabTitle), columns)

        if tab.name in ['8']:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, LEFT),
                    HDim(region, 'Region', DIRECTLY, LEFT),
                    HDim(population, 'Population Size', DIRECTLY, LEFT),
                    HDim(measure, 'Survey Measure Type', DIRECTLY, ABOVE),
                    HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
                    ]
        elif tab.name in ['9']:
            dimensions = [
                    HDim(period, 'Period', DIRECTLY, LEFT),
                    HDim(region, 'Region', DIRECTLY, ABOVE),
                    HDim(measure, 'Survey Measure Type', DIRECTLY, ABOVE),
                    HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
                    ]
        elif tab.name in ['10']:
            dimensions = [
                    HDim(period, 'Period', CLOSEST, LEFT),
                    HDim(measure, 'Survey Measure Type', DIRECTLY, LEFT),
                    HDim(sample, 'Total Blood Test Sample', CLOSEST, LEFT),
                    HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
                    ]
        else:
            dimensions = [
                        HDim(period, 'Period', DIRECTLY, LEFT),
                        HDim(measure, 'Survey Measure Type', DIRECTLY, ABOVE),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType),
                        HDimConst('Unit', unit)
                        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())


# %%
all_dat = []

pd.set_option('display.float_format', lambda x: '%.2f' % x)

out = Path('out')
out.mkdir(exist_ok=True)

for tab in tabs:

    if tab.name in ['1']:#1

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if '%' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if '%' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if '%' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if '%' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)
    elif tab.name in ['2']:#2

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if '%' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if '%' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if '%' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if '%' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['3']:#3

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if '%' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if '%' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if '%' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if '%' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df = df.replace({'Lower CI' : {
            '' : 0},
                         'Upper CI' : {
            '' : 0
                         }})

        df['Weighted'] = 'temp'
        df['Weighted'] = df.apply(lambda x: 'TRUE' if '%' in x['Survey Measure Type'] else 'FALSE', axis = 1)

        trace.add_column('Weighted')
        trace.Weighted('Add column filled on condition that values are weighted or not from sheet (replace with check)')

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['4']:#4

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Rate per 10000' if 'Incidence rate' in x['Survey Measure Type'] else 'Estimated Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Rate per 10000' and 'Estimated Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Person per 10000' if 'Incidence rate' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Person per 10000' and 'Person' where applicable")

        df['Weighted'] = 'FALSE'
        trace.add_column('Weighted')
        trace.Weighted('Add column filled on condition that values are weighted or not from sheet (replace with check)')

        df = df.replace({'Survey Measure Type' : {
            'New infections per day' : 'Estimated New Infections per day (modelled)'}})

        trace.add_column('OBS')

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['5']:#5

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Rate per 10000' if 'Incidence rate' in x['Survey Measure Type'] else 'Estimated Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Rate per 10000' where applicable")

        df['Unit'] = df.apply(lambda x: 'Person' if 'Incidence rate' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Person' where applicable")

        df['Weighted'] = 'FALSE'
        trace.add_column('Weighted')
        trace.Weighted("Add column filled on condition that values are weighted or not from sheet (replace with check)")
        trace.add_column('OBS')

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['6']:#6

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Rate per 10000' if 'Incidence rate' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Rate per 10000', 'Count', or 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Person' , axis = 1)
        trace.Unit("Replace temp values with 'Person' where applicable")

        df = df.replace({'Lower CI' : {
            '' : 0},
                         'Upper CI' : {
            '' : 0},
                        'DATAMARKER' : {
            '**' : 'p value = 0.08 comparing last 2 week periods'
                        }})

        df['Weighted'] = 'FALSE'
        trace.add_column('Weighted')
        trace.Weighted("Add column filled on condition that values are weighted or not from sheet (replace with check)")
        trace.add_column('OBS')

        df = df.rename(columns = {'DATAMARKER' : 'Marker'})
        trace.add_column('Marker')
        trace.Marker("Replace '**' with 'p value = 0.08 comparing last 2 week periods' as per sheet notes")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['7']:#7

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Rate per 10000' if 'Incidence rate' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Rate per 10000', 'Count', or 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Household' , axis = 1)
        trace.Unit("Replace temp values with 'Household' where applicable")

        df = df.replace({'Lower CI' : {
            '' : 0},
                         'Upper CI' : {
            '' : 0},
                        'DATAMARKER' : {
            '**' : 'p value = 0.08 comparing last 2 week periods'
                        }})

        df['Weighted'] = 'FALSE'
        trace.add_column('Weighted')
        trace.Weighted("Add column filled on condition that values are weighted or not from sheet (replace with check)")
        trace.add_column('OBS')

        df = df.rename(columns = {'DATAMARKER' : 'Marker'})
        trace.add_column('Marker')
        trace.Marker("Replace '**' with 'p value = 0.08 comparing last 2 week periods' as per sheet notes")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['8']:#8

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if '%' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if '%' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if '%' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if '%' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)

    elif tab.name in ['9']:#9

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if '%' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if '%' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if '%' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if '%' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)
    elif tab.name in ['10']:#10

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df['Measure Type'] = df.apply(lambda x: 'Percentage' if 'Percentage' in x['Survey Measure Type'] else 'Count', axis = 1)
        trace.Measure_Type("Replace temp values with 'Estimated Percentage' and 'Estimated Average Count' where applicable")

        df['Unit'] = df.apply(lambda x: 'Percent' if 'Percentage' in x['Survey Measure Type'] else 'Person', axis = 1)
        trace.Unit("Replace temp values with 'Percent' and 'Person' where applicable")

        df['OBS'] = df.apply(lambda x: x['OBS']*100 if 'Percentage' in x['Survey Measure Type'] else x['OBS'], axis = 1)
        trace.add_column('OBS')
        trace.OBS("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Upper CI'] = df.apply(lambda x: float(x['Upper CI'])*100 if 'Percentage' in x['Survey Measure Type'] else x['Upper CI'], axis = 1)
        trace.Upper_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Lower CI'] = df.apply(lambda x: float(x['Lower CI'])*100 if 'Percentage' in x['Survey Measure Type'] else x['Lower CI'], axis = 1)
        trace.Lower_CI("Multiple values by 100 if they are Percentages to correct from Excel formatting")

        df['Weighted'] = 'temp'
        df['Weighted'] = df.apply(lambda x: 'TRUE' if 'weighted' in x['Survey Measure Type'] else 'FALSE', axis = 1)

        trace.add_column('Weighted')

        df = df.replace({'Lower CI' : {
            '' : 0},
                         'Upper CI' : {
            '' : 0},
                         'Survey Measure Type' : {
            'Individuals included in antibody analysis (unweighted)' : 'Individuals included in antibody analysis',
            'Percentage of individuals testing positive for antibodies (weighted)' : 'Percentage of individuals testing positive for antibodies',
            'Estimated average number of people in England who would test positive for antibodies  (weighted)' : 'Estimated average number of people in England who would test positive for antibodies'}})

        infoComments(name, list(df.columns))

        #df.drop_duplicates().to_csv(out / f'{tableName}.csv', index = False)
        df.drop_duplicates()
        all_dat.append(df)


# %%


notes = """
These statistics refer to infections reported in the community, by which we mean private households. These figures exclude infections reported in hospitals, care homes or other institutional settings.
This analysis is based on statistical modelling conducted by our research partners at the University of Oxford.
The method combines a statistical modelling approach with population information used in standard population weighting.
As this is based on Bayesian analysis, the appropriate uncertainty measure to use is credible intervals rather than confidence intervals. However they can be interpreted in the same way.
Estimates are presented for the mid-point (Thursday) of each week over the period.
The England population used in this analysis relates to the community population aged two years and over. It is not the same as the total population of England as reported in our mid-year population estimates.
Only people aged sixteen and over are included in our blood test. Therefore, the English population estimates used included only those aged 16 and over. This population is 45,042,000
"""

infoNotes(notes)


# %%
trace.output()

#df


# %%
#all_dat[9].head(60)

# %%

# %%
