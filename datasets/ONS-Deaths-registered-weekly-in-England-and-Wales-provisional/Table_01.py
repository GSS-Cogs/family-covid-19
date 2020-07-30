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

# +
###  Sheet : Weekly figures 2020
##### Structure : Week number, Week ended, Sex, Age Group, Region, Weekly registrations or occurrences , Death grouped by, Death cause, Value, Measure Type, Unit
# -

for name, tab in tabs.items():
    if (name == 'Weekly figures 2020'):
        columns=["Week number", "Week ended", "Weekly registrations or occurrences", "Sex", "Age group", "Region", "Death grouped by", "Death cause", "Marker", "Measure Type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)

        remove_footnotes = tab.filter(contains_string('Footnotes:')).expand(RIGHT).expand(DOWN)
        
        week_number = tab.filter(contains_string('Week number')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_number('Week number given at cell range: {}', var = excelRange(week_number))
        
        week_ended = tab.filter(contains_string('Week ended')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_ended('Week ended given at cell range: {}', var = excelRange(week_ended))

        region = tab.filter(contains_string('Deaths by region of usual')).shift(0,1).expand(DOWN).is_not_blank() - remove_footnotes
        trace.Region('Week ended given at cell range: {}', var = excelRange(region))
        
        death_grouped_by = 'Deaths by region of usual residence'
        trace.Death_grouped_by('Hardcoded value as: Deaths by region of usual residence')
        sex = 'Persons'
        trace.Sex('Hardcoded value as: Persons')
        age_group = 'All ages'
        trace.Age_group('Hardcoded value as: All ages')
        death_cause = 'unknown'
        trace.Death_cause('Hardcoded value as: unknown')
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        reg_or_occ = "Registrations"
        trace.Weekly_registrations_or_occurrences('Hardcoded value as: Registrations and Occurrences')
        
        ######   Transform region data (bottom of sheet) #########
        observations = region.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(region, 'Region', DIRECTLY, LEFT), 
            HDimConst('Sex', sex),
            HDimConst('Age group', age_group),
            HDimConst('Death cause', death_cause),
            HDimConst('Death grouped by', death_grouped_by),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())
        
        
        ######   Transform age group data #########
        remove_region_data = tab.filter(contains_string('Deaths by region of usual residence')).expand(RIGHT).expand(DOWN)
        
        age_group_defined = tab.filter(contains_string('Deaths by age group')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Deaths by age group')) - tab.filter(contains_string('Males 6')) - tab.filter(contains_string('Females 6')) - tab.filter(contains_string('Persons 6')) - remove_region_data 
        trace.Age_group('Age group given at cell range: {}', var = excelRange(age_group_defined))
                
        sex_defined = tab.filter(contains_string('Persons 6')).expand(DOWN).is_not_blank() - tab.filter(contains_string('Deaths by age group'))  - remove_region_data - age_group_defined
        trace.Sex('Sex given at cell range: {}', var = excelRange(sex_defined))
        
        death_grouped_by = 'Deaths by age group'
        trace.Death_grouped_by('Hardcoded value as: Deaths by age group')
        region = 'England and Wales'
        trace.Region('Hardcoded value as: England and Wales')
        
        observations = age_group_defined.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(age_group_defined, 'Age group', DIRECTLY, LEFT), 
            HDim(sex_defined, 'Sex', CLOSEST, ABOVE), 
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Death cause', death_cause),
            HDimConst('Measure Type', measure_type),
            HDimConst('Region', region),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())
        
         ######   Transform Death cause data #########
        remove_age_data = tab.filter(contains_string('Persons 6')).expand(RIGHT).expand(DOWN)
        death_grouped_by = 'Deaths by cause'
        trace.Death_grouped_by('Hardcoded value as: Deaths by cause')
        death_cause_by_cause = tab.filter(contains_string('Deaths by cause 2,3,4,5')).shift(0,1).expand(DOWN).is_not_blank() - remove_age_data  - remove_region_data - age_group_defined
        trace.Death_cause('Sex given at cell range: {}', var = excelRange(death_cause_by_cause))

        observations = death_cause_by_cause.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(death_cause_by_cause, 'Death cause', DIRECTLY, LEFT),
            HDimConst('Sex', sex),
            HDimConst('Age group', age_group),
            HDimConst('Region', region),
            HDimConst('Death grouped by', death_grouped_by),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())
        
         ######   Transform Total Death data #########
        remove =  tab.filter(contains_string('Note: Deaths could possibly')).expand(RIGHT).expand(DOWN)
        death_grouped_by = tab.filter(contains_string('Total deaths,')).expand(DOWN).is_not_blank() - remove
        trace.Death_grouped_by('Sex given at cell range: {}', var = excelRange(death_grouped_by))

        observations = death_grouped_by.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', DIRECTLY, ABOVE),
            HDim(week_ended, 'Week ended', DIRECTLY, ABOVE),
            HDim(death_grouped_by, 'Death grouped by', DIRECTLY, LEFT),
            HDim(death_grouped_by, 'Region', DIRECTLY, LEFT), #will need filtered as this info is included in death_grouped_by
            HDimConst('Sex', sex),
            HDimConst('Age group', age_group),
            HDimConst('Death cause', death_cause),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datasetTitle, "df")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
