#!/usr/bin/env python
# coding: utf-8

# In[56]:


#!/usr/bin/env python
# coding: utf-8


# In[56]:





# In[57]:



#!/usr/bin/env python
# coding: utf-8


# In[58]:



# -*- coding: utf-8 -*-
# # NRS Births, deaths, and other vital events

from gssutils import *
import json
from dateutil.parser import parse
from datetime import datetime, timedelta
from urllib.parse import urljoin
import string
import pathlib
import re

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

def cellCont(cell):
    return re.findall(r"'([^']*)'", str(cell))[0]

def excelRange(bag):
    xValue = []
    yValue = []
    for cell in bag:
        coordinate = cellLoc(cell)
        xValue.append(''.join([i for i in coordinate if not i.isdigit()]))
        yValue.append(int(''.join([i for i in coordinate if i.isdigit()])))
    high = 0
    low = 0
    for i in xValue:
        if col2num(i) >= high:
            high = col2num(i)
        if low == 0:
            low = col2num(i)
        elif col2num(i) < low:
            low = col2num(i)
        highx = colnum_string(high)
        lowx = colnum_string(low)
    highy = str(max(yValue))
    lowy = str(min(yValue))

    return '{' + lowx + lowy + '-' + highx + highy + '}'

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[ ]:


scrape = Scraper(landingPage)
scrape


# In[ ]:


scrape.distributions


# In[ ]:


dist = scrape.distributions[0]
display(dist)


# In[ ]:



pd.set_option('display.float_format', lambda x: '%.2f' % x)

trace = TransformTrace()

tabs = { tab.name: tab for tab in dist.as_databaker() if tab.name.startswith('Q')}
list(tabs)

datasetTitle = info['title']
link = dist.downloadURL

tidied_sheets = {}

