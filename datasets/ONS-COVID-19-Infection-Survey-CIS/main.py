#!/usr/bin/env python
# coding: utf-8

# In[207]:


# # ONS Coronavirus  COVID-19  Infection Survey 

from gssutils import * 
import json
import string
import warnings

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

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


# In[208]:


#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper


# In[209]:


distribution = scraper.distributions[0]
display(distribution)


# In[210]:


trace = TransformTrace()

tabs = { tab: tab for tab in distribution.as_databaker() }

tidied_sheets = []

infectionSurvey = 'ONS Coronavirus COVID-19 Infection Survey'
link = distribution.downloadURL

for tab in tabs:

    if tab.name.isdigit():

            columns=["Period", "ONS Geography Code", "Survey Criteria", "Age", "Sex", "Working Location", "CI Lower", "CI Upper", "Measure Type", "Unit"]
            trace.start(infectionSurvey, tab, columns, link)

            cell = tab.filter(contains_string('Contents')).shift(0, 5)

            remove = tab.filter(contains_string('Notes:')).expand(RIGHT).expand(DOWN)
            pivot = cellLoc(cell)

            if '4' in tab.name:
                period = cell.fill(DOWN).is_not_blank() - remove
            else:
                period = cell.shift(0, -2)
            trace.Period('Period Range for Tab given at cell value: {}', var = cellLoc(period))

            region = 'E92000001'

            if tab.name in ['4', '5', '6','10']:
                infections = cell.shift(1, -1).expand(RIGHT).is_not_blank() - (tab.filter(contains_string('Confidence Interval'))) - remove
            else:
                infections = cell.fill(DOWN).is_not_blank() - remove
            trace.Survey_Criteria('Selected as non-blank values in range: {}', var = excelRange(infections))

            if '5' in tab.name:
                age = cell.expand(DOWN).is_not_blank() - remove
            else:
                age = "All"

            if '6' in tab.name:
                sex = cell.expand(DOWN).is_not_blank() - remove
            else:
                sex = 'All'

            if '10' in tab.name:
                workLoc = cell.expand(DOWN).is_not_blank() - remove
            else:
                workLoc = 'All' #Includes Not Applicable

            confidenceLower = tab.filter(contains_string('Lower')).expand(DOWN) - remove
            trace.CI_Lower('Selected as all values in range: {}', var = excelRange(confidenceLower))

            confidenceUpper = tab.filter(contains_string('Upper')).expand(DOWN) - remove
            trace.CI_Upper('Selected as all values in range: {}', var = excelRange(confidenceUpper))

            trace.Measure_Type('Initially Hard Coded to Count')

            trace.Unit('Initially Hard Coded to Person')

            if '4' in tab.name:
                observations = period.fill(RIGHT).is_not_blank() - remove - confidenceLower - confidenceUpper
            elif '5' in tab.name:
                observations = age.fill(RIGHT).is_not_blank() - confidenceLower - confidenceUpper
            elif '6' in tab.name:
                observations = sex.fill(RIGHT).is_not_blank() - confidenceLower - confidenceUpper
            elif '10' in tab.name:
                observations = workLoc.fill(RIGHT).is_not_blank() - confidenceLower - confidenceUpper
            else:
                observations = infections.fill(RIGHT).is_not_blank() - remove - confidenceLower - confidenceUpper

            if '4' in tab.name:
                dimensions = [
                        HDim(period, 'Period', DIRECTLY, LEFT),
                        HDimConst('ONS Geography Code', region),
                        HDim(infections, 'Survey Criteria', DIRECTLY, ABOVE),
                        HDimConst("Age", age),
                        HDimConst('Sex', sex),
                        HDimConst('Working Location', workLoc),
                        HDim(confidenceLower, 'CI Lower', DIRECTLY, RIGHT),
                        HDim(confidenceUpper, 'CI Upper', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', 'Percentage'), #Easier to change Count values to Count post transform
                        HDimConst('Unit', 'Percent') #Easier to change Count values to Person post transform
                ]
            elif '5' in tab.name:
                dimensions = [
                        HDim(period, 'Period', CLOSEST, ABOVE),
                        HDimConst('ONS Geography Code', region),
                        HDim(infections, 'Survey Criteria', DIRECTLY, ABOVE),
                        HDim(age, 'Age', DIRECTLY, LEFT),
                        HDimConst('Sex', sex),
                        HDimConst('Working Location', workLoc),
                        HDim(confidenceLower, 'CI Lower', DIRECTLY, RIGHT),
                        HDim(confidenceUpper, 'CI Upper', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', 'Percentage'), #Easier to change Count values to Count post transform
                        HDimConst('Unit', 'Percent') #Easier to change Count values to Person post transform
                ]
            elif '6' in tab.name:
                dimensions = [
                        HDim(period, 'Period', CLOSEST, ABOVE),
                        HDimConst('ONS Geography Code', region),
                        HDim(infections, 'Survey Criteria', DIRECTLY, ABOVE),
                        HDimConst('Age', age),
                        HDim(sex, 'Sex', DIRECTLY, LEFT),
                        HDimConst('Working Location', workLoc),
                        HDim(confidenceLower, 'CI Lower', DIRECTLY, RIGHT),
                        HDim(confidenceUpper, 'CI Upper', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', 'Percentage'), #Easier to change Count values to Count post transform
                        HDimConst('Unit', 'Percent') #Easier to change Count values to Person post transform
                ]
            elif '10' in tab.name:
                dimensions = [
                        HDim(period, 'Period', CLOSEST, ABOVE),
                        HDimConst('ONS Geography Code', region),
                        HDim(infections, 'Survey Criteria', DIRECTLY, ABOVE),
                        HDimConst('Age', age),
                        HDimConst('Sex', sex),
                        HDim(workLoc, 'Working Location', DIRECTLY, LEFT),
                        HDim(confidenceLower, 'CI Lower', DIRECTLY, RIGHT),
                        HDim(confidenceUpper, 'CI Upper', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', 'Percentage'), #Easier to change Count values to Count post transform
                        HDimConst('Unit', 'Percent') #Easier to change Count values to Person post transform
                ]
            else:
                dimensions = [
                        HDim(period, 'Period', CLOSEST, ABOVE),
                        HDimConst('ONS Geography Code', region),
                        HDim(infections, 'Survey Criteria', DIRECTLY, LEFT),
                        HDimConst("Age", age),
                        HDimConst('Sex', sex),
                        HDimConst('Working Location', workLoc),
                        HDim(confidenceLower, 'CI Lower', DIRECTLY, RIGHT),
                        HDim(confidenceUpper, 'CI Upper', DIRECTLY, RIGHT),
                        HDimConst('Measure Type', 'Percentage'), #Easier to change Count values to Count post transform
                        HDimConst('Unit', 'Percent') #Easier to change Count values to Person post transform
                ]
 
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)

            trace.store("infectionSurvey", tidy_sheet.topandas())

    else:
        continue


# In[211]:


import pandas as pd

df = trace.combine_and_trace(infectionSurvey, "infectionSurvey").fillna('')

df = df.reset_index(drop=True)

df['Period'] = df.apply(lambda x: x['Period'].replace('between ', '') if 'between' in x['Period'] else x['Period'], axis = 1)

df['Measure Type'] = df.apply(lambda x: 'Count' if decimal(x['OBS']) == True else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'Average Count' if 'average' in x['Period'] and 'Count' in x['Measure Type'] else x['Measure Type'], axis = 1)

trace.Measure_Type("Updated to 'Count' for Count values")
df['Measure Type'] = df.apply(lambda x: 'Average Count' if 'average' in x['Survey Criteria'].lower() and '%' not in x['Survey Criteria'] else x['Measure Type'], axis = 1)
trace.Measure_Type("Updated to 'Average Count' for Average Count values")
df['Measure Type'] = df.apply(lambda x: 'Average Percentage' if 'average' in x['Survey Criteria'].lower() and '%' in x['Survey Criteria'] else x['Measure Type'], axis = 1)
trace.Measure_Type("Updated to 'Average Percentage' for Average % values")

df['Unit'] = df.apply(lambda x: 'Person' if 'Count' in x['Measure Type'] else x['Unit'], axis = 1)
trace.Unit("Updated to 'Person' for Count values")

df['OBS'] = df.apply(lambda x: x['OBS']*100 if 'Percent' in x['Unit'] else x['OBS'], axis = 1)
df['CI Lower'] = df.apply(lambda x: float(x['CI Lower'])*100 if 'Percent' in x['Unit'] else x['CI Lower'], axis = 1)
df['CI Upper'] = df.apply(lambda x: float(x['CI Upper'])*100 if 'Percent' in x['Unit'] else x['CI Upper'], axis = 1)

indexNames = df[ df['DATAMARKER'] == '-' ].index
df.drop(indexNames, inplace = True)


trace.add_column("Value")
trace.multi(['Value', 'CI_Lower', 'CI_Upper'], "Due to Excel formatting percent values need to be adjusted by multiplying by 100.")

df['Period'] = df.apply(lambda x: x['Period'].split(":", 1)[0] if ':' in x['Period'] else x['Period'], axis = 1)

df = df.replace({'Survey Criteria' : {
    'Estimated average % of the population that had COVID-19 (weighted)' : 'Estimated Total COVID-19 Cases (weighted)',
    'Estimated average number of people in England who had COVID-19 (weighted)' : 'Estimated Total COVID-19 Cases (weighted)',
    'Number of individuals included in this analysis (unweighted)' : 'Total Individuals in Analysis (unweighted)',
    'Estimated average number of people in England who were newly infected with COVID-19 per week ' : 'Estimated Infections Per Week (weighted)',
    'New infections per 100 people followed for 1 week, known as the incidence rate ' : 'Incidence Rate (weighted)',
    'Individuals included in antibody analysis' : 'Individuals Included in Antibody Analysis (unweighted)',
    'Percentage of individuals testing positive for antibodies' : 'Estimated Individuals Testing Positive for Antibodies (unweighted)',
    '% testing positive for COVID-19' : 'Estimated Tested Positive for COVID-19 (weighted)', 
    'Number testing positive for COVID-19' : 'Estimated Tested Positive for COVID-19 (weighted)',
    'Individuals not working in patient-facing healthcare or resident-facing social care roles' : 'Estimated Individuals not Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)',
    'Individuals working in patient-facing healthcare or resident-facing social care roles' : 'Estimated Individuals Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)',
    'Individuals not reporting any symptoms on the day of the test' : 'Estimated Individuals Testing Positive for COVID-19 Not Reporting Symptons on Day of Test (unweighted)',
    'Individuals reporting any symptoms on the day of the test' : 'Estimated Individuals Testing Positive for COVID-19 Reporting Symptons on Day of Test (unweighted)',
    'Individuals reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test' : 'Estimated Individuals Testing Positive for COVID-19 reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)',
    'Individuals reporting no cough or fever or loss of taste/smell on the day of the test' : 'Estimated Individuals Testing Positive for COVID-19 reporting no cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)'}, 
                 'CI Lower' : {
    '' : 'N/A'},
                 'CI Upper' : {
    '' : 'N/A'},
                 'Age' : {
    '70 and above' : '70+'
                 }})

trace.Survey_Criteria("Change 'Estimated average % of the population that had COVID-19 (weighted)' to 'Estimated Total COVID-19 Cases (weighted)'")
trace.Survey_Criteria("Change 'Estimated average number of people in England who had COVID-19 (weighted)' to 'Estimated Total COVID-19 Cases (weighted)'")
trace.Survey_Criteria("Change 'Number of individuals included in this analysis (unweighted)' to 'Total Individuals in Analysis (unweighted)'")
trace.Survey_Criteria("Change 'Estimated average number of people in England who were newly infected with COVID-19 per week ' to 'Estimated Infections Per Week (weighted)'")
trace.Survey_Criteria("Change 'New infections per 100 people followed for 1 week, known as the incidence rate ' to 'Incidence Rate (weighted)'")
trace.Survey_Criteria("Change 'Individuals included in antibody analysis' to 'Individuals Included in Antibody Analysis (unweighted)'")
trace.Survey_Criteria("Change 'Percentage of individuals testing positive for antibodies' to 'Estimated Individuals Testing Positive for Antibodies (unweighted)'")
trace.Survey_Criteria("Change '% testing positive for COVID-19' to 'Estimated Tested Positive for COVID-19 (weighted)'")
trace.Survey_Criteria("Change 'Number testing positive for COVID-19' to 'Estimated Tested Positive for COVID-19 (weighted)'")
trace.Survey_Criteria("Change 'Individuals not working in patient-facing healthcare or resident-facing social care roles' to 'Estimated Individuals not Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)'")
trace.Survey_Criteria("Change 'Individuals working in patient-facing healthcare or resident-facing social care roles' to 'Estimated Individuals Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)'")
trace.Survey_Criteria("Change 'Individuals not reporting any symptoms on the day of the test' to 'Estimated Individuals Testing Positive for COVID-19 Not Reporting Symptons on Day of Test (unweighted)'")
trace.Survey_Criteria("Change 'Individuals reporting any symptoms on the day of the test' to 'Estimated Individuals Testing Positive for COVID-19 Reporting Symptons on Day of Test (unweighted)'")
trace.Survey_Criteria("Change 'Individuals reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test' to 'Estimated Individuals Testing Positive for COVID-19 reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)'")
trace.Survey_Criteria("Change 'Individuals reporting no cough or fever or loss of taste/smell on the day of the test' to 'Estimated Individuals Testing Positive for COVID-19 reporting no cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)")

trace.CI_Lower("Change blank values to N/A")
trace.CI_Upper("Change blank values to N/A")
trace.Age("Change value '70 and above' to 70+")

df['OBS'] = df.apply(lambda x: str(int(x['OBS'])) if 'Person' in x['Unit'] else x['OBS'], axis = 1)
df['CI Lower'] = df.apply(lambda x: str(int(float(x['CI Lower']))) if ('Person' in x['Unit'] and 'N/A' not in x['CI Lower']) else x['CI Lower'], axis = 1)
df['CI Upper'] = df.apply(lambda x: str(int(float(x['CI Upper']))) if ('Person' in x['Unit'] and 'N/A' not in x['CI Upper']) else x['CI Upper'], axis = 1)

df = df.drop(['DATAMARKER'], axis=1)

df = df.rename(columns={'OBS':'Value'})

df = df[['Period', 'ONS Geography Code', 'Survey Criteria', 'Age', 'Sex', 'Working Location', 'CI Lower', 'CI Upper', 'Measure Type', 'Unit', 'Value']]

df


# In[212]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[213]:


notes = """
These statistics refer to infections reported in the community, by which we mean private households. These figures exclude infections reported in hospitals, care homes or other institutional settings.
The estimate for those testing positive for antibodies presented in this publication has not been updated and is the same as estimates presented in our previous publication. Once we have received additional blood sample results we will provide updated antibodies analysis.
We asked individuals to self report whether they worked in patient-facing healthcare or resident-facing social care, where that information was missing or uncertain, other information provided about their occupation has been used.
"""

for column in df:
    if column in ('Survey Criteria', 'Age', 'Sex', 'Working Location'):
        df[column] = df[column].map(lambda x: pathify(x))


# In[214]:


out = Path('out')
out.mkdir(exist_ok=True)

infectionSurveyTitle = pathify(infectionSurvey)

scraper.dataset.comment = notes

import os

df.drop_duplicates().to_csv(out / f'{infectionSurveyTitle}.csv', index = False)

with open(out / f'{infectionSurveyTitle}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()

df