df = df.replace({'Region' : { "Total deaths, all ages" : "England and Wales",
                             "week over the previous 5 years 1 (Wales)" : "Wales",
                            "week over the previous 5 years 1 (England)" : "England", 
                            "week over the previous 5 years 1 (England and Wales)" : "England and Wales"}})

df = df.replace({'Death grouped by' : { 
                             "week over the previous 5 years 1 (Wales)" : "Total deaths: average of corresponding week over the previous 5 years 1",
                            "week over the previous 5 years 1 (England)" : "Total deaths: average of corresponding week over the previous 5 years 1", 
                            "week over the previous 5 years 1 (England and Wales)" : "Total deaths: average of corresponding week over the previous 5 years 1"}})

# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

tidy = df[["Week number", "Week ended", "Weekly registrations or occurrences", "Sex", "Age group", "Region", "Death grouped by", "Death cause", "Value", "Measure Type", "Unit"]]


# Notes taken from Tables

notes = """
Note that up-to-date counts of the total numbers of deaths involving coronavirus (COVID-19) are published by Department of Health and Social Care (DHSC) on the .GOV.UK website. ONS figures differ from the DHSC counts as the latter include deaths which have not yet been registered.
1 This average is based on the actual number of death registrations recorded for each corresponding week over the previous five years. Moveable public holidays, when register offices are closed, affect the number of registrations made in the published weeks and in the corresponding weeks in previous years.
2 Counts of deaths by underlying cause exclude deaths at age under 28 days. Counts of deaths involving Covid-19 will include neonatals.
3 Coding of deaths by cause for the latest week is not yet complete.
4 For deaths registered from 1st January 2020, cause of death is coded to the ICD-10 classification using MUSE 5.5 software. Previous years were coded to IRIS 4.2.3, further information about the change in software is available.
5 An 'underlying cause of death' refers to the main cause of death, whereas a cause being 'mentioned on the death certificate' means that it might be the main reason or a contributory reason to the cause of death.
6 Does not include deaths where age is either missing or not yet fully coded. For this reason counts of 'Persons', 'Males' and 'Females' may not sum to 'Total Deaths, all ages'.
7 Does not include deaths of those resident outside England and Wales or those records where the place of residence is either missing or not yet fully coded. For this reason counts for "Deaths by Region of usual residence" may not sum to "Total deaths, all ages".
8 These figures represent death registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release.
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
scraper.dataset.comment = notes
tidy.drop_duplicates().to_csv(out / 'observations_1.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy

# -



# ______________________________________________________________________________________________________________________
