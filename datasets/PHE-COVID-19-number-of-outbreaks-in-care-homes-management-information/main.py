# -*- coding: utf-8 -*-
# # PHE COVID-19  number of outbreaks in care homes – management information 

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

def date_time (date):
    if len(date)  == 10:
        return 'gregorian-interval/' + date + 'T00:00:00/P7D'
    else:
        return 'year/2020'


# -

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "PHE COVID-19 number of outbreaks in care homes – management information"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
datasetTitle = 'PHE COVID-19 number of outbreaks in care homes – management information'
trace = TransformTrace()
df = pd.DataFrame()
list(tabs)

for name, tab in tabs.items():
    if 'Metadata' in name:
        continue
    elif (name == 'Government_office_regions') or (name == 'PHE_centres'):
        columns=["Week commencing", "Categorised by", "Region","Area code","All outbreaks", "Number of care homes", "Percentage of care homes that have reported an outbreak", "Measure Type", "Unit"]
    else:
        columns=["Week commencing", "Categorised by", "Region","Area code","All outbreaks", "Number of care homes", "Measure Type", "Unit"]
    trace.start(datasetTitle, tab, columns, scrape.distributions[0].downloadURL)
    
    remove_1 = tab.filter(contains_string('All outbreaks')).expand(RIGHT)
    
    week_commencing = tab.filter(contains_string('Week commencing')).shift(0,1).expand(RIGHT).is_not_blank() - remove_1
    trace.Week_commencing('Week commencing given at cell range: {}', var = excelRange(week_commencing))
    
    all_outbreaks = tab.filter(contains_string('All outbreaks')).shift(0,1).expand(DOWN).is_not_blank() 
    trace.All_outbreaks('All outbreaks given at cell range: {}', var = excelRange(all_outbreaks))
    
    num_care_homes = tab.filter(contains_string('Number of care homes')).shift(0,1).expand(DOWN).is_not_blank() 
    trace.Number_of_care_homes('All outbreaks given at cell range: {}', var = excelRange(num_care_homes))
    
    if (name == 'Government_office_regions'):
        categorised_by = "Government office region"
        trace.Categorised_by('Hardcoded value as: Government office region')
        
        area_code = tab.filter(contains_string('Government office region')).shift(1,1).expand(DOWN).is_not_blank() 
        trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
        
        region = tab.filter(contains_string('Government office region')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Region('region given at cell range: {}', var = excelRange(region))
        
        outbreak_percentage = tab.filter(contains_string('Percentage of care homes that have reported an outbreak')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Percentage_of_care_homes_that_have_reported_an_outbreak('Percentage of care homes that have reported an outbreak given at cell range: {}', var = excelRange(outbreak_percentage))
        
    if (name == 'PHE_centres'):
        categorised_by = "PHE Centres"
        trace.Categorised_by('Hardcoded value as: PHE Centres')
        
        area_code = tab.filter(contains_string('PHE centre')).shift(1,1).expand(DOWN).is_not_blank() 
        trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
        
        region = tab.filter(contains_string('PHE centre')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Region('region given at cell range: {}', var = excelRange(region))
        
        outbreak_percentage = tab.filter(contains_string('Percentage of care homes that have reported an outbreak')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Percentage_of_care_homes_that_have_reported_an_outbreak('Percentage of care homes that have reported an outbreak given at cell range: {}', var = excelRange(outbreak_percentage))
    
    if (name == 'Upper_Tier_Local_authorities'):
        categorised_by = "Local Authority Upper Tier"
        trace.Categorised_by('Hardcoded value as: Local Authority Upper Tier')
        
        area_code = tab.filter(contains_string('Local Authority')).shift(1,1).expand(DOWN).is_not_blank() 
        trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
        
        region = tab.filter(contains_string('Government office region')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Region('region given at cell range: {}', var = excelRange(region))

    if (name == 'Lower_Tier_Local_authorities'):
        categorised_by = "Local Authority Lower Tier"
        trace.Categorised_by('Hardcoded value as: Local Authority Lower Tier')
        
        area_code = tab.filter(contains_string('Local Authority')).shift(1,1).expand(DOWN).is_not_blank() 
        trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
     
        region = tab.filter(contains_string('Government office region')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Region('region given at cell range: {}', var = excelRange(region))
    
    measure_type = 'Outbreaks of COVID-19'
    trace.Measure_Type('Hardcoded value as: Deaths')
    unit = 'Count'
    trace.Unit('Hardcoded value as: Count')
    observations = area_code.waffle(week_commencing)
    
    if ((name == 'Government_office_regions') or (name == 'PHE_centres')):
        dimensions = [
            HDim(week_commencing, 'Week commencing', DIRECTLY, ABOVE),
            HDim(area_code, 'Area code', DIRECTLY, LEFT),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDim(all_outbreaks, 'All outbreaks', DIRECTLY, RIGHT),
            HDim(num_care_homes, 'Number of care homes', DIRECTLY, RIGHT),
            HDim(outbreak_percentage, 'Percentage of care homes that have reported an outbreak', DIRECTLY, RIGHT),
            HDimConst('Categorised by', categorised_by),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet) 
        trace.store("sheets_1_2", tidy_sheet.topandas())
        
    elif ((name == 'Upper_Tier_Local_authorities') or (name == 'Lower_Tier_Local_authorities')):
        dimensions = [
            HDim(week_commencing, 'Week commencing', DIRECTLY, ABOVE),
            HDim(area_code, 'Area code', DIRECTLY, LEFT),
            HDim(region, 'Region', DIRECTLY, LEFT),
            HDim(all_outbreaks, 'All outbreaks', DIRECTLY, RIGHT),
            HDim(num_care_homes, 'Number of care homes', DIRECTLY, RIGHT),
            HDimConst('Categorised by', categorised_by),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet) 
        trace.store("sheets_3_4", tidy_sheet.topandas())
        

# +
df_1_2 = trace.combine_and_trace(datasetTitle, "sheets_1_2")
df_3_4 = trace.combine_and_trace(datasetTitle, "sheets_3_4")
tidied_sheets = [df_1_2, df_3_4]

for df in tidied_sheets:
    df.rename(columns={'OBS' : 'Value'}, inplace=True)
    trace.add_column("Value")
    trace.Value("Rename databaker columns OBS to Value")

    trace.Week_commencing("Formating to gregorian-interval/YYY-MM-DDT00:00:00/P7D")
    df['Week commencing'] =  df["Week commencing"].apply(date_time)
    trace.Week_commencing("Renaming label to Period")
    df.rename(columns={'Week commencing' : 'Period'}, inplace=True)
# -

tidy_1_2 = df_1_2[["Period", 'Value', "Categorised by", "Region","Area code", "Measure Type", "Unit", "All outbreaks", "Number of care homes", "Percentage of care homes that have reported an outbreak"]]
tidy_3_4 = df_3_4[["Period", 'Value', "Categorised by", "Region","Area code", "Measure Type", "Unit", "All outbreaks", "Number of care homes"]]

out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
tidy_1_2.drop_duplicates().to_csv(out / f'{title}_1.csv', index = False)
tidy_3_4.drop_duplicates().to_csv(out / f'{title}_2.csv', index = False)
