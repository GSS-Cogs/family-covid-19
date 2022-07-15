#!/usr/bin/env python
# coding: utf-8

# In[295]:


# ONS Deaths involving COVID-19 in the care sector, England and Wales 

from gssutils import *
import datetime
from datetime import timedelta
import json 
import logging
import re
import isodate


# In[296]:


#### Add transformation script here #### 

scraper = Scraper(seed="info.json") 
tabs = scraper.distribution(latest=True).as_databaker()
source_sheet = scraper.distribution(latest=True).downloadURL
print("Using source data", source_sheet)
scraper


# In[297]:


def tabs_from_named(tabs, wanted):
    """Given all labs and a list of tab names wanted, return the ones we want, raise if they're not here"""
    wanted = [wanted] if not isinstance(wanted, list) else wanted
    wanted_tabs = [x for x in tabs if x.name.strip() in wanted]
    assert len(wanted_tabs) == len(wanted),         f"Could not find tab name {','.join(wanted)} in tabs {','.join([x.name for x in tabs])}"
    return wanted_tabs

class is_type(object):
    """Filter to match cell on type of cell.value"""
    
    def __init__(self, type_wanted):
        self.type_wanted = type_wanted
        
    def __call__(self, cell):
        return True if type(cell.value) == self.type_wanted else False

def get_date_range(title):
    """
    Given a title cell, extract a range date for use as period
    
    example title cell:
    -------------------
    Number of deaths of care home residents by date of death (ONS) and date of notification (CQC and CIW), 
     from 28 December 2019 to 12 June 2020, registered up to 20 June 2020 1,2,3,4,5,6,7,8
    """
    
    # get rid of rogue whitespace....sigh
    title = " ".join([x for x in title.split(" ") if len(x) > 0])
    
    # Cut out string title so we've mainly time left
    # TODO - likely to be fragile
    if "from week ending" in title:
        title = "".join(title.split("from week ending ")[1:])
    elif "day of notification" in title:
        title = "".join(title.split("day of notification ")[1:])
    elif "from" in title:
        title = "".join(title.split("from ")[1:])
    elif "deaths occurring from" in title:
        title = "".join(title.split("deaths occurring from")[1:])
    else:
        title = "".join(title.split("date of notification ")[1:])

    # Use re to check there's the expected date format
    months = "(January|February|March|April|May|June|July|August|September|October|November|December)"
    r_query = "\d+ {} \d{} to \d+ {} \d{}".format(months, "{4}", months, "{4}")
    m = re.match(r'{}'.format(r_query), title)
    
    # Assert found and cut the bit we want
    assert m is not None, f"Cannot find the expected date string in the title '{title}'."
    date_string = title[:m.span()[1]]
    
    # Get and format the start
    start_of_interval_obj = datetime.datetime.strptime(date_string.split("to")[0].strip(), '%d %B %Y')
    start_of_interval_str = start_of_interval_obj.strftime('%Y-%m-%dT00:00:00')
    
    # Get and format the duration
    end_of_interval_obj = datetime.datetime.strptime(date_string.split("to")[1].strip(), '%d %B %Y')
    duration_str = isodate.duration_isoformat(end_of_interval_obj-start_of_interval_obj)
    
    t = f"gregorian-interval/{start_of_interval_str}/{duration_str}"
    print(t)
    
    return t

def create_tidy(cs, tab_name):
    """Wrap some standard operations to avoid repeating ourselves"""
    df = cs.topandas().fillna("")

    # rename stuff
    df = df.rename(columns={"OBS":"Value", "DATAMARKER":"Marker"})

    return df

import requests

