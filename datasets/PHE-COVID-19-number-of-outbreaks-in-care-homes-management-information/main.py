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
tidied_sheets = []
trace = TransformTrace()
df = pd.DataFrame()
list(tabs)

for name, tab in tabs.items():
    
    datacube_name = "Number of deaths in care homes notified to the Care Quality Commission, England (By Local Authority)"
    columns=["Week commencing", "Categorised by", "Region","Area code","All outbreaks", "Number of care homes", "Percentage of care homes that have reported an outbreak", "Measure Type", "Unit"]
    trace.start(datacube_name, tab, columns, scrape.distributions[0].downloadURL)

    if name == 'Government_office_regions':
        categorised_by = "Government office region"
        trace.Categorised_by('Hardcoded value as: Government office region')
        remove_1 = tab.filter(contains_string('All outbreaks')).expand(RIGHT)
        
        week_commencing = tab.filter(contains_string('Week commencing')).shift(0,1).expand(RIGHT).is_not_blank() - remove_1
        trace.Week_commencing('Week commencing given at cell range: {}', var = excelRange(week_commencing))
           
        area_code = tab.filter(contains_string('Government office region')).shift(1,1).expand(DOWN).is_not_blank() 
        trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
        
        region = tab.filter(contains_string('Government office region')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Region('region given at cell range: {}', var = excelRange(region))
       
        all_outbreaks = tab.filter(contains_string('All outbreaks')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.All_outbreaks('All outbreaks given at cell range: {}', var = excelRange(all_outbreaks))

        num_care_homes = tab.filter(contains_string('Number of care homes')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Number_of_care_homes('All outbreaks given at cell range: {}', var = excelRange(num_care_homes))

        outbreak_percentage = tab.filter(contains_string('Percentage of care homes that have reported an outbreak')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Percentage_of_care_homes_that_have_reported_an_outbreak('Percentage of care homes that have reported an outbreak given at cell range: {}', var = excelRange(outbreak_percentage))

        measure_type = 'Outbreaks of COVID-19'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        observations = area_code.waffle(week_commencing)
        
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
        trace.store("combined_dataframe", tidy_sheet.topandas())
        
    if name == 'PHE_centres':
        categorised_by = "PHE Centres"
        trace.Categorised_by('Hardcoded value as: PHE Centres')
        remove_1 = tab.filter(contains_string('All outbreaks')).expand(RIGHT)
        
        week_commencing = tab.filter(contains_string('Week commencing')).shift(0,1).expand(RIGHT).is_not_blank() - remove_1
        trace.Week_commencing('Week commencing given at cell range: {}', var = excelRange(week_commencing))
           
        area_code = tab.filter(contains_string('PHE centre')).shift(1,1).expand(DOWN).is_not_blank() 
        #trace.Area_code('Area code given at cell range: {}', var = excelRange(area_code))
        
        region = tab.filter(contains_string('PHE centre')).shift(0,1).expand(DOWN).is_not_blank() 
        #trace.Region('region given at cell range: {}', var = excelRange(region))
       
        all_outbreaks = tab.filter(contains_string('All outbreaks')).shift(0,1).expand(DOWN).is_not_blank() 
        #trace.All_outbreaks('All outbreaks given at cell range: {}', var = excelRange(all_outbreaks))

        num_care_homes = tab.filter(contains_string('Number of care homes')).shift(0,1).expand(DOWN).is_not_blank() 
        #trace.Number_of_care_homes('All outbreaks given at cell range: {}', var = excelRange(num_care_homes))

        outbreak_percentage = tab.filter(contains_string('Percentage of care homes that have reported an outbreak')).shift(0,1).expand(DOWN).is_not_blank() 
        #trace.Percentage_of_care_homes_that_have_reported_an_outbreak('Percentage of care homes that have reported an outbreak given at cell range: {}', var = excelRange(outbreak_percentage))

        measure_type = 'Outbreaks of COVID-19'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        observations = area_code.waffle(week_commencing)
        
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
        trace.store("combined_dataframe", tidy_sheet.topandas())



# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

trace.Week_commencing("Formating to gregorian-interval/YYY-MM-DDT00:00:00/P7D")
df['Week commencing'] =  df["Week commencing"].apply(date_time)
trace.Week_commencing("Renaming label to Period")
df.rename(columns={'Week commencing' : 'Period'}, inplace=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

tidy = df[["Period", 'Value', "Categorised by", "Region","Area code", "Measure Type", "Unit", "All outbreaks", "Number of care homes", "Percentage of care homes that have reported an outbreak"]]
tidy

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
#scraper.dataset.comment = notes
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
#scraper.dataset.family = 'covid-19'

#df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
#with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())
#trace.output()
#tidy
# -


