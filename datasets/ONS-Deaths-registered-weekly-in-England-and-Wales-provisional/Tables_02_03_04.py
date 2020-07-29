# -*- coding: utf-8 -*-
# # ONS Deaths registered weekly in England and Wales, provisional 

# +
from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import re
from datetime import datetime

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



# -

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage)  
tabs = { tab.name: tab for tab in scraper.distributions[0].as_databaker() }
datasetTitle = 'ONS Deaths registered weekly in England and Wales'
trace = TransformTrace()
df = pd.DataFrame()
list(tabs)

# ###  3 Sheets : Covid-19 - Weekly registrations,  Covid-19 - Weekly occurrences, UK - Covid-19 - Weekly reg
# ##### Firstly Transforming Sheets : Covid-19 - Weekly registrations and  Covid-19 - Weekly occurrences
# ##### Structure : Week number, Week ended, Sex, Age Group, Region, Weekly registrations or occurrences , Value, Measure Type, Unit
# ###### Note, dimension "Occurance or Registration" is just what I have named it, for now, to differentiate between the two sheets but there is definitely a better naming convention for the dimension. 
#

for name, tab in tabs.items():
    if (name == 'Covid-19 - Weekly registrations') or (name == 'Covid-19 - Weekly occurrences'):

        columns=["Week number", "Week ended", "Weekly registrations or occurrences", "Sex", "Age group", "Region", "Marker", "Measure Type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)
        
        remove_region_data = tab.filter(contains_string('Deaths by region of usual residence')).expand(DOWN).expand(RIGHT)

        week_number = tab.filter(contains_string('Week number')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_number('Week number given at cell range: {}', var = excelRange(week_number))

        week_ended = tab.filter(contains_string('Week ended')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_ended('Week ended given at cell range: {}', var = excelRange(week_ended))

        #note blank value for age_group = "Deaths involving COVID-19, all ages1"
        age_group = tab.filter(contains_string('Week ended')).shift(1,3).expand(DOWN) - tab.filter(contains_string('Deaths by age group')) - tab.filter(contains_string('Males')) - tab.filter(contains_string('Females')) - tab.filter(contains_string('Persons')) - remove_region_data
        trace.Age_group('Age group given at cell range: {}', var = excelRange(age_group))

        sex = tab.filter(contains_string('Week ended')).shift(1,2).expand(DOWN) - tab.filter(contains_string('Deaths by age group'))  - remove_region_data - age_group
        trace.Sex('Sex given at cell range: {}', var = excelRange(sex))
        #observations for first part of sheet, representing different age groups
        observations = week_ended.fill(DOWN).is_not_blank() - remove_region_data

        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')

        # region of "England and Wales" only applicable to the first part of the sheet. 
        region_all = 'England and Wales'
        trace.Region('Hardcoded value as: England and Wales to represent all values') 
        
        reg_or_occ = "Registrations"
        if (name == 'Covid-19 - Weekly occurrences'):
            reg_or_occ = "Occurrences"
            trace.Weekly_registrations_or_occurrences('Hardcoded value as: Occurrences') 
        trace.Weekly_registrations_or_occurrences('Hardcoded value as: Registrations') 

        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(age_group, 'Age group', DIRECTLY, LEFT), #Blank Value = All ages
            HDim(sex, 'Sex', CLOSEST, ABOVE),  #Blank values = Persons
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Region', region_all),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df_2", tidy_sheet.topandas())

        region = tab.filter(contains_string('Deaths by region of usual residence')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Region('Region given at cell range: {}', var = excelRange(region))

        sex = 'Persons'
        trace.Sex('Hardcoded value as: Count')
        age_group = 'All ages'
        trace.Age_group('Hardcoded value as: all ages')
        #observations for second part of sheet, representing different Regions
        observations = region.fill(RIGHT).is_not_blank()

        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Sex', sex),
            HDimConst('Age group', age_group),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df_2", tidy_sheet.topandas())

# ### Separately transform Sheet: UK - Covid-19 - Weekly reg
# ##### Structure : Week number, Week ended, Sex, Age Group, Region, Weekly registrations or occurrences , Value, Measure Type, Unit
#

for name, tab in tabs.items():
    if (name == 'UK - Covid-19 - Weekly reg'):

        columns=["Week number", "Week ended", "Weekly registrations or occurrences", "Sex", "Age group", "Region", "Marker", "Measure Type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)
        
        remove_age_data = tab.filter(contains_string('Deaths involving COVID-19 by age')).expand(DOWN).expand(RIGHT)
        remove_footnotes = tab.filter(contains_string('Footnotes:')).expand(RIGHT).expand(DOWN) 
       
        week_number = tab.filter(contains_string('Week number')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_number('Week number given at cell range: {}', var = excelRange(week_number))

        week_ended = tab.filter(contains_string('Week ended')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_ended('Week ended given at cell range: {}', var = excelRange(week_ended))
        
        #Blank value = all UK
        region = tab.filter(contains_string('UK deaths involving COVID-19, all ages')).shift(1,0).expand(DOWN) - remove_age_data
        trace.Region('Region given at cell range: {}', var = excelRange(region))
        
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        sex = 'Persons'
        trace.Sex('Hardcoded value as: Count')
        age_group = 'All ages'
        trace.Age_group('Hardcoded value as: all ages')
        reg_or_occ = "Registrations"
        trace.Weekly_registrations_or_occurrences('Hardcoded value as: Registrations') 
        
        #Transform first part of sheet relating to region data
        observations = week_ended.fill(DOWN).is_not_blank() - remove_age_data
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Sex', sex),
            HDimConst('Age group', age_group),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())
    
        #note blank value for age_group = "Deaths involving COVID-19, all ages1"
        age_group = tab.filter(contains_string('Deaths involving COVID-19 by age')).shift(1,3).expand(DOWN).is_not_blank() - tab.filter(contains_string('Deaths by age group')) - tab.filter(contains_string('Males')) - tab.filter(contains_string('Females')) - tab.filter(contains_string('Persons')) - remove_footnotes 
        trace.Age_group('Age group given at cell range: {}', var = excelRange(age_group))
        
        sex = tab.filter(contains_string('Persons - UK')).expand(DOWN).is_not_blank() - tab.filter(contains_string('Deaths by age group'))  - remove_footnotes - age_group
        trace.Sex('Sex given at cell range: {}', var = excelRange(sex))
        
        region = 'England and Wales'
        trace.Region('Hardcoded value as: England and Wales to represent all values')
        
        observations = age_group.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(age_group, 'Age group', DIRECTLY, LEFT), #Blank Value = All ages
            HDim(sex, 'Sex', CLOSEST, ABOVE),  #Blank values = Persons
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Region', region),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df_2", tidy_sheet.topandas())

# ##### Join sheets Covid-19 - Weekly registrations,  Covid-19 - Weekly occurrences, UK - Covid-19 - Weekly reg
# ##### and fix up any obvious structural issues. 

df_2 = trace.combine_and_trace(datasetTitle, "df_2")
df_2.rename(columns={'OBS' : 'Value'}, inplace=True)
df_2 = df_2.replace({'Sex' : { "" : "Persons"}})
df_2 = df_2.replace({'Age group' : { "" : "All ages"}})
df_2 = df_2.replace({'Region' : { "" : "All UK"}})
df_2['Week number'] = df_2.apply(lambda x: x['Week number'].replace('.0', ''), axis = 1)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")       

from IPython.core.display import HTML
for col in df_2:
    if col not in ['Value']:
        df_2[col] = df_2[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df_2[col].cat.categories) 

tidy_2 = df_2[["Week number", "Week ended", "Weekly registrations or occurrences", "Sex", "Age group", "Region","Value", "Measure Type", "Unit"]] 

# Notes taken from Tables

notes = """
Note that up-to-date counts of the total numbers of deaths involving coronavirus (COVID-19) are published by Department of Health and Social Care (DHSC) on the .GOV.UK website. ONS figures differ from the DHSC counts as the latter include deaths which have not yet been registered.

1 Coding of deaths by cause for the latest week is not yet complete.
2 For deaths registered from 1st January 2020, cause of death is coded to the ICD-10 classification using MUSE 5.5 software. Previous years were coded to IRIS 4.2.3, further information about the change in software is available.
3 Deaths involving COVID-19 have been included within weekly death registrations figures due to the pandemic.
4 Does not include deaths where age is either missing or not yet fully coded. For this reason counts of 'Persons', 'Males' and 'Females' may not sum to 'Total Deaths, all ages'.
5 Does not include deaths of those resident outside England and Wales or those records where the place of residence is either missing or not yet fully coded. For this reason counts for "Deaths by Region of usual residence" may not sum to "Total deaths, all ages".
6 These figures represent death registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release. 
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
scraper.dataset.comment = notes
tidy_2.drop_duplicates().to_csv(out / 'observations_2.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy_2

# -

# ______________________________________________________________________________________________________________________
