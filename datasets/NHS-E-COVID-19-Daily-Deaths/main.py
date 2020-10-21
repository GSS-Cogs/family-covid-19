#!/usr/bin/env python
# coding: utf-8

# In[491]:


#!/usr/bin/env python
# coding: utf-8


# In[492]:



from gssutils import *
import json
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import string


# In[493]:


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def extractMaximum(ss):
    num, res = 0, 0

    # start traversing the given string
    for i in range(len(ss)):

        if ss[i] >= "0" and ss[i] <= "9":
            num = num * 10 + int(int(ss[i]) - 0)
        else:
            res = max(res, num)
            num = 0

    return max(res, num)

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
        coordinate = right(str(cell).split()[0], len(str(cell).split()[0]) - 2)
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

    return '{' + lowy + lowx + '-' + highy + highx + '}'


# In[494]:




#scraper = Scraper(landingPage)
#scraper

#dist = scraper.distributions[0]
#dist

#No currently usable scraper, dataURL changes too often to make good use of seed(info.json)


# In[495]:


dataLinks = []

parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen(landingPage)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

for link in soup.find_all('a', href=True):
    if not "total announced" in link.text:continue
    dataLinks.append(link['href'])

for i in dataLinks:
    print(i)


# In[496]:



trace = TransformTrace()


# In[497]:



for link in dataLinks:
    urllib.request.urlretrieve(link, "data.xlsx")
    tabs = loadxlstabs("data.xlsx")
    for tab in tabs:

        dailyDeaths ='NHS COVID-19 Daily Deaths'

        if 'deaths by trust' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('NHS England Region'))
            pivot = right(left(str(cell), 6),4).strip()

            region = cell.fill(DOWN).is_not_blank()
            trace.ONS_Geography_Code('Selected as non-blank values in range: {}', var = excelRange(region))

            code = cell.shift(2, 0).fill(DOWN).is_not_blank()
            trace.NHS_Hospital_Code('Selected as non-blank values in range: {}', var = excelRange(code))

            period = cell.shift(4, 0).expand(RIGHT).is_not_blank()
            trace.Period('Selected as non-blank values in range: {}', var = excelRange(period))

            age = 'All'
            trace.Age('Hardcoded as {}', var = age)

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = 'All'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            measureType = 'Deaths Positive Test'
            trace.Measure_Type('Hardcoded as {}', var = measureType)

            unit = 'Count'
            trace.Unit('Hardcoded as {}', var = unit)

            observations = period.fill(DOWN).is_not_blank()

            dimensions = [
                    HDim(region, 'ONS Geography Code', DIRECTLY, LEFT),
                    HDim(code, 'NHS Hospital Code', DIRECTLY, LEFT),
                    HDim(period, 'Period', DIRECTLY, ABOVE),
                    HDimConst('Age', age),
                    HDimConst('Sex', sex),
                    HDimConst('Ethnicity', ethnicity),
                    HDimConst('Pre-existing Condition' , condition),
                    HDimConst('Pre-existing Condition Status' , conditionStatus),
                    HDimConst('Measure Type', measureType), #change to 'Deaths Awaiting Verification' for 'Awaiting Verification' Period
                    HDimConst('Unit', unit)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        elif 'deaths by region' in tab.name.lower() or 'no post testFINE' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('NHS England Region'))

            region = cell.fill(DOWN).is_not_blank()
            trace.ONS_Geography_Code('Selected as non-blank values in range: {}', var = excelRange(region))

            code = 'All'
            trace.NHS_Hospital_Code('Hardcoded as {}', var = code)

            period = cell.shift(RIGHT).expand(RIGHT).is_not_blank()
            trace.Period('Selected as non-blank values in range: {}', var = excelRange(period))

            age = 'All'
            trace.Age('Hardcoded as {}', var = age)

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = 'All'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            unit = 'Count'
            trace.Unit('Hardcoded as {}', var = unit)

            if 'deaths by region' in tab.name.lower():
                measureType = 'Deaths Positive Test'
            elif 'no post test' in tab.name.lower():
                measureType = 'Deaths No Positive Test'
            else:
                'ERROR CHECK TAB NAME'

            trace.Measure_Type('Variable based on tab name, currently: {}', var = measureType)

            observations = region.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDim(region, 'ONS Geography Code', DIRECTLY, LEFT),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', DIRECTLY, ABOVE),
                    HDimConst('Age', age),
                    HDimConst('Sex', sex),
                    HDimConst('Ethnicity', ethnicity),
                    HDimConst('Pre-existing Condition' , condition),
                    HDimConst('Pre-existing Condition Status' , conditionStatus),
                    HDimConst('Measure Type', measureType), #change to 'Deaths Awaiting Verification' for 'Awaiting Verification' Period
                    HDimConst('Unit', unit)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        elif 'deaths by age' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('Up to 01-Mar-20')).shift(-2,0)

            region = 'E92000001'
            trace.ONS_Geography_Code('Hardcoded as {}', var = region)

            code = 'All'
            trace.NHS_Hospital_Code('Hardcoded as {}', var = code)

            period = cell.shift(RIGHT).expand(RIGHT).is_not_blank()
            trace.Period('Selected as non-blank values in range: {}', var = excelRange(period))

            age = cell.fill(DOWN).is_not_blank()
            trace.Age('Selected as non-blank values in range: {}', var = excelRange(age))

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = 'All'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            measureType = 'Deaths Positive Test'
            trace.Measure_Type('Hardcoded as {}', var = measureType)

            unit = 'Count'
            trace.Unit('Hardcoded as {}', var = unit)

            observations = age.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDimConst('ONS Geography Code', region),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', DIRECTLY, ABOVE),
                    HDim(age, 'Age', DIRECTLY, LEFT),
                    HDimConst('Sex', sex),
                    HDimConst('Ethnicity', ethnicity),
                    HDimConst('Pre-existing Condition' , condition),
                    HDimConst('Pre-existing Condition Status' , conditionStatus),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        elif 'deaths by ethnicity' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('Count')).shift(-2, 0)

            region = 'E92000001'
            trace.ONS_Geography_Code('Hardcoded as {}', var = region)

            code = 'All'
            trace.NHS_Hospital_Code('Hardcoded as {}', var = code)

            period = tab.filter('Period:').shift(RIGHT)
            trace.Period('Single Date given for whole sheet, located: {}', var = excelRange(period))

            age = 'All'
            trace.Age('Hardcoded as {}', var = age)

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = cell.fill(DOWN).is_not_blank()
            trace.Ethnicity('Selected as non-blank values in range: {}', var = excelRange(ethnicity))
            #THIS CURRENTLY EXCLUDES SOME 'TOTAL' ROWS FOR EACH ETHNICITY, I can't find a way to replace the whitespace for each column heading
            #reliably that wouldn't risk data accuracy if anything in the table was changed, and this dataset is updated very often
            #This is probably not an issue since the Total rows don't add any information and are just additions of other rows (but if someone see's this and knows some tricks go for it

            conditionStatus = 'All'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            measureType = 'Deaths Positive Test'
            trace.Measure_Type('Hardcoded as {}', var = measureType)

            unit = cell.shift(RIGHT).expand(RIGHT).is_not_blank()
            trace.Unit('Selected as non-blank values in range: {}', var = excelRange(unit))

            observations = ethnicity.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDimConst('ONS Geography Code', region),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDimConst('Age', age),
                    HDimConst('Sex', sex),
                    HDim(ethnicity, 'Ethnicity', DIRECTLY, LEFT),
                    HDimConst('Pre-existing Condition' , condition),
                    HDimConst('Pre-existing Condition Status' , conditionStatus),
                    HDimConst('Measure Type', measureType),
                    HDim(unit, 'Unit', DIRECTLY, ABOVE)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())


        elif 'deaths by gender' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('Female')).shift(-2, 0)

            region = 'E92000001'
            trace.ONS_Geography_Code('Hardcoded as {}', var = region)

            code = 'All'
            trace.NHS_Hospital_Code('Hardcoded as {}', var = code)

            period = tab.filter('Period:').shift(RIGHT)
            trace.Period('Single Date given for whole sheet, located: {}', var = excelRange(period))

            age = cell.fill(DOWN).is_not_blank()
            trace.Age('Selected as non-blank values in range: {}', var = excelRange(age))

            sex = cell.expand(RIGHT).is_not_blank()
            trace.Sex('Selected as non-blank values in range: {}', var = excelRange(sex))

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = 'All'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            measureType = 'Deaths Positive Test'
            trace.Measure_Type('Hardcoded as {}', var = measureType)

            unit = 'Count'
            trace.Unit('Hardcoded as {}', var = unit)

            observations = age.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDimConst('ONS Geography Code', region),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(age, 'Age', DIRECTLY, LEFT),
                    HDim(sex, 'Sex', DIRECTLY, ABOVE),
                    HDimConst('Ethnicity', ethnicity),
                    HDimConst('Pre-existing Condition' , condition),
                    HDimConst('Pre-existing Condition Status' , conditionStatus),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        elif 'deaths by condition' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('Yes')).shift(-2, 0)

            region = 'E92000001'
            trace.ONS_Geography_Code('Hardcoded as {}', var = region)

            code = 'All'
            trace.NHS_Hospital_Code('Hardcoded as {}', var = code)

            period = tab.filter('Period:').shift(RIGHT)
            trace.Period('Single Date given for whole sheet, located: {}', var = excelRange(period))

            age = cell.fill(DOWN).is_not_blank()
            trace.Age('Selected as non-blank values in range: {}', var = excelRange(age))

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = cell.expand(RIGHT).is_not_blank()
            trace.Preexisting_Condition_Status('Selected as non-blank values in range: {}', var = excelRange(conditionStatus))

            condition = 'All'
            trace.Preexisting_Condition('Hardcoded as {}', var = condition)

            measureType = 'Deaths Positive Test'
            trace.Measure_Type('Hardcoded as {}', var = measureType)

            unit = 'Count'
            trace.Unit('Hardcoded as {}', var = unit)

            observations = age.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDimConst('ONS Geography Code', region),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(age, 'Age', DIRECTLY, LEFT),
                    HDimConst('Sex', sex),
                    HDimConst('Ethnicity', ethnicity),
                    HDimConst('Pre-existing Condition' , condition),
                    HDim(conditionStatus, 'Pre-existing Condition Status', DIRECTLY, ABOVE),
                    HDimConst('Measure Type', measureType),
                    HDimConst('Unit', unit)
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        elif 'deaths by cond (detail)' in tab.name.lower():

            columns=["Period", "ONS Geography Code", "NHS Hospital Code", "Age", "Sex", "Ethnicity", "Preexisting Condition", "Preexisting Condition Status", "Measure Type", "Unit"]
            trace.start(dailyDeaths, tab, columns, link)

            cell = tab.filter(contains_string('Date introduced'))

            remove = tab.filter(contains_string('Notes:')).expand(RIGHT).expand(DOWN)

            region = 'E92000001'
            trace.Sex('Hardcoded as {}', var = code)

            code = 'All'
            trace.ONS_Geography_Code('Hardcoded as {}', var = code)

            period = cell.fill(DOWN).is_not_blank() - remove
            trace.Period('Selected as non-blank values in range: {}', var = excelRange(period))

            age = 'All'
            trace.Age('Hardcoded as {}', var = age)

            sex = 'All'
            trace.Sex('Hardcoded as {}', var = sex)

            ethnicity = 'All'
            trace.Ethnicity('Hardcoded as {}', var = ethnicity)

            conditionStatus = 'Yes'
            trace.Preexisting_Condition_Status('Hardcoded as {}', var = conditionStatus)

            condition = period.shift(RIGHT)
            trace.Preexisting_Condition('Selected as non-blank values in range: {}', var = excelRange(condition))

            measureType = cell.shift(RIGHT).fill(RIGHT).is_not_blank()
            trace.Measure_Type('Selected as non-blank values in range: {}', var = excelRange(measureType))

            unit = cell.shift(RIGHT).fill(RIGHT).is_not_blank()
            trace.Unit('Selected as non-blank values in range: {}', var = excelRange(unit))

            observations = condition.fill(RIGHT).is_not_blank()

            dimensions = [
                    HDimConst('ONS Geography Code', region),
                    HDimConst('NHS Hospital Code', code),
                    HDim(period, 'Period', DIRECTLY, LEFT),
                    HDimConst('Age', age),
                    HDimConst('Sex', sex),
                    HDimConst('Ethnicity', ethnicity),
                    HDim(condition, 'Pre-existing Condition', DIRECTLY, LEFT),
                    HDimConst( 'Pre-existing Condition Status', conditionStatus),
                    HDim(measureType, 'Measure Type', DIRECTLY, ABOVE),
                    HDim(unit, 'Unit', DIRECTLY, ABOVE),
            ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("dailyDeaths", tidy_sheet.topandas())

        else:
            continue


# In[498]:


dailyDeathsDf = trace.combine_and_trace(dailyDeaths, "dailyDeaths").fillna('')

#dailyDeathsDf['Period'] = dailyDeathsDf.apply(lambda x: datetime.strptime(right(x['Period'], (len(x['Period']) - 19)), '%d %B %Y').strftime('%Y-%m-%d') if x['Period'].startswith('All data up to') else x['Period'], axis = 1)
#This is a terrible solution, but them using "all data up to" etc as the period is also terrible

dailyDeathsDf['Measure Type'] = dailyDeathsDf.apply(lambda x: 'Deaths Awaiting Verification' if 'Awaiting verification' in str(x['Period']) else x['Measure Type'], axis = 1)
dailyDeathsDf['Measure Type'] = dailyDeathsDf.apply(lambda x: 'Percentage' if 'Percentage' in x['Unit'] and 'null' not in x['Unit'] else x['Measure Type'], axis = 1)
dailyDeathsDf['Measure Type'] = dailyDeathsDf.apply(lambda x: 'Percentage without Null and not stated' if 'Percentage' in x['Unit'] and 'null' in x['Unit'] else x['Measure Type'], axis = 1)

trace.Measure_Type('Change to Percentage for Percentage values using column headers as reference')

dailyDeathsDf['Unit'] = dailyDeathsDf.apply(lambda x: 'Percent' if 'Percentage' in x['Measure Type'] else x['Unit'], axis = 1)

trace.Unit('Change to Percent where Measure Type is changed to Percentage')

indexNames = dailyDeathsDf[ dailyDeathsDf['Period'].isin(['Awaiting verification','Up to 01-Mar-20','Total', 'All data up to 4pm 14 October 2020', 'All data up to 5pm 9 June 2020'])].index
dates = dailyDeathsDf['Period'].drop(indexNames)
#intervalOfOrderPeriods = days_between(max(dates), min(dates))
#dailyDeathsDf['Period'] = dailyDeathsDf.apply(lambda x: 'gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Total' in x['Period'] else ('gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Awaiting verification' in x['Period'] else x['Period']), axis = 1)

trace.Period('Chance Total Period to be full range of dates')

dailyDeathsDf = dailyDeathsDf.replace({'ONS Geography Code' : {
        'England' : 'E92000001',
		'London' : 'E12000007',
		'Midlands' : 'E40000008',
		'North East and Yorkshire' : 'E40000009',
        'North East And Yorkshire' : 'E40000009',
        'East of England' : 'E12000006',
		'North West' : 'E12000002',
		'South East' : 'E40000005',
		'South West' : 'E32000013'},
                                    'Unit' : {
        'Percentage (excluding null and not stated)' : 'Percent',
        '% of deaths (excluding unknown or not reported) with condition' : 'Percent',
        '% of deaths since introduced with condition' : 'Percent',
        'Count of all deaths since condition introduced' : 'Count',
        'Count of condition' : 'Count',
        'Count of unknown or not reported for condition' : 'Count'},
                                    'Pre-existing Condition' : {
        'Count of condition' : 'With Condition',
        'Count of unknown or not reported for condition' : 'unknown or not reported',
        'Count of all deaths since condition introduced' : 'Deaths since Condition Introduced',
        '% of deaths since introduced with condition' : 'Deaths since Condition Introduced',
        '% of deaths (excluding unknown or not reported) with condition' : 'Deaths excluding unknown or not reported'}})

dailyDeathsDf['OBS'] = dailyDeathsDf.apply(lambda x: x['OBS']*100 if 'Percent' in x['Unit'] else x['OBS'], axis = 1)

trace.ONS_Geography_Code('Replace location names with Geography Codes')

trace.Unit("Replace 'Percentage (excluding null and not stated)' with 'Percent'")

trace.Preexisting_Condition("Replace 'Count of condition' with 'With Condition'")
trace.Preexisting_Condition("Replace 'Count of unknown or not reported for condition' with 'unknown or not reported'")
trace.Preexisting_Condition("Replace 'Count of all deaths since condition introduced' with 'Deaths since Condition Introduced'")
trace.Preexisting_Condition("Replace '% of deaths since introduced with condition' with'Deaths since Condition Introduced'")
trace.Preexisting_Condition("Replace '% of deaths (excluding unknown or not reported) with condition' with 'Deaths excluding unknown or not reported'")


# In[499]:


from IPython.core.display import HTML
for col in dailyDeathsDf:
    if col not in ['Value']:
        dailyDeathsDf[col] = dailyDeathsDf[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(dailyDeathsDf[col].cat.categories)


# In[500]:


out = Path('out')
out.mkdir(exist_ok=True)

dailyDeathsTitle = pathify(dailyDeaths)

import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

dailyDeathsDf.drop_duplicates().to_csv(out / f'{dailyDeathsTitle}.csv', index = False)

trace.output()

