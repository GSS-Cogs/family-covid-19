#!/usr/bin/env python
# coding: utf-8

# In[152]:


# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI

from gssutils import *
import json
#title = "Weekly deaths, 2020 (NI)"
scrape = Scraper('https://www.nisra.gov.uk/publications/weekly-deaths')
scrape


# In[153]:



scrape.distributions = [x for x in scrape.distributions if x.mediaType == Excel]


# In[154]:


dist = scrape.distributions[0]
display(dist)


# In[155]:


tabs = { tab.name: tab for tab in dist.as_databaker() if tab.name.startswith('Table')}
list(tabs)

tidied_sheets = {}

for name, tab in tabs.items():

    if 'table 1' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 4).fill(DOWN).is_not_blank() - remove

        measurement = cell.shift(2, 3).expand(RIGHT).is_not_blank() | cell.shift(2, 4).expand(RIGHT).is_not_blank()

        measure_type = 'Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(measurement, 'Measurement', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 2' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(0, 4).fill(RIGHT).is_not_blank() | tab.filter('Year to Date')

        gender = cell.shift(0, 5).expand(DOWN).is_not_blank()

        age = gender.shift(RIGHT).expand(DOWN).is_not_blank() - remove

        measure_type = 'Deaths'

        unit = 'Count'

        observations = age.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, ABOVE),
        HDim(gender, 'Gender', CLOSEST, ABOVE),
        HDim(age, 'Age', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 3' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = cell.shift(2, 4).expand(RIGHT).is_not_blank()

        week_ending = cell.shift(1, 4).fill(DOWN).is_not_blank() - remove

        measure_type = 'Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDim(area, 'Area', DIRECTLY, ABOVE),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 4' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(2, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 5' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(0, 4).fill(RIGHT).is_not_blank() | tab.filter('Year to Date')

        gender = cell.shift(0, 5).expand(DOWN).is_not_blank()

        age = gender.shift(RIGHT).expand(DOWN).is_not_blank() - remove

        measure_type = 'Covid Related Deaths'

        unit = 'Count'

        observations = age.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, ABOVE),
        HDim(gender, 'Gender', CLOSEST, ABOVE),
        HDim(age, 'Age', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 6' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = cell.shift(2, 4).expand(RIGHT).is_not_blank()

        week_ending = cell.shift(1, 4).fill(DOWN).is_not_blank() - remove

        measure_type = 'Covid Related Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDim(area, 'Area', DIRECTLY, ABOVE),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 7' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(2, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Covid Related Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 8' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = cell.shift(2, 4).expand(RIGHT).is_not_blank()

        week_ending = cell.shift(1, 4).fill(DOWN).is_not_blank() - remove

        measure_type = 'Covid Related Care Home Deaths'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDim(area, 'Area', DIRECTLY, ABOVE),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 9' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        period = cell.shift(0, 4).expand(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(1, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Covid Related Deaths'

        unit = 'Count'

        observations = period.fill(RIGHT).is_not_blank() - tab.filter('Cumulative Total').expand(DOWN)

        dimensions = [
        HDimConst('Area', area),
        HDim(period, 'Period', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 10' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove

        measure_type = 'Covid Related Death Occurrences'

        unit = 'Count'

        observations = week_ending.shift(RIGHT)

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 11' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(2, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Covid Related Death Occurrences'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 12' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        week_ending = cell.shift(1, 3).fill(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(2, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Covid Related Death Occurrences'

        unit = 'Count'

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDimConst('Area', area),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

    elif 'table 13' == name.lower():

        remove = tab.filter('P Weekly published data are provisional.').expand(DOWN).expand(RIGHT)

        cell = tab.filter('Contents')

        area = 'Northern Ireland'

        period = cell.shift(0, 4).expand(DOWN).is_not_blank() - remove

        place_of_death = cell.shift(1, 3).expand(RIGHT).is_not_blank()

        measure_type = 'Covid Related Death Occurrences'

        unit = 'Count'

        observations = period.fill(RIGHT).is_not_blank() - tab.filter('Cumulative Total').expand(DOWN)

        dimensions = [
        HDimConst('Area', area),
        HDim(period, 'Period', DIRECTLY, LEFT),
        HDim(place_of_death, 'Place of Death', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()


# In[156]:


for name in tidied_sheets:

    if 'table 1' in name.lower():

        df = tidied_sheets['Table 1']

        df['Unit'] = df.apply(lambda x: 'Average Count' if 'Average' in x['Measurement'] else x['Unit'], axis = 1)

    elif 'table 2' in name.lower():

        df = tidied_sheets['Table 2']

        df['Gender'] = df.apply(lambda x: 'All' if 'Total Registered Deaths' in x['Gender'] else x['Gender'], axis = 1)

    elif 'table 3' in name.lower():

        df = tidied_sheets['Table 3']

    elif 'table 4' in name.lower():

        df = tidied_sheets['Table 4']

    elif 'table 5' in name.lower():

        df = tidied_sheets['Table 5']

        df['Gender'] = df.apply(lambda x: 'All' if 'Total Registered Deaths' in x['Gender'] else x['Gender'], axis = 1)

    elif 'table 6' in name.lower():

        df = tidied_sheets['Table 6']

    elif 'table 7' in name.lower():

        df = tidied_sheets['Table 7']

    elif 'table 8' in name.lower():

        df = tidied_sheets['Table 8']

    elif 'table 9' in name.lower():

        df = tidied_sheets['Table 9']

    elif 'table 10' in name.lower():

        df = tidied_sheets['Table 10']

    elif 'table 11' in name.lower():

        df = tidied_sheets['Table 11']

    elif 'table 12' in name.lower():

        df = tidied_sheets['Table 12']

        df['Unit'] = df.apply(lambda x: 'Percent' if '%' in x['Place of Death'] else x['Unit'], axis = 1)

        df['Measure Type'] = df.apply(lambda x: 'Percentage of all Covid Related Deaths' if '%' in x['Place of Death'] else x['Measure Type'], axis = 1)

        df['Place of Death'] = df.apply(lambda x: 'Hospital' if '% of all Covid-19 Hospital Deaths' in x['Place of Death'] else x['Place of Death'], axis = 1)

        df['Place of Death'] = df.apply(lambda x: 'Total' if '% of all Covid-19 Deaths' in x['Place of Death'] else x['Place of Death'], axis = 1)

    elif 'table 13' in name.lower():

        df = tidied_sheets['Table 13']

df


# In[157]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[157]:




