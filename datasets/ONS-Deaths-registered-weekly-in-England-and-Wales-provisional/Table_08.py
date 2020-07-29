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

# ### Sheet : Covid-19 - Place of occurrence 
# ##### Structure : Week number, Week ended , Region, Deaths type, Place of Occurance , Weekly registrations or occurrences,Value, Measure Type, Unit

# +
for name, tab in tabs.items():
    if (name == 'Covid-19 - Place of occurrence '):
        columns=["Week number", "Period", "Region", "Death classification", "Place of occurance", "Weekly registrations or occurrences", "Marker", "Measure Type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)
        
        remove_footnotes = tab.filter(contains_string('Footnotes:')).expand(RIGHT).expand(DOWN)
        remove_duration_data = tab.filter(contains_string('Deaths registered from 28 December')).expand(DOWN).expand(RIGHT)
        
        week_number = tab.filter(contains_string('Week number')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Week_number('Week number given at cell range: {}', var = excelRange(week_number))

        week_ended = tab.filter(contains_string('Week ended')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Period('Week ended given at cell range: {}', var = excelRange(week_ended))
        
        region = tab.filter(contains_string('England and Wales')).expand(RIGHT).is_not_blank() - remove_duration_data
        trace.Region('Region given at cell range: {}', var = excelRange(region))
        
        death_classification = tab.filter(contains_string('Total deaths')).expand(RIGHT).is_not_blank()
        trace.Death_classification('Death classification given at cell range: {}', var = excelRange(region))
       
        place_of_occurance = tab.filter(contains_string('Home')).expand(DOWN).is_not_blank() - remove_duration_data
        trace.Place_of_occurance('Place of occurance given at cell range: {}', var = excelRange(region))
        
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        reg_or_occ = "Registrations"
        trace.Weekly_registrations_or_occurrences('Hardcoded value as: Registrations') 
        
        
        #Transforming first half of sheet
        observations = place_of_occurance.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(week_number, 'Week number', CLOSEST, LEFT),
            HDim(week_ended, 'Period', CLOSEST, LEFT),
            HDim(region, 'Region', CLOSEST, LEFT),
            HDim(death_classification, 'Death classification', DIRECTLY, ABOVE),
            HDim(place_of_occurance, 'Place of occurance', DIRECTLY, LEFT),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df_4", tidy_sheet.topandas())

        #transforming second half of sheet relating to "Deaths registered from 28 December 2019 to 10 July 2020"
        #note date will therefore be a duration of above date range. 
        period = tab.filter(contains_string('Deaths registered from 28 December'))
        trace.Period('Week ended given at cell range: {}', var = excelRange(period))
        
        region = period.shift(0,1).expand(RIGHT).is_not_blank()
        trace.Region('Region given at cell range: {}', var = excelRange(region))

        place_of_occurance = period.shift(0,1).expand(DOWN).is_not_blank() - remove_footnotes
        trace.Place_of_occurance('Place of occurance given at cell range: {}', var = excelRange(region))
        
        #Transforming Second half of sheet
        observations = place_of_occurance.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(period, 'Period', CLOSEST, LEFT),
            HDim(region, 'Region', CLOSEST, LEFT),
            HDim(death_classification, 'Death classification', DIRECTLY, ABOVE),
            HDim(place_of_occurance, 'Place of occurance', DIRECTLY, LEFT),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            HDimConst('Week number', "n/a"),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df_4", tidy_sheet.topandas()) 

df_4 = trace.combine_and_trace(datasetTitle, "df_4")
df_4.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
# -

from IPython.core.display import HTML
for col in df_4:
    if col not in ['Value']:
        df_4[col] = df_4[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df_4[col].cat.categories) 

tidy_4 = df_4[["Week number", "Period", "Region", "Death classification","Place of occurance", "Weekly registrations or occurrences", "Value", "Measure Type", "Unit"]]

# Notes taken from Tables

notes = """
Weekly provisional figures on deaths registered6 where coronavirus (COVID-19)3 was mentioned on the death certificate, by place of occurrence, in England and Wales

1 Coding of deaths by cause for the latest week is not yet complete.
2 For deaths registered from 1st January 2020, cause of death is coded to the ICD-10 classification using MUSE 5.5 software. Previous years were coded to IRIS 4.2.3, further information about the change in software is available.
3 Deaths involving COVID-19 have been included within weekly death registrations figures due to the pandemic.
4 Does not include deaths where age is either missing or not yet fully coded. For this reason counts of 'Persons', 'Males' and 'Females' may not sum to 'Total Deaths, all ages'.
5 Non-residents are included in the England and Wales total but not England and Wales seperately. For this reason counts for "England" and "Wales" may not sum to "England and Wales".
6 These figures represent death registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release.
7 Deaths at home are those at the usual residence of the deceased (according to the informant)‚ where this is not a communal establishment.
   Care homes includes homes for the chronic sick; nursing homes; homes for people with mental health problems and non-NHS multi function sites.
   Hospices include Sue Ryder Homes; Marie Curie Centres; oncology centres; voluntary hospice units; and palliative care centres.
   Other Communal Establishments include schools for people with learning disabilities; holiday homes and hotels; common lodging houses; aged persons’ accommodation; assessment centres; schools; convents and monasteries; nurses’ homes;
   university and college halls of residence; young offender institutions; secure training centres; detention centres; prisons and remand homes.
   Elsewhere includes all places not covered above such as deaths on a motorway; at the beach; climbing a mountain; walking down the street; at the cinema; at a football match; while out shopping; or in someone else's home.
   This category also includes people who are pronounced dead on arrival at hospital.
8 These figures are calculated using the most up-to-date data we have available to get the most accurate estimates.
9 We have made improvements in the way we code place of death estimates and therefore there may be differences between these and previously published estimates.
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
scraper.dataset.comment = notes
tidy_4.drop_duplicates().to_csv(out / 'observations_4.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy_4

# -
# ______________________________________________________________________________________________________________________
