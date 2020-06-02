#!/usr/bin/env python
# coding: utf-8

# In[65]:


# # PHE Coronavirus  COVID-19  in the UK

from gssutils import *
import pandas as pd
import json

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[66]:


"""
Note that the scraper for this page doesn't currently work/exist.
Therefore to run this pipeline you will need to download the TWO csv files from https://coronavirus.data.gov.uk/
to the folder which contains main.py/main.ipynb
"""


# In[67]:


covidCases = pd.read_csv('coronavirus-cases_latest.csv')

covidCases = covidCases.drop(['Area name'], axis=1)

covidCases = pd.melt(covidCases, id_vars = ['Area code','Area type', 'Specimen date'], var_name = 'Reported Case Type', value_name = 'Value')

covidCases['Measure Type'] = 'Cases'
covidCases['Measure Type'] = covidCases.apply(lambda x: 'Rate' if 'rate' in x['Reported Case Type'] else x['Measure Type'], axis = 1)

covidCases['Unit'] = 'Count'

covidCases = covidCases.rename(columns={'Area code':'ONS Geography Code',
                                        'Specimen date':'Period',
                                        'Area type' : 'Area Type'})


covidCases = covidCases[['Period', 'ONS Geography Code', 'Area Type', 'Reported Case Type', 'Measure Type', 'Unit', 'Value']]


# In[68]:


covidDeaths = pd.read_csv('coronavirus-deaths_latest.csv')

covidDeaths = covidDeaths.drop(['Area name'], axis=1)

covidDeaths = pd.melt(covidDeaths, id_vars = ['Area code','Area type', 'Reporting date'], var_name = 'Reported Case Type', value_name = 'Value')

covidDeaths['Measure Type'] = 'Deaths'

covidDeaths['Unit'] = 'Count'

covidDeaths = covidDeaths.rename(columns={'Area code':'ONS Geography Code',
                                          'Reporting date':'Period',
                                          'Area type' : 'Area Type'})


covidDeaths = covidDeaths[['Period', 'ONS Geography Code', 'Area Type', 'Reported Case Type', 'Measure Type', 'Unit', 'Value']]


# In[69]:





# In[70]:


from IPython.core.display import HTML
for col in covidCases:
    if col not in ['Value']:
        covidCases[col] = covidCases[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(covidCases[col].cat.categories)

from IPython.core.display import HTML
for col in covidDeaths:
    if col not in ['Value']:
        covidDeaths[col] = covidDeaths[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(covidDeaths[col].cat.categories)


# In[71]:


for column in covidCases:
    if column in ('Area Type', 'Reported Case Type'):
        covidCases[column] = covidCases[column].map(lambda x: pathify(x))

covidCases.head(25)

for column in covidDeaths:
    if column in ('Area Type', 'Reported Case Type'):
        covidDeaths[column] = covidDeaths[column].map(lambda x: pathify(x))

covidDeaths.head(25)


# In[72]:


out = Path('out')
out.mkdir(exist_ok=True)

titleCovidCases = pathify('PHE Coronavirus COVID-19 Cases in the UK')

titleCovidDeaths = pathify('PHE Coronavirus COVID-19 Deaths in the UK')

import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))


covidCases.drop_duplicates().to_csv(out / f'{titleCovidCases}.csv', index = False)

covidDeaths.drop_duplicates().to_csv(out / f'{titleCovidDeaths}.csv', index = False)
"""
scraper.dataset.family = 'homelessness'
scraper.dataset.theme = THEME['housing-planning-local-services']
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-homelessness/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')"""

