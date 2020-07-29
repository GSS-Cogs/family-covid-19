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

# ### 3 Sheets : Covid-19 - E&W comparisons, Covid-19 - England comparisons, Covid-19 - Wales comparison
# ##### Structure : Date, Region, Comparison Category, Weekly registrations or occurrences , Value, Measure Type, Unit
#
#

# +
for name, tab in tabs.items():
    if (name == 'Covid-19 - E&W comparisons') or (name == 'Covid-19 - England comparisons') or (name == 'Covid-19 - Wales comparison'):
        remove_footnotes = tab.filter(contains_string('Footnotes:')).expand(RIGHT).expand(DOWN)
        
        columns=["Date", "Region", "Comparison Category", "Weekly registrations or occurrences", "Measure Type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)
 
        date = tab.filter(contains_string('Date')).shift(0,1).expand(DOWN).is_not_blank() - remove_footnotes
        trace.Date('Date given at cell range: {}', var = excelRange(date))
         
        comparision_cat = tab.filter(contains_string('Date')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Comparison_Category('Comparison Category given at cell range: {}', var = excelRange(comparision_cat))
        
        region = 'England and Wales'
        trace.Region('Hardcoded value as: England and Wales to represent all values')
        if (name == 'Covid-19 - England comparisons'):
            region = 'England'
            trace.Region('Hardcoded value as: England')
        elif (name == 'Covid-19 - Wales comparison'):
            region = 'Wales'
            trace.Region('Hardcoded value as: Wales')
    
        reg_or_occ = "Registrations and Occurrences"
        trace.Weekly_registrations_or_occurrences('Hardcoded value as: Registrations and Occurrences') 
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        
        observations = date.fill(RIGHT).is_not_blank()
        dimensions = [
            HDim(date, 'Date', DIRECTLY, LEFT),
            HDim(comparision_cat, 'Comparison Category', DIRECTLY, ABOVE),
            HDimConst('Region', region),
            HDimConst('Weekly registrations or occurrences', reg_or_occ),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet_2 = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet_2)
        #savepreviewhtml(tidy_sheet_2) 
        trace.store("df_3", tidy_sheet_2.topandas())

df_3 = trace.combine_and_trace(datasetTitle, "df_3")
df_3.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
# -
from IPython.core.display import HTML
for col in df_3:
    if col not in ['Value']:
        df_3[col] = df_3[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df_3[col].cat.categories) 

tidy_3 = df_3[["Date", "Region", "Comparison Category", "Weekly registrations or occurrences", "Value", "Measure Type", "Unit"]]


# Notes taken from Tables

notes = """
Note that up-to-date counts of the total numbers of deaths involving coronavirus (COVID-19) are published by Department of Health and Social Care (DHSC) on the .GOV.UK website. ONS figures differ from the DHSC counts as the latter include deaths which have not yet been registered.
1 Data is provisional.
2 Figures include deaths of non-residents.
3 Figures for the latest week are based on boundaries as of May 2020.
4 Figures for deaths occurring only include deaths that were registered by the date indicated, so may be an underestimate due to registration delays. More information on registration delays for a range of causes can be found on the ONS website via the link below.
Impact of registration delays on mortality statistics in England and Wales: 2018 (latest)
5 DHSC death counts are taken the next day. For example, deaths reported on the 6 March were used for 5 March.
6 Counts are cumulative.
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
scraper.dataset.comment = notes
tidy_3.drop_duplicates().to_csv(out / 'observations_3.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy_3