class Geography(object):
    """
    We're going to 'borrow' a json representation of the admin hierarchy to do
    some basic lookups of area codes.
    """

    def __init__(self, url, overrides={}):
        self.url = url
        r = requests.get(self.url)
        if r.status_code != 200:
            raise Exception("Failed to get geography codes off cmd, status code {},from url {}"                            .format(r.status_code, self.url))
        self.json = r.json()
        
        # Where the same label is used for two codes, we use an overrides dict to pass in 
        # specific choices
        self.overrides = overrides
        
    def __call__(self, label):
        
        if label in self.overrides.keys():
            return self.overrides[label]
        else:
            found = []
            for item in self.json["items"]:
                if item["label"].lower().strip() == label.lower().strip():
                    found.append(item["code"])
            assert len(found) == 1, f"There is not exactly one code for {label} on {self.url}."                             f" Instead we got: {','.join(found)}"
            return found[0]

region_overrides = {
     'England and Wales': 'K04000001',
     'England': 'E92000001',
     'Wales': 'W92000004',
     'East': 'E12000006'
}

get_regions = Geography("https://api.beta.ons.gov.uk/v1/code-lists/regions/editions/2017/codes", 
                        overrides=region_overrides)

local_authority_overrides = {
     'England and Wales': 'K04000001',
     'England': 'E92000001',
     'Wales': 'W92000004'
}
get_local_authorities = Geography("https://api.beta.ons.gov.uk/v1/code-lists/local-authority/editions/2016/codes", 
                                overrides=local_authority_overrides)


# In[298]:


all_dat = {}


# In[299]:


# ## Transform: Table 1

