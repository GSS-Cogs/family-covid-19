#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
# # NRS Monthly Data on Births and Deaths Registered in Scotland

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

j = 0

distributions = {}

for i in scrape.distributions:
    j += 1
    display(i)
    distributions['Table ' + str(j)] = i

distributions


# In[4]:


tidied_tables = {}

for tableNumber, dist in distributions.items():

    print(tableNumber)

    tabs = {tab for tab in dist.as_databaker()}

    tidied_sheets = []

    if 'table 1' in tableNumber.lower():

        for tab in tabs:

            tableTitle = tableNumber + ' ' + 'Births in Scotland by month of registration and NHS Board area'

            remove = tab.filter('Footnotes').expand(RIGHT).expand(DOWN)

            cell = tab.filter(contains_string(tableNumber))

            area = tab.name

            year = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

            month = cell.shift(2, 4).expand(RIGHT).is_not_blank() - remove

            observations = year.shift(RIGHT).fill(RIGHT).is_not_blank()

            measure_type = 'Births'

            unit = 'Count'

            dimensions = [
                HDimConst('Area', area),
                HDim(year, 'Year', DIRECTLY, LEFT),
                HDim(month, 'Month', DIRECTLY, ABOVE),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            savepreviewhtml(tidy_sheet, fname="Preview.html")

            tidied_sheets.append(tidy_sheet.topandas())

        tidied_tables[tableTitle] = pd.concat(tidied_sheets)

    elif 'table 2' in tableNumber.lower():

        for tab in tabs:

            tableTitle = tableNumber + ' ' + 'Births in Scotland by month of registration and council area'

            remove = tab.filter('Footnotes').expand(RIGHT).expand(DOWN)

            cell = tab.filter(contains_string(tableNumber))

            area = tab.name

            year = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

            month = cell.shift(2, 4).expand(RIGHT).is_not_blank() - remove

            observations = year.shift(RIGHT).fill(RIGHT).is_not_blank()

            measure_type = 'Births'

            unit = 'Count'

            dimensions = [
                HDimConst('Area', area),
                HDim(year, 'Year', DIRECTLY, LEFT),
                HDim(month, 'Month', DIRECTLY, ABOVE),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            savepreviewhtml(tidy_sheet, fname="Preview.html")

            tidied_sheets.append(tidy_sheet.topandas())

        tidied_tables[tableTitle] = pd.concat(tidied_sheets)

    elif 'table 3' in tableNumber.lower():

        for tab in tabs:

            tableTitle = tableNumber + ' ' + 'Deaths in Scotland by month of registration and NHS Board area'

            remove = tab.filter('Footnotes').expand(RIGHT).expand(DOWN)

            cell = tab.filter(contains_string(tableNumber))

            area = tab.name

            year = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

            month = cell.shift(2, 4).expand(RIGHT).is_not_blank() - remove

            observations = year.shift(RIGHT).fill(RIGHT).is_not_blank()

            measure_type = 'Deaths'

            unit = 'Count'

            dimensions = [
                HDimConst('Area', area),
                HDim(year, 'Year', DIRECTLY, LEFT),
                HDim(month, 'Month', DIRECTLY, ABOVE),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            savepreviewhtml(tidy_sheet, fname="Preview.html")

            tidied_sheets.append(tidy_sheet.topandas())

        tidied_tables[tableTitle] = pd.concat(tidied_sheets)

    elif 'table 4' in tableNumber.lower():

        for tab in tabs:

            tableTitle = tableNumber + ' ' + 'Deaths in Scotland by month of registration and council area'

            remove = tab.filter('Footnotes').expand(RIGHT).expand(DOWN)

            cell = tab.filter(contains_string(tableNumber))

            area = tab.name

            year = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

            month = cell.shift(2, 4).expand(RIGHT).is_not_blank() - remove

            observations = year.shift(RIGHT).fill(RIGHT).is_not_blank()

            measure_type = 'Deaths'

            unit = 'Count'

            dimensions = [
                HDimConst('Area', area),
                HDim(year, 'Year', DIRECTLY, LEFT),
                HDim(month, 'Month', DIRECTLY, ABOVE),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            savepreviewhtml(tidy_sheet, fname="Preview.html")

            tidied_sheets.append(tidy_sheet.topandas())

        tidied_tables[tableTitle] = pd.concat(tidied_sheets)

    elif 'table 5' in tableNumber.lower():

        for tab in tabs:

            tableTitle = tableNumber + ' ' + 'Deaths in Scotland by month of registration and cause of death'

            remove = tab.filter('Footnotes').expand(RIGHT).expand(DOWN)

            cell = tab.filter(contains_string(tableNumber))

            area = cellCont(cell.shift(DOWN))

            year = cell.shift(2, 4).expand(RIGHT).is_not_blank() - remove

            month = cell.shift(1, 5).fill(DOWN).is_not_blank() - remove

            cause_of_death = cell.shift(0, 3).fill(DOWN).is_not_blank() - remove

            observations = month.fill(RIGHT).is_not_blank()

            measure_type = 'Deaths'

            unit = 'Count'

            dimensions = [
                HDimConst('Area', area),
                HDim(year, 'Year', DIRECTLY, ABOVE),
                HDim(month, 'Month', DIRECTLY, LEFT),
                HDim(cause_of_death, 'Cause of Death', CLOSEST, ABOVE),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                ]

            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            savepreviewhtml(tidy_sheet, fname="Preview.html")

            tidied_sheets.append(tidy_sheet.topandas())

        tidied_tables[tableTitle] = pd.concat(tidied_sheets)

tidied_tables

