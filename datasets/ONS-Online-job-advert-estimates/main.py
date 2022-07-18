#!/usr/bin/env python
# coding: utf-8

# In[97]:


# # ONS Online job advert estimates 

# +
from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import numpy as np
from urllib.parse import urljoin
import os

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


# In[98]:


info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scrape = Scraper(landingPage)  
distribution = scrape.distributions[0]
distribution


# In[99]:


datasetTitle = 'Online job advert estimates'
tabs = { tab: tab for tab in distribution.as_databaker() }
for i in tabs:
    print(i.name)


# In[100]:


tidied_tabs = []

for tab in tabs:

    if 'adverts by category' in tab.name.lower():

        print(tab.name)

        remove = tab.filter('Notes:').expand(RIGHT).expand(DOWN)

        date = tab.filter('Date').fill(RIGHT).is_not_blank()

        category = tab.filter('Date').fill(DOWN).is_not_blank() - remove - tab.filter('Imputed values')

        imputed_values = tab.filter('Imputed values').fill(RIGHT).filter('All').fill(UP).is_not_blank() | tab.filter('Imputed values').fill(RIGHT).filter('Education only').fill(UP) - (tab.filter('Date').fill(DOWN)-tab.filter('Education')).expand(RIGHT) - date 

        if 'DD' in tab.name:
            deduplicated = 'yes'

            unit = 'Job Adverts'

            measure_type = 'Indicator Deduplicated'

        elif 'YoY' in tab.name:
            deduplicated = 'yes'

            unit = 'Job Adverts'

            measure_type = 'Indicator Equivalent to Prior Year'

        else:
            deduplicated = 'no'

            unit = 'Job Adverts'

            measure_type = 'Indicator'

        region = "United Kingdom"

        observations = category.fill(RIGHT).is_not_blank() - imputed_values

        dimensions = [
            HDim(date, 'Period', DIRECTLY, ABOVE),
            HDim(category, 'Category', DIRECTLY, LEFT),
            HDimConst('Region', region),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Marker', '')
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        
        nonimputed = tidy_sheet.topandas()

        observations = (tab.filter('Imputed values').fill(RIGHT).filter('All').fill(UP).is_not_blank() | tab.filter('Imputed values').fill(RIGHT).filter('Education only').fill(UP) - (tab.filter('Date').fill(DOWN)-tab.filter('Education')).expand(RIGHT)).is_not_blank() - date

        dimensions = [
            HDim(date, 'Period', DIRECTLY, ABOVE),
            HDim(category, 'Category', DIRECTLY, LEFT),
            HDimConst('Region', region),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Marker', 'imputed')
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
 
        imputed = tidy_sheet.topandas()

        tidied_tabs.append(pd.concat([nonimputed, imputed]))

    elif 'adverts by region' in tab.name.lower():

        print(tab.name)

        remove = tab.filter('Notes:').expand(RIGHT).expand(DOWN)

        date = tab.filter('Date').fill(RIGHT).is_not_blank()

        region = (tab.filter('Date').fill(DOWN).is_not_blank() - remove - tab.filter('Imputed values')) | tab.filter('Unknown') | tab.filter('Unmatched')

        imputed_values = tab.filter('Imputed values').fill(RIGHT).filter('All').fill(UP).is_not_blank() - date

        if 'DD' in tab.name:
            deduplicated = 'yes'

            unit = 'Job Adverts'

            measure_type = 'Indicator Deduplicated'

        elif 'YoY' in tab.name:
            deduplicated = 'yes'

            unit = 'Job Adverts '

            measure_type = 'Indicator Equivalent to Prior Year'

        else:
            deduplicated = 'no'

            unit = 'Job Adverts'

            measure_type = 'Indicator'

        observations = region.shift(RIGHT).fill(RIGHT).is_not_blank() - imputed_values

        dimensions = [
            HDim(date, 'Period', DIRECTLY, ABOVE),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDimConst('Category', 'all'),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Marker', '')
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        
        nonimputed = tidy_sheet.topandas()

        observations = tab.filter('Imputed values').fill(RIGHT).filter('All').fill(UP).is_not_blank() - date

        dimensions = [
            HDim(date, 'Period', DIRECTLY, ABOVE),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDimConst('Category', 'all'),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Marker', 'imputed')
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
 
        imputed = tidy_sheet.topandas()

        tidied_tabs.append(pd.concat([nonimputed, imputed]))


# In[101]:


df = pd.concat(tidied_tabs)
df.rename(columns={'OBS' : 'Value'}, inplace=True)

df['Period'] = df['Period'].map(lambda x: f'day/{x}')

df = df.rename(columns={'Category' : 'Industry'})

df['Region'] = df['Region'].str.replace('(' , '').str.replace(')' , '')

df = df.replace({'Region' : {'United Kingdom' : 'K02000001'}})

df['Industry'] = df['Industry'].apply(pathify)
df['Measure Type'] = df['Measure Type'].apply(pathify)
df['Unit'] = df['Unit'].apply(pathify)

df


# In[102]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 


# In[103]:


tidy = df[['Period', 'Industry', 'Region', 'Measure Type', 'Unit', 'Value', 'Marker']]

for column in tidy:
    if column in ('Industry', 'Region'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()

tidy


# In[104]:


notes = """
Total job adverts by Adzuna Category, Index 2019 average = 100
1. The observations were collected on a roughly weekly basis; however they were not all collected at the same point in each week, leading to slightly irregular gaps between each observation.
2. Furthermore some weeks have no observation. The missing  values have been imputed using linear interpolation, and have been highlighted.
3. The education industry's total online job adverts estimate for the 21st of March 2019 was an anomaly, and the value was imputed through linear interpolation.
4. The 2019 average values used to index the series were calculated after imputing the missing weeks.
5. The Adzuna categories used do not correspond to SIC categories.
6. There is an increased level of duplication in the Management/exec/consulting category for the 19th June 2020, resulting in a potentially inflated value for total job adverts in this category.
7. Historically the health and social care category has shown a strong correlation with the ONS Vacancy Survey, but from April 2020 it has increasingly diverged from the vacancies data.

"""


# In[105]:


tidy.to_csv('observations.csv', index=False)

catalog_metadata = scrape.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file('catalog-metadata.json')

