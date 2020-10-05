#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # WG Attendance at local authority settings during the coronavirus  COVID-19  pandemic

from gssutils import *
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

info = json.load(open('info.json'))

req = Request(info["landingPage"], headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
plaintext = html.decode('utf8')
soup = BeautifulSoup(plaintext)
for a in soup.select('#series--content > div:nth-child(1) > div > div > ul > li > div > div.index-list__title > a'):
    dataPage = a['href']
req = Request(dataPage, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
plaintext = html.decode('utf8')
soup = BeautifulSoup(plaintext)
for a in soup.select('.accordion__content > div > div > div > div > div > div > div.document__details > h3 > a'):
    dataURL = a['href']

with open('info.json', 'r+') as info:
    data = json.load(info)
    data["dataURL"] = dataURL
    info.seek(0)
    json.dump(data, info, indent=4)
    info.truncate()

scrape = Scraper(seed="info.json")
scrape.distributions[0].title = "Attendance at local authority settings during the coronavirus (COVID-19) pandemic"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

try :
    tab = tabs['Table1_Eng']
    cell = tab.filter('Date')
    remove = tab.filter(contains_string('Source:'))
    cell.assert_one()
    authority = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.fill(DOWN).is_not_blank().is_not_whitespace()
    observations = authority.fill(DOWN).is_not_blank().is_not_whitespace() - remove
    Dimensions = [
                HDim(authority,'Local Authority Settings',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDimConst('Unit','Count'),
                HDimConst('Measure Type','Attendence')

    ]
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)

    def user_perc1(x,y):
        if (str(x) ==  'Percentage of Settings') | (str(x) ==  'Percentage of children') | (str(x) ==  'Percentage of staff') :
            return 'Percentage'
        else:
            return y
    new_table['Measure Type'] = new_table.apply(lambda row: user_perc1(row['Local Authority Settings'], row['Measure Type']), axis = 1)

    def user_perc2(x,y):
        if (str(x) ==  'Percentage of Settings') | (str(x) ==  'Percentage of children') | (str(x) ==  'Percentage of staff') :
            return 'percent'
        else:
            return y

    new_table['Unit'] = new_table.apply(lambda row: user_perc2(row['Local Authority Settings'], row['Unit']), axis = 1)
    def date_time(time_value):
        time_string = str(time_value).replace(".0", "").strip()
        time_len = len(time_string)
        if time_len == 10:
            return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
    new_table["Period"] = new_table["Period"].apply(date_time)
    next_table = pd.concat([next_table, new_table])
except:
    print ('Sheet not found')

# Period not defined properly due to variation in date format in source data
# Further updated

try :
    tab = tabs['Table2_Eng']
    cell = tab.filter('Week beginning')
    remove = tab.filter(contains_string('Source:'))
    cell.assert_one()
    authority = cell.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.fill(DOWN).is_not_blank().is_not_whitespace()
    observations = authority.fill(DOWN).is_not_blank().is_not_whitespace() - remove
    Dimensions = [
                HDim(authority,'Local Authority Settings',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDimConst('Unit','Count'),
                HDimConst('Measure Type','Attendence')

    ]
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)

    def user_perc1(x,y):
        if (str(x) ==  'Percentage of Settings') | (str(x) ==  'Percentage of children') | (str(x) ==  'Percentage of staff') :
            return 'Percentage'
        else:
            return y
    new_table['Measure Type'] = new_table.apply(lambda row: user_perc1(row['Local Authority Settings'], row['Measure Type']), axis = 1)

    def user_perc2(x,y):
        if (str(x) ==  'Percentage of Settings') | (str(x) ==  'Percentage of children') | (str(x) ==  'Percentage of staff') :
            return 'percent'
        else:
            return y

    new_table['Unit'] = new_table.apply(lambda row: user_perc2(row['Local Authority Settings'], row['Unit']), axis = 1)
    new_table['Period'] = new_table['Period'].str.rstrip('(a)')
    def date_time(time_value):
        time_string = str(time_value).replace(".0", "").strip()
        time_len = len(time_string)
        if time_len == 10:
            return 'gregorian-day/' + time_string[:10] + 'T00:00/P4D'
    new_table["Period"] = new_table["Period"].apply(date_time)
    next_table = pd.concat([next_table, new_table])
except:
    print ('Sheet not found')

from IPython.core.display import HTML
for col in new_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories)

tidy = next_table[['Period','Local Authority Settings', 'Measure Type','Unit',  'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'Attendance at local authority settings during the coronavirus COVID-19 pandemic_new.csv', index = False)