for tab in tabs_from_named(tabs, "Table_1"):
    
    try:
        date_cell = tab.filter("Week\nending")
        
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))

        cause_of_death = date_cell.fill(RIGHT).is_not_blank()

        week = tab.filter('Week\nnumber').fill(DOWN)

        obs = cause_of_death.waffle(period) - tab.filter(contains_string('5 year average')).fill(DOWN)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(week, "Week", DIRECTLY, LEFT),
            HDim(cause_of_death, "Cause of Death", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 1 Preview.html")
        
        all_dat["table 1"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[300]:


df = all_dat['table 1'].replace(r'\n',' ', regex=True) 

df['Area'] = df['Cause of Death'].str.split(',').str[1].str.strip()
df['Cause of Death'] = df['Cause of Death'].str.split(',').str[0].str.strip()

df['Week'] = df['Week'].astype(float).astype(int)

df['Period'] = 'week/' + df['Period'].str.split('-').str[0] + '-W' + df['Week'].astype(str)

df = df.replace({'Area' : { 'England and Wales': 'K04000001',
                            'England': 'E92000001',
                            'Wales': 'W92000004'}})

df['Sex'] = 'all'

df['Age'] = 'all'

df['Place of Death'] = 'all'

df['Marker'] = ''

df['Measure Type'] = 'count'
df['Unit'] = 'deaths'

df = df.reindex(sorted(df.columns), axis=1)

df = df.drop(columns=['Week'])

df.to_csv("table 1.csv", index=False)

all_dat["table 1"] = df

df


# In[301]:


# ## Transform: Table 2

for tab in tabs_from_named(tabs, "Table_2"):
    
    try:
        first_persons_cell = tab.excel_ref('B').filter(contains_string("All deaths,\n"))

        sex = tab.filter("Age groups").fill(RIGHT).is_not_blank()
        
        causeofdeath = tab.filter("Age groups").fill(RIGHT).is_not_blank()

        area = tab.filter("Age groups").shift(UP)

        obs = causeofdeath.fill(DOWN).is_not_blank() - tab.filter("Age groups").expand(RIGHT)

        age = obs.fill(LEFT) - obs
    
        dimensions = [
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(causeofdeath, "Cause of Death", DIRECTLY, ABOVE),
            HDim(area, "Area", CLOSEST, ABOVE),
            HDimConst("Period", get_date_range(tab.excel_ref('A1').value))
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 2 Preview.html")
        
        all_dat['table 2'] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[302]:


df = all_dat['table 2'].replace(r'\n',' ', regex=True) 

df['Sex'] = df['Sex'].str.split(',').str[1].str.strip()
df['Cause of Death'] = df['Cause of Death'].str.split(',').str[0].str.strip()
df['Area'] = df['Area'].str.split(',').str[2].str.split('[').str[0].str.strip()

df['Measure Type'] = df.apply(lambda x: 'percentage' if '%' in x['Cause of Death'] else 'count', axis = 1)

df['Unit'] = df.apply(lambda x: 'percent' if '%' in x['Cause of Death'] else 'deaths', axis = 1)

df = df.replace({'Area' : { 'England and Wales': 'K04000001',
                            'England': 'E92000001',
                            'Wales': 'W92000004'}})

df['Place of Death'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)                           

df.to_csv("table 2.csv", index=False)

all_dat['table 2'] = df

all_dat['table 2']


# In[303]:


# ## Transform: Table 3

for tab in tabs_from_named(tabs, "Table_3"):
    
    try:
        date_cell = tab.filter("Week\nending")
        
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))

        place_of_death = date_cell.fill(RIGHT).is_not_blank()

        week = tab.filter('Week\nnumber').fill(DOWN)

        obs = place_of_death.waffle(period)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(week, "Week", DIRECTLY, LEFT),
            HDim(place_of_death, "Place of Death", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 3 Preview.html")

        df["Cause of Death"] = "all"
        
        all_dat["table 3"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[304]:


df = all_dat['table 3'].replace(r'\n',' ', regex=True) 

df['Area'] = df['Place of Death'].str.split(',').str[1].str.strip()
df['Place of Death'] = df['Place of Death'].str.split(',').str[0].str.strip()

df['Week'] = df['Week'].astype(float).astype(int)

df['Period'] = 'week/' + df['Period'].str.split('-').str[0] + '-W' + df['Week'].astype(str)

df = df.replace({'Area' : { 'England and Wales': 'K04000001',
                            'England': 'E92000001',
                            'Wales': 'W92000004'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)

df = df.drop(columns=['Week'])

df.to_csv("table 3.csv", index=False)

all_dat["table 3"] = df

all_dat['table 3']


# In[305]:


# ## Transform: Table 4

for tab in tabs_from_named(tabs, "Table_4"):
    
    try:
        date_cell = tab.filter("Week\nending")
        
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))

        place_of_death = date_cell.fill(RIGHT).is_not_blank()

        week = tab.filter('Week\nnumber').fill(DOWN)

        obs = place_of_death.waffle(period)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(week, "Week", DIRECTLY, LEFT),
            HDim(place_of_death, "Place of Death", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 4 Preview.html")

        df["Cause of Death"] = "involving covid-19"
        
        all_dat["table 4"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[306]:


df = all_dat['table 4'].replace(r'\n',' ', regex=True) 

df['Area'] = df['Place of Death'].str.split(',').str[1].str.strip()
df['Place of Death'] = df['Place of Death'].str.split(',').str[0].str.strip()

df['Week'] = df['Week'].astype(float).astype(int)

df['Period'] = 'week/' + df['Period'].str.split('-').str[0] + '-W' + df['Week'].astype(str)

df = df.replace({'Area' : { 'England and Wales': 'K04000001',
                            'England': 'E92000001',
                            'Wales': 'W92000004'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)

df = df.drop(columns=['Week'])

df.to_csv("table 4.csv", index=False)

all_dat["table 4"] = df

all_dat['table 4']


# In[307]:


# ## Transform: Table 5

for tab in tabs_from_named(tabs, "Table_5"):
    
    try:
        date_cell = tab.filter("Week\nending")
        
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))

        area = date_cell.fill(RIGHT).is_not_blank()

        week = tab.filter('Week\nnumber').fill(DOWN)

        obs = area.waffle(period) - tab.filter("Wales").expand(DOWN)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(week, "Week", DIRECTLY, LEFT),
            HDim(area, "Area", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 5 Preview.html")

        df["Cause of Death"] = "all"

        df["Place of Death"] = "all"
        
        all_dat["table 5"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[308]:


df = all_dat['table 5'].replace(r'\n',' ', regex=True) 

df['Week'] = df['Week'].astype(float).astype(int)

df['Period'] = 'week/' + df['Period'].str.split('-').str[0] + '-W' + df['Week'].astype(str)

df['Area'] = df['Area'].str.strip()

df = df.replace({'Area' : {'All households' : 'E92000001',
                           'East of England' : 'E12000006',
                           'East Midlands' : 'E12000004',
                           'London' : 'E12000007',
                           'North East' : 'E12000001',
                           'North West' : 'E12000002',
                           'South East' : 'E12000008',
                           'South West' : 'E12000009',
                           'West Midlands' : 'E12000005',
                           'Yorkshire and The Humber' : 'E12000003',
                           'all' : 'E92000001',
                           'Wales': 'W92000004'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)

df = df.drop(columns=['Week'])

df.to_csv("table 5.csv", index=False)

all_dat["table 5"] = df

all_dat['table 5']


# In[309]:


# ## Transform: Table 6

for tab in tabs_from_named(tabs, "Table_6"):
    
    try:
        date_cell = tab.filter("Week\nending")
        
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))

        area = date_cell.fill(RIGHT).is_not_blank()

        week = tab.filter('Week\nnumber').fill(DOWN)

        obs = area.waffle(period) - tab.filter("Wales").expand(DOWN)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(area, "Area", DIRECTLY, ABOVE),
            HDim(week, "Week", DIRECTLY, LEFT)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 6 Preview.html")

        df["Cause of Death"] = "involving covid-19"

        df["Place of Death"] = "all"
        
        all_dat["table 6"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[310]:


df = all_dat['table 6'].replace(r'\n',' ', regex=True) 

df['Week'] = df['Week'].astype(float).astype(int)

df['Period'] = 'week/' + df['Period'].str.split('-').str[0] + '-W' + df['Week'].astype(str)

df['Area'] = df['Area'].str.strip()

df = df.replace({'Area' : {'All households' : 'E92000001',
                           'East of England' : 'E12000006',
                           'East Midlands' : 'E12000004',
                           'London' : 'E12000007',
                           'North East' : 'E12000001',
                           'North West' : 'E12000002',
                           'South East' : 'E12000008',
                           'South West' : 'E12000009',
                           'West Midlands' : 'E12000005',
                           'Yorkshire and The Humber' : 'E12000003',
                           'all' : 'E92000001',
                           'Wales': 'W92000004'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)

df = df.drop(columns=['Week'])

df.to_csv("table 6.csv", index=False)

all_dat["table 6"] = df

all_dat['table 6']


# In[311]:


# ## Transform: Table 7

for tab in tabs_from_named(tabs, "Table_7"):
    
    try:
        area = tab.filter("Area Code").fill(DOWN).is_not_blank()

        period = tab.filter("Area Code").shift(2, 0).expand(RIGHT).is_not_blank()

        obs = period.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 7 Preview.html")

        df["Cause of Death"] = "all"

        df["Place of Death"] = "Care Home"
        
        all_dat["table 7"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[312]:


df = all_dat['table 7'].replace(r'\n',' ', regex=True) 

df['Period'] = df['Period'].str.split(',').str[1].str.strip()

df['Period'] = df.apply(lambda x: 'gregorian-interval/2020-03-14T00:00:00/P292' if '2020' in x['Period'] else 'gregorian-interval/2021-01-01T00:00:00/P385', axis = 1)

df = df.replace({'Marker' : {'z' : 'unavailable'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df = df.reindex(sorted(df.columns), axis=1)

df.to_csv("table 7.csv", index=False)

all_dat["table 7"] = df

all_dat['table 7']


# In[313]:


# ## Transform: Table 8

for tab in tabs_from_named(tabs, "Table_8"):
    
    try:
        area = tab.filter("Area Code").fill(DOWN).is_not_blank()

        period = tab.filter("Area Code").shift(2, 0).expand(RIGHT).is_not_blank()

        obs = period.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 8 Preview.html")

        df["Cause of Death"] = "involving covid-19"

        df["Place of Death"] = "Care Home"
        
        all_dat["table 8"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[314]:


df = all_dat['table 8'].replace(r'\n',' ', regex=True) 

df['Period'] = df['Period'].str.split(',').str[1].str.strip()

df['Period'] = df.apply(lambda x: 'gregorian-interval/2020-03-14T00:00:00/P292' if '2020' in x['Period'] else 'gregorian-interval/2021-01-01T00:00:00/P385', axis = 1)

df = df.replace({'Marker' : {'z' : 'unavailable'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Sex'] = 'all'

df['Age'] = 'all'

df = df.reindex(sorted(df.columns), axis=1)

df.to_csv("table 8.csv", index=False)

all_dat["table 8"] = df

all_dat['table 8']


# In[315]:


# ## Transform: Table 9

for tab in tabs_from_named(tabs, "Table_9"):
    
    try:
        cause_of_death = tab.filter("Leading cause code").fill(DOWN).is_not_blank()

        area = tab.filter("Leading cause name").shift(RIGHT).expand(RIGHT).is_not_blank()
        
        sex = tab.filter("Leading cause name").shift(RIGHT).expand(RIGHT).is_not_blank()

        obs = area.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(cause_of_death, "Cause of Death", DIRECTLY, LEFT),
            HDim(area, "Area", DIRECTLY, ABOVE),
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDimConst("Period", get_date_range(tab.excel_ref('A1').value))
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)

        savepreviewhtml(cs, fname="Table 9 Preview.html")

        df["Place of Death"] = "Care Home"
        
        all_dat["table 9"] = df
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e


# In[316]:


df = all_dat['table 9'].replace(r'\n',' ', regex=True) 

df['Sex'] = df['Area'].str.split(',').str[0].str.strip()
df['Area'] = df['Area'].str.split(',').str[1].str.strip()

df['Cause of Death'] = df['Cause of Death'].str.strip()

df = df.replace({'Area' : { 'England and Wales': 'K04000001',
                            'England': 'E92000001',
                            'Wales': 'W92000004'}})

df['Measure Type'] = 'count'

df['Unit'] = 'deaths'

df['Age'] = 'all'

df['Marker'] = ''

df = df.reindex(sorted(df.columns), axis=1)

df.to_csv("table 9.csv", index=False)

all_dat["table 9"] = df

all_dat['table 9']


# In[317]:


df = pd.concat(all_dat.values())

df = df.replace({'Age' : {'All ages' : 'all',
                          '90+' : '90-plus'},
                 'Sex' : {'Female' : 'F', 
                          'Females' : 'F', 
                          'Male' : 'M', 
                          'Males' : 'M', 
                          'Persons' : 'T', 
                          'all' : 'T'},
                 'Cause of Death' : {'involving covid-19' : 'involving-covid-19',
                                     'Proportion of deaths involving COVID-19 (%)' : 'involving-covid-19',
                                     'Deaths involving COVID-19' : 'involving-covid-19',
                                     'All deaths' : 'all'}})

df['Place of Death'] = df['Place of Death'].apply(pathify)
df['Cause of Death'] = df['Cause of Death'].apply(pathify)

df['Value'] = df.apply(lambda x: '0' if x['Marker'] != '' else x['Value'], axis = 1)

df['Marker'] = df.apply(lambda x: x['Marker'] if x['Marker'] == 'unavailable' else 'N/A', axis = 1)

df = df[['Period', 'Area', 'Age', 'Sex', 'Cause of Death', 'Place of Death', 'Value', 'Marker', 'Measure Type', 'Unit']]

df


# In[318]:


df.to_csv('observations.csv', index=False)

catalog_metadata = scraper.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file('catalog-metadata.json')


# In[319]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)

