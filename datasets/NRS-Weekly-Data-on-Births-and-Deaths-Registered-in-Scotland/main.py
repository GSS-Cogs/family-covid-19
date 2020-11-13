#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
# # NRS Weekly Data on Births and Deaths Registered in Scotland

from gssutils import *
import json
import re

def cellCont(cell):
    return re.findall(r"'([^']*)'", str(cell))[0]

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[2]:


scrape = Scraper(landingPage)
scrape


# In[3]:


scrape.distributions = [x for x in scrape.distributions if x.mediaType == Excel]

for i in scrape.distributions:
    display(i)


# In[4]:


birthsDist = scrape.distributions[0]
display(birthsDist)

deathsDist = scrape.distributions[1]
display(deathsDist)


# In[5]:


tabs = {}

birthTabs = { tab.name: tab for tab in birthsDist.as_databaker()}
list(birthTabs)
tabs.update(birthTabs)

deathTabs = { tab.name: tab for tab in deathsDist.as_databaker()}
list(deathTabs)
tabs.update(deathTabs)

tidied_sheets = {}

for name, tab in tabs.items():

    remove = tab.filter('Notes').expand(DOWN).expand(RIGHT)

    if 'table 1' in cellCont(tab.excel_ref('A1')).lower():
        cell = tab.filter(contains_string('Table 1:'))
    elif 'table 2' in cellCont(tab.excel_ref('A1')).lower():
        cell = tab.filter(contains_string('Table 2:'))

    area = 'Scotland'

    year = cell.shift(1, 3).expand(RIGHT).is_not_blank()

    week = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

    if 'table 1' in cellCont(tab.excel_ref('A1')).lower():
        measure_type = 'Births'
    elif 'table 2' in cellCont(tab.excel_ref('A1')).lower():
        measure_type = 'Deaths'

    unit = 'Count'

    observations = week.fill(RIGHT).is_not_blank() - tab.filter('Week Number').expand(DOWN)

    dimensions = [
        HDimConst('Area', area),
        HDim(year, 'Year', DIRECTLY, ABOVE),
        HDim(week, 'Week', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

    tidy_sheet = ConversionSegment(tab, dimensions, observations)
    savepreviewhtml(tidy_sheet, fname="Preview.html")

    if 'table 1' in cellCont(tab.excel_ref('A1')).lower():
        tableName = 'Table 1'
    elif 'table 2' in cellCont(tab.excel_ref('A1')).lower():
        tableName = 'Table 2'

    tidied_sheets[tableName] = tidy_sheet.topandas()


# In[6]:


dataframes = []

for name in tidied_sheets:

    if 'table 1' in name.lower():

        df = tidied_sheets['Table 1']

        df['Week'] = df.apply(lambda x: x['Week'][1:] if 'W' in x['Week'] else x['Week'], axis = 1)

        dataframes.append(df)

    elif 'table 2' in name.lower():

        df = tidied_sheets['Table 2']

        df['Week'] = df.apply(lambda x: x['Week'][1:] if 'W' in x['Week'] else x['Week'], axis = 1)

        dataframes.append(df)

merged_df = pd.concat(dataframes)
merged_df


# In[7]:


csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
merged_df.drop_duplicates().to_csv(out / csvName, index = False)


# In[8]:


from IPython.core.display import HTML
for col in merged_df:
    if col not in ['Value']:
        merged_df[col] = merged_df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(merged_df[col].cat.categories)