for name, tab in tabs.items():

    if 'q1' == name.lower():

        columns = ['Period', 'Measurement', 'Sex', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Table Q1:"))

        year = cell.shift(1,2).fill(DOWN).is_not_blank() - remove
        trace.Period('Year to use with Period taken from cell range: {}', var = excelRange(year))

        quarter = cell.shift(0,2).fill(DOWN).is_not_blank() - remove
        trace.Period('Quarter to use with Period taken from cell range: {}', var = excelRange(quarter))

        measurement1 = cell.shift(2, 2).expand(RIGHT).is_not_blank()
        trace.Measurement('Temporary header name')
        trace.Measurement('Measurement Value found in cell range: {}', var = excelRange(measurement1))

        measurement2 = cell.shift(2, 3).expand(RIGHT).is_not_blank()
        trace.Sex('Observations adapted from Value found in range: {}', var = excelRange(measurement2))

        measurement3 = cell.shift(2, 4).expand(RIGHT) - cell.shift(2, 2).expand(RIGHT).filter('Year').shift(0, 2).expand(RIGHT)
        trace.Measurement('Additional information found in range: {}', var = excelRange(measurement3))
        trace.Sex('Additional information found in range: {}', var = excelRange(measurement3))

        observations = (year.fill(RIGHT).is_not_blank() | quarter.fill(RIGHT).is_not_blank()) & measurement3.expand(DOWN)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDim(year, 'Year', CLOSEST, ABOVE),
        HDim(quarter, 'Quarter', CLOSEST, BELOW),
        HDim(measurement1, 'Measurement 1', CLOSEST, LEFT),
        HDim(measurement2, 'Measurement 2', CLOSEST, LEFT),
        HDim(measurement3, 'Measurement 3', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

    elif 'q2' in name.lower():

        columns = ['Period', 'Area', 'Measurement', 'Sex', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Table Q2:"))

        period = 'quarter/2020-Q2'
        trace.Period('Period Hardcoded for tab as: {}', var = period)

        area = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove
        trace.Area('Value found in cell range: {}', var = excelRange(measurement1))

        areaType = area.filter(contains_string('areas'))

        measurement1 = cell.shift(1, 3).expand(RIGHT).is_not_blank()
        trace.Measurement('Temporary header name')
        trace.Measurement('Measurement Value found in cell range: {}', var = excelRange(measurement1))

        measurement2 = cell.shift(1, 4).expand(RIGHT).is_not_blank()
        trace.Sex('Observations adapted from Value found in range: {}', var = excelRange(measurement2))

        measurement3 = cell.shift(1, 5).expand(RIGHT) - cell.shift(1, 3).expand(RIGHT).filter('Area').shift(0, 2).expand(DOWN)
        trace.Measurement('Additional information found in range: {}', var = excelRange(measurement3))
        trace.Sex('Additional information found in range: {}', var = excelRange(measurement3))

        observations = area.fill(RIGHT).is_not_blank() & measurement3.expand(DOWN)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDimConst('Period', period),
        HDim(area, 'Area', CLOSEST, BELOW),
        HDim(areaType, 'Area Type', CLOSEST, ABOVE),
        HDim(measurement1, 'Measurement 1', CLOSEST, LEFT),
        HDim(measurement2, 'Measurement 2', CLOSEST, LEFT),
        HDim(measurement3, 'Measurement 3', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

    elif 'q3' in name.lower():

        columns = ['Period', 'Area', 'Measurement', 'Age', 'Sex', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Table Q3:"))

        period = 'quarter/2020-Q2'
        trace.Period('Period Hardcoded for tab as: {}', var = period)

        measurement = 'Deaths'
        trace.Measurement('Temporary header name')
        trace.Measurement("Hardcoded for tab as: {}", var = measurement)

        area = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove
        trace.Area('Value found in cell range: {}', var = excelRange(area))

        areaType = area.filter(contains_string('areas'))

        age = cell.shift(1, 3).expand(RIGHT).is_not_blank()
        trace.Age('Value found in cell range: {}', var = excelRange(age))

        gender = cell.shift(1, 4).expand(RIGHT).is_not_blank()
        trace.Sex('Value found in cell range: {}', var = excelRange(gender))

        observations = area.fill(RIGHT).is_not_blank() & gender.expand(DOWN)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDimConst('Period', period),
        HDim(area, 'Area', CLOSEST, BELOW),
        HDim(areaType, 'Area Type', CLOSEST, ABOVE),
        HDimConst('Measurement', measurement),
        HDim(age, 'Age', CLOSEST, LEFT),
        HDim(gender, 'Gender', CLOSEST, LEFT)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

    elif 'q4' in name.lower():

        columns = ['Period', 'ICD 10 Summary List', 'Cause of Death', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Table Q4:"))

        period = cell.shift(2, 4).expand(RIGHT).is_not_blank() - cell.shift(2, 4).expand(RIGHT).filter(contains_string('average'))
        trace.Period('Year for period found in range: {}', var = excelRange(period))

        icd = cell.shift(0, 3).fill(DOWN) - remove
        trace.ICD_10_Summary_List("Value found in range: {}", var = excelRange(icd))

        cause_of_death = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove
        trace.Cause_of_Death('Value found in cell range: {}', var = excelRange(cause_of_death))

        observations = cause_of_death.fill(RIGHT).is_not_blank() & period.expand(DOWN) - tab.filter('ICD 10 Summary List').expand(RIGHT)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDim(period, 'Period', DIRECTLY, ABOVE),
        HDim(icd, 'ICD 10 Summary List', DIRECTLY, LEFT),
        HDim(cause_of_death, 'Cause of Death', DIRECTLY, LEFT)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

    elif 'q5' in name.lower():

        columns = ['Period', 'Cause of Death', 'ICD 10 Summary List', 'Age', 'Sex', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Q5:"))

        period = left(right(cellCont(tab.filter(contains_string('Q5'))), 5), 4)
        trace.Period('Period Year for tab as: {}', var = period)

        icd = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove
        trace.ICD_10_Summary_List("Value found in range: {}", var = excelRange(icd))

        cause_of_death = cell.shift(1, 2).fill(DOWN).is_not_blank() - remove
        trace.Cause_of_Death('Value found in cell range: {}', var = excelRange(cause_of_death))

        age = (cell.shift(2, 3).expand(RIGHT) | cell.shift(2, 3).expand(RIGHT).shift(DOWN)).is_not_blank()
        trace.Age('Value found in cell range: {}', var = excelRange(age))

        gender = cell.shift(2, 2).fill(DOWN).is_not_blank() - remove
        trace.Sex('Value found in cell range: {}', var = excelRange(gender))

        observations = gender.fill(RIGHT).is_not_blank() & age.expand(DOWN)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDimConst('Period', period),
        HDim(cause_of_death, 'Cause of Death', CLOSEST, ABOVE),
        HDim(icd, 'ICD 10 Summary List', CLOSEST, ABOVE),
        HDim(age, 'Age', DIRECTLY, ABOVE),
        HDim(gender, 'Gender', DIRECTLY, LEFT)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())

    elif 'q6' in name.lower():

        columns = ['Period', 'Area', 'Cause of Death', 'ICD 10 Summary List', 'Sex', 'Value', 'Marker']

        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter('Footnotes').expand(DOWN).expand(RIGHT)

        cell = tab.filter(contains_string("Q6:"))

        period = left(right(cellCont(tab.filter(contains_string('Q6:'))), 5), 4)
        trace.Period('Period Year for tab as: {}', var = period)

        icd = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove
        trace.ICD_10_Summary_List("Value found in range: {}", var = excelRange(icd))

        cause_of_death = cell.shift(1, 2).fill(DOWN).is_not_blank() - remove
        trace.Cause_of_Death('Value found in cell range: {}', var = excelRange(cause_of_death))

        area = cell.shift(3, 2).expand(RIGHT).is_not_blank()
        trace.Area('Value found in cell range: {}', var = excelRange(area))

        gender = cell.shift(2, 2).fill(DOWN).is_not_blank() - remove
        trace.Sex('Value found in cell range: {}', var = excelRange(gender))

        observations = gender.fill(RIGHT).is_not_blank() & area.expand(DOWN)
        trace.Value('Observations found in range: {}', var = excelRange(observations))

        dimensions = [
        HDimConst('Period', period),
        HDim(cause_of_death, 'Cause of Death', CLOSEST, ABOVE),
        HDim(icd, 'ICD 10 Summary List', CLOSEST, ABOVE),
        HDim(area, 'Area', DIRECTLY, ABOVE),
        HDim(gender, 'Gender', DIRECTLY, LEFT)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(name, tidy_sheet.topandas())


# In[ ]:



out = Path('out')
out.mkdir(exist_ok=True)

tidied_tables = {}

for name in tabs:

    if name.lower() == 'q1':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df = df.replace({'Measurement 1' : {
            ' Marriages 2' : 'Marriages',
            'Stillbirths 1' : 'Stillbirths'},
                         'Year' : {
            'Year 20196 ' : 'Year 2019',
            'Year 20206 ' : 'Year 2020'},
                        'DATAMARKER' : {
            '- ' : '-'
                        }})
        trace.Measurement("Replace ' Marriages 2' with 'Marriages'")
        trace.Measurement("Replace 'Stillbirths 1' with 'Stillbirths'")
        trace.Period("Replace 'Year 20196 ' with 'Year 2019'")
        trace.Period("Replace 'Year 20206 ' with 'Year 2020'")

        df['Quarter'] = df.apply(lambda x: '1st' if '1st' in x['Quarter'] else x['Quarter'], axis =1)
        df['Quarter'] = df.apply(lambda x: left(x['Quarter'], 1), axis =1)
        df['Year'] = df.apply(lambda x: right(x['Year'].strip(), 4), axis =1)
        df['Period'] = df.apply(lambda x: 'quarter/'+ x['Year'].replace('Year ', '') + '-Q' + x['Quarter'], axis = 1)
        trace.add_column("Period")
        trace.Period("Create Period Value based on 'Year' and 'Quarter' columns")

        df['Gender'] = df.apply(lambda x: 'F' if 'Female' in x['Measurement 2'] else ('M' if 'Male' in x['Measurement 2'] else 'T'), axis = 1)
        df['Gender'] = df.apply(lambda x: 'T' if 'both sexes' in x['Measurement 2'].lower() else x['Gender'], axis = 1)
        trace.Sex("Replace 'Females' with 'F', 'Males' with 'M' and 'T' otherwise where appropriate")

        df = df.replace({'Measurement 1' : {
            'Civil Partnerships  Female ' : 'Civil Partnerships',
            'Civil Partnerships  Male ' : 'Civil Partnerships',
            'Deaths - all ages Both sexes Number' : 'Deaths all ages Number',
            'Deaths - all ages Both sexes Rate3' : 'Deaths all ages Rate',
            'Deaths - all ages Females ' : 'Deaths all ages Number',
            'Deaths - all ages Males ' : 'Deaths all ages Number',
            'Infant deaths Number ' : 'Infant deaths Number',
            'Infant deaths Rate5 ' : 'Infant deaths Rate',
            'Live births  Females ' : 'Live births Number',
            'Live births  To unmarried parents % of live births' : 'Live births To unmarried parents % of live births',
            'Live births  To unmarried parents Number' : 'Live births To unmarried parents Number',
            'Live births Both sexes Number' : 'Live births Number',
            'Live births Both sexes Rate3' : 'Live births Rate',
            'Live births Males ' : 'Live births Number',
            'Live births Males per 1,000 females ' : 'Live births Males per 1000 females',
            'Marriages Opposite Sex ' : 'Marriages Opposite Sex Number',
            'Marriages Rate3 ' : 'Marriages Rate',
            'Marriages Same Sex ' : 'Marriages Number',
            'Marriages Total ' : 'Marriages Total',
            'Neonatal deaths Number ' : 'Neonatal deaths Number',
            'Neonatal deaths Rate5 ' : 'Neonatal deaths Rate',
            'Perinatal deaths Number ' : 'Perinatal deaths Number',
            'Perinatal deaths Rate4 ' : 'Perinatal deaths Rate',
            'Stillbirths Number ' : 'Stillbirths Number',
            'Stillbirths Rate4 ' : 'Stillbirths Rate'}})
        trace.Measurement('Combining column Value indicate rate/number Value (for use for stage 2 and then removed)')

        df['Gender'] = df.apply(lambda x: 'T' if 'sex' in x['Measurement 1'].lower() or 'Marriages' in x['Measurement 1'] else x['Gender'], axis = 1)

        df['Parent Marital Status'] = df.apply(lambda x: 'unmarried' if 'To unmarried parents' in x['Measurement 2'] else 'married', axis = 1)
        df['Parent Marital Status'] = df.apply(lambda x: 'all' if 'live births' not in x['Measurement 1'].lower() else x['Parent Marital Status'], axis = 1)
        trace.add_column('Parent Marital Status')
        trace.Parent_Marital_Status("Unmarried or Married based on Live Birth values, all to rest of rows")

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")
        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 population' if 'rate' in x['Measurement 2'].lower() or 'rate' in x['Measurement 3'].lower() else 'count', axis = 1)
        df['Unit'] = df.apply(lambda x: 'births' if 'live births' in x['Measurement 1'].lower() else 'deaths', axis = 1)

        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 live and still births' if 'rate' in x['Measure Type'] and x['Measurement 1'].lower() in ['stillbirths', 'perinatal deaths'] else x['Measure Type'], axis = 1)
        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 live births' if 'rate' in x['Measure Type'] and x['Measurement 1'].lower() in ['neonatal deaths', 'infant deaths'] else x['Measure Type'], axis = 1)

        indexNames = df[ df['Measurement 2'] == 'Males per 1,000 females' ].index
        df.drop(indexNames, inplace = True)
        indexNames = df[ df['Measurement 3'] == '% of live births' ].index
        df.drop(indexNames, inplace = True)

        trace.add_column('Vital Event')
        trace.Vital_Event("Replaces Temp Header 'Measurement'")
        trace.Vital_Event("Ignore 'males per 1,000 females' as it can be derived from the data")
        trace.Vital_Event("Ignore 'TO unmarried parents % of live births' as it can be derived from the data")

        df = df.drop(['Year', 'Quarter', 'DATAMARKER', 'Measurement 2', 'Measurement 3'], axis=1)

        df = df.rename(columns={'Measurement 1' : 'Vital Event', 'OBS' : 'Value', 'Gender' : 'Sex'})
        trace.Value("Rename 'Observations' column to 'Value' ")

        df = df[['Period', 'Vital Event', 'Sex', 'Parent Marital Status', 'Value', 'Measure Type', 'Unit']]

        tidied_tables[name] = df

    elif name.lower() == 'q2':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df['Gender'] = df.apply(lambda x: 'F' if 'Female' in x['Measurement 2'] else ('M' if 'Male' in x['Measurement 2'] else 'T'), axis = 1)
        df['Gender'] = df.apply(lambda x: 'T' if 'both sexes' in x['Measurement 2'].lower() else x['Gender'], axis = 1)
        df['Gender'] = df.apply(lambda x: 'T' if 'Marriages' in x['Measurement 1'] else x['Gender'], axis = 1)
        trace.Sex("Replace 'Females' with 'F', 'Males' with 'M' and 'T' otherwise where appropriate")

        df['Area'] = df.apply(lambda x: x['Area'].strip(), axis = 1)

       	indexNames = df[ df['Area'].isin(['Council areas','NHS Board areas'])].index
        df.drop(indexNames, inplace = True)

        df['Area'] = df.apply(lambda x: x['Area'] + ' ' + x['Area Type'], axis = 1)

        df = df.replace({'Measurement 1' : {
            'Deaths' : 'Deaths - all ages',
            'Marriages ' : 'Marriages'},
                        'Area' : {
            'Aberdeen City Council areas': 'S12000033',
            'Aberdeenshire Council areas' : 'S12000034',
            'Angus Council areas' : 'S12000041',
            'Argyll and Bute Council areas' : 'S12000035',
            'Ayrshire and Arran NHS Board areas' : 'S08000015',
            'Borders NHS Board areas' : 'S08000016',
            'City of Edinburgh Council areas' : 'S12000036',
            'Clackmannanshire Council areas' : 'S12000005',
            'Dumfries and Galloway Council areas' : 'S12000006',
            'Dumfries and Galloway NHS Board areas' : 'S08000017',
            'Dundee City Council areas' : 'S12000042',
            'East Ayrshire Council areas' : 'S12000008',
            'East Dunbartonshire Council areas' : 'S12000045',
            'East Lothian Council areas' : 'S12000010',
            'East Renfrewshire Council areas' : 'S12000011',
            'Falkirk Council areas' : 'S12000014',
            'Fife Council areas' : 'S12000047',
            'Fife NHS Board areas' : 'S08000029',
            'Forth Valley NHS Board areas' : 'S08000019',
            'Glasgow City Council areas' : 'S12000049',
            'Grampian NHS Board areas' : 'S08000020',
            'Greater Glasgow and Clyde NHS Board areas' : 'S08000031',
            'Highland Council areas' : 'S12000017',
            'Highland NHS Board areas' : 'S08000022',
            'Inverclyde Council areas' : 'S12000018',
            'Lanarkshire NHS Board areas' : 'S08000032',
            'Lothian NHS Board areas' : 'S08000024',
            'Midlothian Council areas' : 'S12000019',
            'Moray Council areas' : 'S12000020',
            'Na h-Eileanan Siar Council areas' : 'S12000013',
            'North Ayrshire Council areas' : 'S12000021',
            'North Lanarkshire Council areas' : 'S12000050',
            'Orkney Islands Council areas' : 'S12000023',
            'Orkney NHS Board areas' : 'S08000025',
            'Perth and Kinross Council areas' : 'S12000048',
            'Renfrewshire Council areas' : 'S12000038',
            'SCOTLAND ' : 'S92000003',
            'Scottish Borders Council areas' : 'S12000026',
            'Shetland Islands Council areas' : 'S12000027',
            'Shetland NHS Board areas' : 'S08000026',
            'South Ayrshire Council areas' : 'S12000028',
            'South Lanarkshire Council areas' : 'S12000029',
            'Stirling Council areas' : 'S12000030',
            'Tayside NHS Board areas' : 'S08000030',
            'West Dunbartonshire Council areas' : 'S12000039',
            'West Lothian Council areas' : 'S12000040',
            'Western Isles NHS Board areas' : 'S08000028'}})
        
        trace.Area('Replace Council Area and NHS Board areas with corresponding Codes')
        
        trace.add_column('Vital Event')
        trace.Vital_Event("Replaces Temp Header 'Measurement'")
        trace.Vital_Event("Replace 'Deaths' with 'Deaths - all ages'")

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")

        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 population' if 'rate' in x['Measurement 2'].lower() or 'rate' in x['Measurement 3'].lower() else 'count', axis = 1)
        df['Unit'] = df.apply(lambda x: 'births' if 'live births' in x['Measurement 1'].lower() else 'deaths', axis = 1)

        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 live and still births' if 'rate' in x['Measure Type'] and x['Measurement 1'].lower() in ['stillbirths', 'perinatal deaths'] else x['Measure Type'], axis = 1)
        df['Measure Type'] = df.apply(lambda x: 'rate per 1000 live births' if 'rate' in x['Measure Type'] and x['Measurement 1'].lower() in ['neonatal deaths', 'infant deaths'] else x['Measure Type'], axis = 1)

        df['Parent Marital Status'] = 'all'
        trace.add_column('Parent Marital Status')
        trace.Parent_Marital_Status("All value 'all' to every row")

        df = df.drop(['Measurement 2', 'Measurement 3', 'Area Type', 'DATAMARKER'], axis=1)

        df = df.rename(columns={'Measurement 1' : 'Vital Event', 'OBS' : 'Value', 'Gender' : 'Sex'})

        df = df[['Period', 'Area', 'Vital Event', 'Parent Marital Status', 'Sex', 'Value', 'Measure Type', 'Unit']]

        tidied_tables[name] = df

    elif name.lower() == 'q3':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df['Area'] = df.apply(lambda x: x['Area'].strip(), axis = 1)
        df['Area Type'] = df.apply(lambda x: x['Area Type'].replace(' 2', ''), axis = 1)
       	indexNames = df[ df['Area'].isin(['Council areas','NHS Board areas'])].index
        df.drop(indexNames, inplace = True)
        df['Area'] = df.apply(lambda x: x['Area'] + ' ' + x['Area Type'], axis = 1)

        df = df.replace({'Area' : {
            'Aberdeen City Council areas': 'S12000033',
            'Aberdeenshire Council areas' : 'S12000034',
            'Angus Council areas' : 'S12000041',
            'Argyll and Bute Council areas' : 'S12000035',
            'Ayrshire and Arran NHS Board areas' : 'S08000015',
            'Borders NHS Board areas' : 'S08000016',
            'City of Edinburgh Council areas' : 'S12000036',
            'Clackmannanshire Council areas' : 'S12000005',
            'Dumfries and Galloway Council areas' : 'S12000006',
            'Dumfries and Galloway NHS Board areas' : 'S08000017',
            'Dundee City Council areas' : 'S12000042',
            'East Ayrshire Council areas' : 'S12000008',
            'East Dunbartonshire Council areas' : 'S12000045',
            'East Lothian Council areas' : 'S12000010',
            'East Renfrewshire Council areas' : 'S12000011',
            'Falkirk Council areas' : 'S12000014',
            'Fife Council areas' : 'S12000047',
            'Fife NHS Board areas' : 'S08000029',
            'Forth Valley NHS Board areas' : 'S08000019',
            'Glasgow City Council areas' : 'S12000049',
            'Grampian NHS Board areas' : 'S08000020',
            'Greater Glasgow and Clyde NHS Board areas' : 'S08000031',
            'Highland Council areas' : 'S12000017',
            'Highland NHS Board areas' : 'S08000022',
            'Inverclyde Council areas' : 'S12000018',
            'Lanarkshire NHS Board areas' : 'S08000032',
            'Lothian NHS Board areas' : 'S08000024',
            'Midlothian Council areas' : 'S12000019',
            'Moray Council areas' : 'S12000020',
            'Na h-Eileanan Siar Council areas' : 'S12000013',
            'North Ayrshire Council areas' : 'S12000021',
            'North Lanarkshire Council areas' : 'S12000050',
            'Orkney Islands Council areas' : 'S12000023',
            'Orkney NHS Board areas' : 'S08000025',
            'Perth and Kinross Council areas' : 'S12000048',
            'Renfrewshire Council areas' : 'S12000038',
            'SCOTLAND ' : 'S92000003',
            'Scottish Borders Council areas' : 'S12000026',
            'Shetland Islands Council areas' : 'S12000027',
            'Shetland NHS Board areas' : 'S08000026',
            'South Ayrshire Council areas' : 'S12000028',
            'South Lanarkshire Council areas' : 'S12000029',
            'Stirling Council areas' : 'S12000030',
            'Tayside NHS Board areas' : 'S08000030',
            'West Dunbartonshire Council areas' : 'S12000039',
            'West Lothian Council areas' : 'S12000040',
            'Western Isles NHS Board areas' : 'S08000028'},
                        'Age' : {
            '0.0' : '0',
            'All ages' : 'All'}})

        trace.Area('Replace Council Area and NHS Board areas with corresponding Codes')

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")

        df['Cause of Death'] = 'all'
        trace.add_column('Cause of Death')
        trace.Cause_of_Death("Replace Measurement column with Cause of Death - filled with 'All'")

        df['Age'] = df.apply(lambda x: x['Age'].replace('+', ' Plus'), axis = 1)
        trace.Age("Replace + with Plus")

        df = df.drop(['Area Type', 'DATAMARKER', 'Measurement'], axis=1)

        df = df.rename(columns={'OBS' : 'Value','Gender' : 'Sex'})

        df = df[['Period', 'Area', 'Age', 'Sex', 'Cause of Death', 'Value']]

        tidied_tables[name] = df

    elif name.lower() == 'q4':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        path = pathlib.PurePath(dist.downloadURL)
        quarter = left(path.name.replace('quarter-', ''), 1)

        df['Period'] = df.apply(lambda x: 'quarter/'+left(str(x['Period']), 4)+'-Q'+quarter, axis = 1)
        df['ICD 10 Summary List'] = df.apply(lambda x: x['ICD 10 Summary List'].strip(), axis = 1)

        df = df.drop(['Cause of Death'], axis=1)
        trace.Cause_of_Death("Replace Cause of Death values with ICD 10 Summary values and drop ICD 10 column")

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")

        df = df.rename(columns={'OBS' : 'Value', 'ICD 10 Summary List' : 'Cause of Death'})

        df['Sex'] = 'T'
        df['Age'] = 'all'
        df['Area'] = 'S92000003'
        trace.add_column("Sex")
        trace.Sex("Fill values with T")
        trace.add_column("Age")
        trace.Age("Fill values with all")
        trace.add_column("Area")
        trace.Area("Fill values with S92000003 - Scotland country code")

        df = df.replace({'Cause of Death' : {'' : 'all'}})

        df = df[['Period', 'Area',  'Age', 'Sex', 'Cause of Death', 'Value']]

        tidied_tables[name] = df

    elif name.lower() == 'q5':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df = df.replace({'Age' : {'<4' : 'Less than 4 Weeks',
                                  '4-' : 'Between 4 Weeks and 1 Year',
                                  'All Ages' : 'All'},
                         'Gender' : {'All' : 'T'},
                         'ICD 10 Summary List' : {'' : 'all'}})

        trace.Age("Replace '<4' with 'Less than 4 Weeks'")
        trace.Age("Replace '4-' with 'Between 4 Weeks and 1 Year'")
        trace.Age("Replace 'All Ages' with 'All'")
        trace.Sex("Replace 'All' with 'T'")

        path = pathlib.PurePath(dist.downloadURL)
        quarter = left(path.name.replace('quarter-', ''), 1)

        df['Age'] = df.apply(lambda x: x['Age'].replace('+', ' Plus'), axis = 1)
        trace.Age("Replace + with Plus")

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")

        df['Area'] = 'S92000003'
        trace.add_column("Area")
        trace.Area("Add 'S92000003' - Scotland Country code - to every row")

        df['Period'] = df.apply(lambda x: 'quarter/' + x['Period'] + '-Q' + quarter, axis = 1)

        df = df.drop(['Cause of Death', 'DATAMARKER'], axis=1)

        df = df.rename(columns={'OBS' : 'Value', 'ICD 10 Summary List' : 'Cause of Death', 'Gender' : 'Sex'})
        trace.Cause_of_Death("Replace Cause of Death values with ICD 10 Summary values and drop ICD 10 column")

        df = df[['Period', 'Area', 'Age', 'Sex', 'Cause of Death', 'Value']]

        tidied_tables[name] = df

    elif name.lower() == 'q6':

        df = trace.combine_and_trace(datasetTitle, name).fillna('')

        df = df.replace({'Area' : {
            'Ayrshire and Arran' : 'S08000015',
            'Borders' : 'S08000016',
            'Dumfries and Galloway' : 'S08000017',
            'Fife' : 'S08000029',
            'Forth Valley' : 'S08000019',
            'Grampian' : 'S08000020',
            'Scotland' : 'S92000003'},
                        'Gender' : {'All' : 'T'},
                        'ICD 10 Summary List' : {'' : 'all'}})
        trace.Area("Replace area names with area codes")

        df['OBS'] = df.apply(lambda x: 0 if '-' in x['DATAMARKER'].lower() else x['OBS'], axis = 1)
        trace.Value("Replace - DATAMARKER values with '0'")

        df['Age'] = 'all'
        trace.add_column("Age")
        trace.Age("Add value 'all'")

        path = pathlib.PurePath(dist.downloadURL)
        quarter = left(path.name.replace('quarter-', ''), 1)
        df['Period'] = df.apply(lambda x: 'quarter/' + x['Period'] + '-Q' + quarter, axis = 1)

        df = df.drop(['Cause of Death', 'DATAMARKER'], axis=1)
        df = df.rename(columns={'OBS' : 'Value', 'ICD 10 Summary List' : 'Cause of Death', 'Gender' : 'Sex'})
        trace.Cause_of_Death("Replace Cause of Death values with ICD 10 Summary values and drop ICD 10 column")

        df = df[['Period', 'Area', 'Age', 'Sex', 'Cause of Death', 'Value']]

        tidied_tables[name] = df


# In[ ]:


cubes = Cubes("info.json")


# In[ ]:


#Stage 2 Alignment - Dataset One

datasetOne = tidied_tables['Q1'][tidied_tables['Q1']['Vital Event'].isin(['Live births', 'Stillbirths', 'Perinatal deaths', 'Infant deaths', 'Neonatal deaths'])].append(tidied_tables['Q2'][tidied_tables['Q2']['Vital Event'].isin(['Live births', 'Stillbirths', 'Perinatal deaths', 'Infant deaths', 'Neonatal deaths'])], sort = False).fillna('S92000003')
datasetOne = datasetOne[datasetOne['Measure Type'].isin(['count'])]
datasetOne = datasetOne[['Period', 'Area', 'Vital Event', 'Sex', 'Parent Marital Status', 'Value', 'Measure Type', 'Unit']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Period', 'Value']

for col in datasetOne.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		datasetOne[col] = datasetOne[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

scrape.dataset.title = 'Births, deaths, and other vital events, Quarterly figures - Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths'
scrape.dataset.comment = 'Quarterly figures for Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths'
scrape.dataset.description = """Quarterly figures for Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths
		About this data
		https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-about.pdf"""
scrape.dataset.family = 'covid-19'
scrape.dataset.issued = dist.issued

cubes.add_cube(scrape, datasetOne, scrape.dataset.title)

datasetOne


# In[ ]:


#Stage 2 Alignment - Dataset Two

datasetTwo = tidied_tables['Q1'][tidied_tables['Q1']['Vital Event'].isin(['Civil Partnerships ', 'Deaths - all ages', 'Marriages'])].append(tidied_tables['Q2'][tidied_tables['Q2']['Vital Event'].isin(['Civil Partnerships ', 'Deaths - all ages', 'Marriages'])], sort = False).fillna('S92000003')
datasetTwo['Unit'] = datasetTwo.apply(lambda x: 'marriages' if 'marriages' in x['Vital Event'].lower() else ('civil partnership' if 'civil partnerships' in x['Vital Event'].lower() else x['Unit']), axis = 1)
datasetTwo = datasetTwo[datasetTwo['Measure Type'].isin(['count'])]
datasetTwo = datasetTwo[['Period', 'Vital Event', 'Sex', 'Area', 'Value']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Period', 'Value']

for col in datasetTwo.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		datasetTwo[col] = datasetTwo[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

scrape.dataset.title = 'Births, deaths, and other vital events, Quarterly figures - Deaths, Marriages & Civil Partnerships'
scrape.dataset.comment = 'Quarterly figures for Deaths, Marriages & Civil Partnerships'
scrape.dataset.description = """Quarterly figures for Deaths, Marriages & Civil Partnerships
		About this data
		https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-about.pdf"""
scrape.dataset.family = 'covid-19'
scrape.dataset.issued = dist.issued

cubes.add_cube(scrape, datasetTwo, scrape.dataset.title)

datasetTwo


# In[ ]:


#Stage 2 Alignment - Dataset Three

datasetThree = tidied_tables['Q2'][tidied_tables['Q2']['Vital Event'] == 'Estimated population at 30 June 2019']
datasetThree = datasetThree.drop(['Vital Event'], axis=1)
datasetThree = datasetThree[['Period', 'Area', 'Sex', 'Value']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

for col in datasetThree.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		datasetThree[col] = datasetThree[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

scrape.dataset.title = 'Births, deaths, and other vital events, Quarterly figures - Estimated Population by Sex and Council Area'
scrape.dataset.comment = 'Quarterly figures for estimated population by sex and Council Area'
scrape.dataset.description = """Quarterly figures for estimated population by sex and Council Area
		About this data
		https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-about.pdf"""
scrape.dataset.family = 'covid-19'
scrape.dataset.issued = dist.issued

cubes.add_cube(scrape, datasetThree, scrape.dataset.title)

datasetThree


# In[ ]:


#Stage 2 Alignment - Dataset Four

datasetFour = pd.concat([tidied_tables['Q3'], tidied_tables['Q4'], tidied_tables['Q5'], tidied_tables['Q6']])
datasetFour = datasetFour[['Period', 'Area', 'Age', 'Sex', 'Cause of Death', 'Value']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

for col in datasetFour.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		datasetFour[col] = datasetFour[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

scrape.dataset.title = 'Births, deaths, and other vital events, Quarterly figures - Deaths by Age, Sex, Cause of Death and Administrative Area'
scrape.dataset.comment = 'Quarterly figures for Deaths by Age, Sex, Cause of Death and Administrative Area'
scrape.dataset.description = """Quarterly figures for Deaths by Age, Sex, Cause of Death and Administrative Area
		About this data
		https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-about.pdf"""
scrape.dataset.family = 'covid-19'
scrape.dataset.issued = dist.issued

cubes.add_cube(scrape, datasetFour, scrape.dataset.title)

datasetFour


# In[ ]:


trace.render("spec_v1.html")
cubes.output_all()


# In[ ]:




