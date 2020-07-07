#!/usr/bin/env python
# coding: utf-8

# In[54]:


# # ONS Coronavirus  COVID-19  related deaths by occupation, England and Wales  deaths registered up to and including 20 April 2020 

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


# In[55]:


scraper = Scraper(landingPage) 
scraper


# In[56]:


distribution = scraper.distributions[0]
display(distribution)


# In[57]:


trace = TransformTrace()

tabs = { tab: tab for tab in distribution.as_databaker() }

tidied_sheets = []

datasetTitle = 'Coronavirus (COVID-19) related deaths by occupation'
link = distribution.downloadURL

with open('info.json') as info:
    data = info.read()

infoData = json.loads(data)

infoData['transform']['transformStage'] = {}

for tab in tabs:

    if tab.name.lower() in ['table 1', 'table 15', 'table 22']: 
        #leave table 2 for now, come back to it later, tables 10,11,12 arent deaths stats, but numbers of people in industries, not sure if applicable. table 21 is based on       deprivation which I'm also not sure how/whether to include

        datasetTitle = 'Coronavirus (COVID-19) related deaths by occupation'

        columns = ['Period','ONS Geography Code','Sex','Age' ,'Occupation', 'Standard Occupation Classification','Cause of Death','Rate','Lower CI','Upper CI','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        cell = tab.filter(contains_string('Cause of death'))

        remove = tab.filter(contains_string('Source:')).shift(UP).expand(RIGHT).expand(LEFT).expand(DOWN)

        pivot = cellLoc(cell)

        cod = cell.fill(DOWN).is_not_blank() - remove
        trace.Cause_of_Death('Cause of Death for Tab given at cell range: {}', var = excelRange(cod))

        period = right(cellCont(str(tab.excel_ref('B1'))), 29).strip()
        trace.Period('Period range for Tab: {}', var = period)

        if tab.name.lower() in ['table 15']:
            region = 'england'
        elif tab.name.lower() in ['table 22']:
            region = 'wales'
        else:
            region = 'england and wales'
        trace.ONS_Geography_Code('Region for Tab hardcoded as: {}', var = region)

        soc = 'all'
        trace.Standard_Occupation_Classification('Hardcoded as: {}', var = soc)

        occupation = 'all'
        trace.Occupation('Hardcoded as: {}', var = occupation)

        age = '20 - 64'
        trace.Age('Hardcoded as: {}', var = age)

        sex = cell.shift(1, -1).expand(RIGHT).is_not_blank()
        trace.Sex('Gender taken from range: {}', var = excelRange(sex))
        
        rate = tab.filter('Rate').fill(DOWN).is_not_blank() - remove
        trace.Rate('Rates taken from range: {}', var = excelRange(rate))

        lower = tab.filter('Lower CI').fill(DOWN).is_not_blank() - remove
        trace.Lower_CI('Lower CI taken from range: {}', var = excelRange(lower))

        upper = tab.filter('Upper CI').fill(DOWN).is_not_blank() - remove
        trace.Upper_CI('Upper CI taken from range: {}', var = excelRange(upper))
        
        observations = tab.filter('Deaths').fill(DOWN).is_not_blank() - remove

        measureType = 'Count'
        trace.Measure_Type('Hardcoded as:', var = measureType)

        unit = 'Person'
        trace.Unit('Hardcoded as:', var = unit)

        title = cellCont(str(tab.excel_ref('B1'))).split(',')[0]
        
        columnInfo = {}

        for i in columns:
            underI = i.replace(' ', '_')
            columnInfo[i] = getattr(getattr(trace, underI), 'var')

        dicti = {'name' : tab.name, 
                 'title' : title, 
                 'columns' : columnInfo}
        
        infoData['transform']['transformStage'][tab.name] = dicti

        with open('infoTransform.json', 'w') as info:
            info.write(json.dumps(infoData, indent=4))        

        dimensions = [
                    HDimConst('Period', period),
                    HDimConst('ONS Geography Code', region),
                    HDim(sex, 'Sex', CLOSEST, LEFT),
                    HDimConst('Age', age),
                    HDimConst('Occupation', occupation),
                    HDimConst('Standard Occupation Classification', soc), 
                    HDim(cod, 'Cause of Death', DIRECTLY, LEFT), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                    HDim(rate, 'Rate', DIRECTLY, RIGHT),
                    HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                    HDimConst('Measure Type', measureType), 
                    HDimConst('Unit', unit) 
            ]
            
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store("deathsByOccupation", tidy_sheet.topandas())
        

    elif tab.name.lower() in ['table 3', 'table 4', 'table 5', 'table 6a', 'table 6b', 'table 7', 'table 8', 'table 9', 'table 16', 'table 17', 'table 18', 'table 19', 'table 20', 'table 23', 'table 24']:

        datasetTitle = 'Coronavirus (COVID-19) related deaths by occupation'

        columns = ['Period','ONS Geography Code','Sex','Age' ,'Occupation', 'Standard Occupation Classification','Cause of Death','Rate','Lower CI','Upper CI','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)
        
        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            cell = tab.filter('Occupation group')
        elif tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            cell = tab.filter('Individual occupation')
        else:
            cell = tab.filter(contains_string('SOC'))

        if tab.name.lower() in ['table 3', 'table 4', 'table 6b', 'table 7', 'table 16', 'table 17', 'table 19', 'table 23', 'table 24']:
            remove = tab.filter(contains_string('Source:')).shift(UP).expand(RIGHT).expand(LEFT).expand(DOWN)
        else:
            remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(LEFT).expand(UP)

        pivot = cellLoc(cell)

        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            cod = cell.shift(1, -1).expand(RIGHT).is_not_blank() - remove
        elif tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            cod = cell.shift(2, 0).expand(RIGHT).is_not_blank() - remove
        else:
            cod = cell.shift(3, -1).expand(RIGHT).is_not_blank() - remove
        trace.Cause_of_Death('Cause of Death for Tab given in cell range: {}', var = excelRange(cod))

        period = right(cellCont(str(tab.excel_ref('B1'))), 29).strip()
        trace.Period('Period range for Tab: {}', var = period)

        if tab.name.lower() in ['table 16', 'table 17']:
            region = 'england'
        else:
            region = 'england and wales'
        trace.ONS_Geography_Code('Region for Tab hardcoded as: {}', var = region)

        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            soc = 'N/A'
            trace.Standard_Occupation_Classification('Standard Occupation Classification not Applicable for tab')
        else:
            soc = cell.fill(DOWN).is_not_blank() - remove
            trace.Standard_Occupation_Classification('Standard Occupation Classification given in cell range: {}', var = excelRange(soc))

        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            occupation = tab.filter('Occupation group').fill(DOWN).is_not_blank() - remove
        else:
            occupation = soc.shift(RIGHT)
        trace.Occupation('Occupation given in cell range: {}', var = excelRange(occupation))
   
        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            sex = cell.shift(1, -2).expand(RIGHT).is_not_blank()
        elif tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            sex = cell.shift(3, -1).expand(RIGHT).is_not_blank()
        else:
            sex = cell.shift(3, -2).expand(RIGHT).is_not_blank()
        trace.Sex('Gender given in range: ', var = excelRange(sex))

        if tab.name.lower() in ['table 9']:
            age = '65+'
        else:
            age = '20 - 64'
        trace.Age('Age hardcoded (given in cell title) as: ', var = excelRange(sex))
        
        if tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            rate = 'N/A'
            trace.Rate('Not Applicable for Tab')
        else:
            rate = tab.filter('Rate').fill(DOWN).is_not_blank() - remove
            trace.Rate('Rates taken from range: {}', var = excelRange(rate))

        if tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            lower = 'N/A'
            trace.Lower_CI('Not Applicable for Tab')
        else:
            lower = tab.filter('Lower CI').fill(DOWN).is_not_blank() - remove
            trace.Lower_CI('Lower CI given in range: ', var = excelRange(lower))

        if tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            upper = 'N/A'
            trace.Upper_CI('Not Applicable for Tab')
        else:
            upper = tab.filter('Upper CI').fill(DOWN).is_not_blank() - remove
            trace.Upper_CI('Upper CI given in range: ', var = excelRange(upper))
        
        if tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            observations = cod.fill(DOWN).is_not_blank() - remove 
        else:
            observations = tab.filter('Deaths').fill(DOWN).is_not_blank() - remove

        measureType = 'Count'
        trace.Measure_Type('Hardcoded as:', var = measureType)

        unit = 'Person'
        trace.Unit('Hardcoded as:', var = unit)

        title = cellCont(str(tab.excel_ref('B1'))).split(',')[0]

        columnInfo = {}

        for i in columns:
            underI = i.replace(' ', '_')
            columnInfo[i] = getattr(getattr(trace, underI), 'var')

        dicti = {'name' : tab.name, 
                 'title' : title, 
                 'columns' : columnInfo}
        
        infoData['transform']['transformStage'][tab.name] = dicti

        with open('infoTransform.json', 'w') as info:
            info.write(json.dumps(infoData, indent=4)) 

        if tab.name.lower() in ['table 7', 'table 19', 'table 24']:
            dimensions = [
                        HDimConst('Period', period),
                        HDimConst('ONS Geography Code', region),
                        HDim(sex, 'Sex', CLOSEST, LEFT),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDimConst('Standard Occupation Classification', soc), 
                        HDim(cod, 'Cause of Death', CLOSEST, LEFT), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                        HDim(rate, 'Rate', DIRECTLY, RIGHT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
        elif tab.name.lower() in ['table 8', 'table 9', 'table 20']:
            dimensions = [
                        HDimConst('Period', period),
                        HDimConst('ONS Geography Code', region),
                        HDim(sex, 'Sex', CLOSEST, LEFT),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDim(soc, 'Standard Occupation Classification', DIRECTLY, LEFT), 
                        HDim(cod, 'Cause of Death', CLOSEST, LEFT), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                        HDimConst('Rate', rate),
                        HDimConst('Lower CI', lower),
                        HDimConst('Upper CI', upper),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
        else:
            dimensions = [
                        HDimConst('Period', period),
                        HDimConst('ONS Geography Code', region),
                        HDim(sex, 'Sex', CLOSEST, LEFT),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDim(soc, 'Standard Occupation Classification', DIRECTLY, LEFT), 
                        HDim(cod, 'Cause of Death', CLOSEST, LEFT), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                        HDim(rate, 'Rate', DIRECTLY, RIGHT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
            
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store("deathsByOccupation", tidy_sheet.topandas())

    elif tab.name.lower() in ['table 13', 'table 14']:

        datasetTitle = 'Coronavirus (COVID-19) related deaths by occupation'

        columns = ['Period','ONS Geography Code','Sex','Age' ,'Occupation', 'Standard Occupation Classification','Cause of Death','Rate','Lower CI','Upper CI','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)
        
        if tab.name.lower() in ['table 14']:
            cell = tab.filter(contains_string('Occupation'))
        else:
            cell = tab.filter(contains_string('Sex'))

        remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(LEFT).expand(DOWN)

        pivot = cellLoc(cell)

        cod = 'Deaths involving COVID-19'
        trace.Cause_of_Death('Hardcoded as: ', var = cod)

        period = right(cellCont(str(tab.excel_ref('B1'))), 29).strip()
        trace.Period('Period range for Tab: {}', var = period)

        if tab.name.lower() in ['table 14']:
            region = cell.shift(1, 1).expand(RIGHT).is_not_blank() - remove
        else:
            region = cell.shift(3, 0).expand(RIGHT).is_not_blank() - remove
        trace.ONS_Geography_Code('Region codes given in range: {}', var = excelRange(region))

        regionOverride = {'Elsewhere' : 'England and Wales excluding London'}

        if tab.name.lower() in ['table 14']:
            soc = 'N/A'
            trace.Standard_Occupation_Classification('Standard Occupation Classification not Applicable for tab')
        else:
            soc = cell.shift(RIGHT).fill(DOWN).is_not_blank() - remove
            trace.Standard_Occupation_Classification('Standard Occupation Classification given in range: ', var = excelRange(soc))

        if tab.name.lower() in ['table 14']:
            occupation = cell.fill(DOWN).is_not_blank() - remove
        else:
            occupation = soc.shift(RIGHT)
        trace.Occupation('Occupation given in cell range: {}', var = excelRange(occupation))
   
        if tab.name.lower() in ['table 14']:
            sex = cell.shift(1, 0).expand(RIGHT).is_not_blank() - remove
        else:
            sex = cell.fill(DOWN).is_not_blank() - remove
        trace.Sex('Gender given in range: ', var = excelRange(sex))

        age = '20 - 64'
        trace.Age('Hardcoded as: {}', var = age)
        
        rate = tab.filter('Rate').fill(DOWN).is_not_blank() - remove
        trace.Rate('Rates taken from range: {}', var = excelRange(rate))

        lower = tab.filter('LCI').fill(DOWN).is_not_blank() - remove
        trace.Lower_CI('Lower CI taken from range: {}', var = excelRange(lower))

        upper = tab.filter('UCI').fill(DOWN).is_not_blank() - remove
        trace.Upper_CI('Upper CI taken from range: {}', var = excelRange(upper))
        
        observations = tab.filter('Deaths').fill(DOWN).is_not_blank() - remove

        measureType = 'Count'
        trace.Measure_Type('Hardcoded as:', var = measureType)

        unit = 'Person'
        trace.Unit('Hardcoded as:', var = unit)

        title = cellCont(str(tab.excel_ref('B1'))).split(',')[0]
        
        columnInfo = {}

        for i in columns:
            underI = i.replace(' ', '_')
            columnInfo[i] = getattr(getattr(trace, underI), 'var')

        dicti = {'name' : tab.name, 
                 'title' : title, 
                 'columns' : columnInfo}
        
        infoData['transform']['transformStage'][tab.name] = dicti

        with open('infoTransform.json', 'w') as info:
            info.write(json.dumps(infoData, indent=4)) 

        if tab.name.lower() in ['table 14']:
            dimensions = [
                        HDimConst('Period', period),
                        HDim(region, 'ONS Geography Code', CLOSEST, LEFT, cellvalueoverride = regionOverride),
                        HDim(sex, 'Sex', CLOSEST, LEFT),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDimConst('Standard Occupation Classification', soc), 
                        HDimConst('Cause of Death', cod), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                        HDim(rate, 'Rate', DIRECTLY, RIGHT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
        else:
            dimensions = [
                        HDimConst('Period', period),
                        HDim(region, 'ONS Geography Code', CLOSEST, LEFT, cellvalueoverride = regionOverride),
                        HDim(sex, 'Sex', CLOSEST, ABOVE),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDim(soc, 'Standard Occupation Classification', DIRECTLY, LEFT), 
                        HDimConst('Cause of Death', cod), #'cause of death' doesnt seem to be the best column header for this but its what they used on table 1
                        HDim(rate, 'Rate', DIRECTLY, RIGHT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store("deathsByOccupation", tidy_sheet.topandas())

    elif tab.name.lower() in ['table 10', 'table 11', 'table 12']:

        smallDatasetTitle = 'Occupation breakdown by Ethnicity'

        columns = ['Period','ONS Geography Code','Age','Sex','Ethnicity','Occupation', 'Standard Occupation Classification','Lower CI','Upper CI','Measure Type','Unit']
        trace.start(smallDatasetTitle, tab, columns, link)
        
        cell = tab.filter('White')

        remove = tab.filter(contains_string('Source:')).expand(RIGHT).expand(LEFT).expand(DOWN)

        remove2 = tab.filter('Sample size').shift(LEFT).expand(DOWN).expand(RIGHT)

        pivot = cellLoc(cell)

        period = '2019'
        trace.Period('Period for Tab: {}', var = period)

        region = 'england and wales'
        trace.ONS_Geography_Code('Region for tab: {}', var = region)
        
        occupation = cell.shift(-1, 0).fill(DOWN).is_not_blank() - remove
        trace.Occupation('Occupation given in cell range: {}', var = excelRange(occupation))
        
        if tab.name.lower() in ['table 12']:
            soc = 'N/A'
            trace.Standard_Occupation_Classification('Not applicable for tab')
        else:
            soc = occupation.shift(LEFT)
            trace.Standard_Occupation_Classification('Standard Occupation Classification given in range: ', var = excelRange(soc))

        ethnicity = cell.expand(RIGHT).is_not_blank() - remove2
        trace.Ethnicity('Ethnicity given in cell range: {}', var = excelRange(ethnicity))
   
        if tab.name.lower() in ['table 10']:
            sex = 'Men'
            trace.Sex('Gender for tab: ', var = sex)
        elif tab.name.lower() in ['table 11']:
            sex = 'Women'
            trace.Sex('Gender for tab: ', var = sex)
        else:
            sex = cell.shift(-2, 0).fill(DOWN).is_not_blank() - remove
            trace.Sex('Gender given in range: ', var = excelRange(sex))

        age = '20 - 64'
        trace.Age('Hardcoded as: {}', var = age)
        
        lower = tab.filter('Lower CI').fill(DOWN).is_not_blank() - remove
        trace.Lower_CI('Lower CI taken from range: {}', var = excelRange(lower))

        upper = tab.filter('Upper CI').fill(DOWN).is_not_blank() - remove
        trace.Upper_CI('Upper CI taken from range: {}', var = excelRange(upper))
        
        observations = tab.filter('Proportion (%)').fill(DOWN).is_not_blank() - remove

        measureType = 'Percentage'
        trace.Measure_Type('Hardcoded as:', var = measureType)

        unit = 'Percent'
        trace.Unit('Hardcoded as:', var = unit)

        title = cellCont(str(tab.excel_ref('B1'))).split(',')[0]
        
        columnInfo = {}

        for i in columns:
            underI = i.replace(' ', '_')
            columnInfo[i] = getattr(getattr(trace, underI), 'var')

        dicti = {'name' : tab.name, 
                 'title' : title, 
                 'columns' : columnInfo}
        
        infoData['transform']['transformStage'][tab.name] = dicti

        with open('infoTransform.json', 'w') as info:
            info.write(json.dumps(infoData, indent=4)) 

        if tab.name.lower() in ['table 12']:
            dimensions = [
                        HDimConst('Period', period),
                        HDimConst('ONS Geography Code', region),
                        HDim(sex, 'Sex', CLOSEST, ABOVE),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDimConst('Standard Occupation Classification', soc), 
                        HDim(ethnicity, 'Ethnicity', CLOSEST, LEFT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
        else:
            dimensions = [
                        HDimConst('Period', period),
                        HDimConst('ONS Geography Code', region),
                        HDimConst('Sex', sex),
                        HDimConst('Age', age),
                        HDim(occupation, 'Occupation', DIRECTLY, LEFT),
                        HDim(soc, 'Standard Occupation Classification', DIRECTLY, LEFT), 
                        HDim(ethnicity, 'Ethnicity', CLOSEST, LEFT),
                        HDim(lower, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper, 'Upper CI', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', measureType), 
                        HDimConst('Unit', unit) 
                ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store("occupationByEthnicity", tidy_sheet.topandas())

    else:
        continue


# In[58]:


pd.set_option('display.float_format', lambda x: '%.0f' % x)

df = trace.combine_and_trace(datasetTitle, "deathsByOccupation").fillna('')

df = df.reset_index(drop=True)

df['Standard Occupation Classification'] = df.apply(lambda x: int(float(x['Standard Occupation Classification'])) if x['Standard Occupation Classification'] not in ['all', 'N/A'] else x['Standard Occupation Classification'], axis = 1)

df = df.replace({'Sex' : {
    'Men aged 65+' : 'Men',
    'Women aged 65+' : 'Women'},
                 'Cause of Death' : {
    'All Causes of death' : 'All Causes of Death', 
    'All causes of death' : 'All Causes of Death',
    'Involving COVID-19' : 'Deaths involving COVID-19'},
                 'Period' : {
    '9th March and 25th May 2020.' : '9th March to 25th May 2020'}})

df = df[['Period','ONS Geography Code','Sex','Age', 'Occupation', 'Standard Occupation Classification','Cause of Death','Rate','Lower CI','Upper CI','Measure Type','Unit','OBS']]

df


# In[59]:


ethDf = trace.combine_and_trace(smallDatasetTitle, "occupationByEthnicity").fillna('')

ethDf = ethDf.reset_index(drop=True)

ethDf['Standard Occupation Classification'] = ethDf.apply(lambda x: int(float(x['Standard Occupation Classification'])) if x['Standard Occupation Classification'] not in ['all', 'N/A', ''] else x['Standard Occupation Classification'], axis = 1)

ethDf = ethDf.replace({'Standard Occupation Classification' : {
    '' : 'N/A'},
                 'Occupation': {
    'All men aged 20 to 64 years with an occupation ' : 'all',
    'All women aged 20 to 64 years with an occupation' : 'all'}})

ethDf = ethDf[['Period','ONS Geography Code','Sex','Age', 'Occupation', 'Standard Occupation Classification','Ethnicity','Lower CI','Upper CI','Measure Type','Unit','OBS']]

ethDf


# In[60]:


notes = """
Age-standardised rates per 100,000 population, standardised to the 2013 European Standard Population. Age-standardised rates are used to allow comparison between populations which may contain different proportions of people of different ages.
The lower and upper confidence limits have been provided. These form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the estimated figure. Calculations based on small numbers of events are often subject to random fluctuations. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
Deaths were defined using the International Classification of Diseases, 10th Revision (ICD-10). Deaths involving COVID-19 include those with an underlying cause, or any mention, of ICD-10 codes U07.1 (COVID-19, virus identified) or U07.2 (COVID-19, virus not identified). All causes of death is the total number of deaths registered during the same time period, including those that involved COVID-19. Average 5 year mortality refers to all causes of deaths, registered in the same time period 2015 to 2019. 
Figures are for the most recent death registrations available at the time of analysis, deaths involving COVID-19 registered between 9th March and 25th May. 
Analysis is not provided when numbers of deaths are below 10 and have been marked ':'.
"""


# In[61]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[62]:


from IPython.core.display import HTML
for col in ethDf:
    if col not in ['Value']:
        ethDf[col] = ethDf[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(ethDf[col].cat.categories)


# In[63]:


for column in df:
    if column in ('Occupation', 'Sex', 'Cause of Death'):
        df[column] = df[column].map(lambda x: pathify(x))


# In[64]:


for column in ethDf:
    if column in ('occupation', 'Sex', 'Ethnicity'):
        ethDf[column] = ethDf[column].map(lambda x: pathify(x))


# In[65]:


out = Path('out')
out.mkdir(exist_ok=True)

GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

title = pathify(datasetTitle)

smallTitle = pathify(smallDatasetTitle)

scraper.dataset.comment = notes

import os

df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

df.drop_duplicates().to_csv(out / f'{smallTitle}.csv', index = False)

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()

df

