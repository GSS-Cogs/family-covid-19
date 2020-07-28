# # ONS Number of deaths in care homes notified to the Care Quality Commission, England 

from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import re
from datetime import datetime


# +
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


info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 
# -

scraper = Scraper(landingPage) 
scraper 

distribution = scraper.distributions[0]

datasetTitle = 'Number of deaths in care homes notified to the Care Quality Commission, England (By Local Authority)'
tabs = { tab: tab for tab in distribution.as_databaker() }
tidied_sheets = []
trace = TransformTrace()
df = pd.DataFrame()

for tab in tabs:
    datacube_name = "Number of deaths in care homes notified to the Care Quality Commission, England (By Local Authority)"
    columns=["Date of Notification", "Place of Occurrence","Death Causes","Local Authority", "Measure Type", "Unit"]
    trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
    
    if tab.name.lower() == 'table 1':
        date_of_notification = tab.filter(contains_string('Date of notification')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Date_of_Notification('Date of notification given at cell range: {}', var = excelRange(date_of_notification))
        
        place_of_occurrrence = tab.filter(contains_string('Date of notification')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Place_of_Occurrence('Place of Occurrence given at cell range: {}', var = excelRange(place_of_occurrrence))
         
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        local_authority = 'England'
        trace.Local_Authority('Hardcoded value as: England')
        death_causes = 'Involving COVID-19'
        trace.Death_Causes('Hardcoded value as: Involving COVID-19')
        observations = place_of_occurrrence.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(date_of_notification, 'Date of notification', DIRECTLY, LEFT),
            HDim(place_of_occurrrence, 'Place of Occurrence', DIRECTLY, ABOVE),
            HDimConst('Local Authority', local_authority),
            HDimConst('Death Causes', death_causes),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("combined_dataframe", tidy_sheet.topandas())
        
    if tab.name.lower() == 'table 2':
        
        date_of_notification = tab.filter(contains_string('Table 2')).shift(0,2).expand(RIGHT).is_not_blank()
        trace.Date_of_Notification('Date of notification given at cell range: {}', var = excelRange(date_of_notification))
        
        local_authority = tab.filter(contains_string('England')).expand(DOWN).is_not_blank()
        trace.Local_Authority('local_authority given at cell range: {}', var = excelRange(local_authority))
            
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        place_of_occurrrence = 'Care homes'
        trace.Place_of_Occurrence('Hardcoded value as: Care homes')
        death_causes = 'Involving COVID-19'
        trace.Death_Causes('Hardcoded value as: Involving COVID-19')
        observations = date_of_notification.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(date_of_notification, 'Date of notification', DIRECTLY, ABOVE),
            HDim(local_authority, 'Local Authority', DIRECTLY, LEFT),
            HDimConst('Place of Occurrence', place_of_occurrrence),
            HDimConst('Death Causes', death_causes),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("combined_dataframe", tidy_sheet.topandas())
        
    if tab.name.lower() == 'table 3':
        
        date_of_notification = tab.filter(contains_string('Table 3')).shift(0,2).expand(RIGHT).is_not_blank()
        trace.Date_of_Notification('Date of notification given at cell range: {}', var = excelRange(date_of_notification))
        
        local_authority = tab.filter(contains_string('England')).expand(DOWN).is_not_blank()
        trace.Local_Authority('local_authority given at cell range: {}', var = excelRange(local_authority))
            
        measure_type = 'Deaths'
        trace.Measure_Type('Hardcoded value as: Deaths')
        unit = 'Count'
        trace.Unit('Hardcoded value as: Count')
        place_of_occurrrence = 'Care homes'
        trace.Place_of_Occurrence('Hardcoded value as: Care homes')
        death_causes = 'All causes'
        trace.Death_Causes('Hardcoded value as: All causes')
        observations = date_of_notification.fill(DOWN).is_not_blank()
        
        dimensions = [
            HDim(date_of_notification, 'Date of notification', DIRECTLY, ABOVE),
            HDim(local_authority, 'Local Authority', DIRECTLY, LEFT),
            HDimConst('Place of Occurrence', place_of_occurrrence),
            HDimConst('Death Causes', death_causes),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
       # savepreviewhtml(tidy_sheet) 
        trace.store("combined_dataframe", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

tidy = df[["Date of notification", "Place of Occurrence",'Value', "Death Causes","Local Authority", "Measure Type", "Unit"]]
trace.Place_of_Occurrence("Remove any prefixed whitespace from all values in column and pathify")
trace.Death_Causes("Remove any prefixed whitespace from all values in column and pathify")
trace.Local_Authority("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Place of Occurrence', 'Death Causes', "Local Authority"):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
tidy['Value'] = tidy['Value'].astype(int)

# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

# Notes taken from Tables : 1, 2, 3

notes = """
1. Data provided by Care Quality Commission.
2. Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 3 Jul 2020, and may be an underestimate due to notification delays.
3. Figures are for persons who were resident in and died in a care home.
"""

# +
dte = pd.DataFrame(columns=['Per'])
dte['Per'] = pd.to_datetime(df['Date of notification'][df['Date of notification'] != 'All Deaths'].unique())
min_date = dte['Per'].min()
date_range = abs((dte['Per'].max() - dte['Per'].min()).days)

print('Date range from Table_02 script: ' + str(date_range) + ' Days')
print('Minimum date from Table_02 script: ' + str(min_date))
date_range_str = 'gregorian-interval/' + str(min_date).replace(' ','T') + '/P' + str(date_range) + 'D'
print('Formatted date range string: ' + date_range_str)
df = df.rename(columns={'Date of notification': 'Period', 'Death Causes': 'Cause of Death', 'Place of Occurrence': 'Location of Death'})
# -

df = df.rename(columns={'Date of notification': 'Period', 'Death Causes': 'Cause of Death', 'Place of Occurrence': 'Location of Death'})
df['Period'] = 'gregorian-interval/' + df['Period'].str.strip() + 'T00:00:00/P1D'
df = df[df['Location of Death'] != 'Location not stated']
df1 = df

df['Period'][df['Period'].str.contains('All Deaths')] = date_range_str

# Table 4

# +
datasetTitle = 'Number of deaths involving COVID-19 in care homes residents by place of occurrence, by week of notification England'
trace = TransformTrace()
tab = next(t for t in tabs.values() if t.name.startswith('Table 4'))
print(tab.name)

datacube_name = "Number of deaths involving COVID-19 in care homes residents by place of occurrence, by week of notification England"
columns=["Week Ending", "Place of Occurrence","Death Causes","Local Authority", "Measure Type", "Unit"]
trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)

#Week ending
week_ending = tab.filter(contains_string('Week Ending')).shift(1,0).expand(RIGHT).is_not_blank()
print(week_ending)
trace.Week_Ending('Date of notification given at cell range: {}', var = excelRange(week_ending))
        
death_cause_options = ['All deaths', 'Deaths involving COVID-19']
death_causes = tab.filter(contains_string('All deaths')).expand(DOWN).one_of(death_cause_options)
trace.Death_Causes('Death Causes given at cell range: {}', var = excelRange(death_causes)) 
        
place_of_occurrrence = tab.filter(contains_string('All deaths')).expand(DOWN).is_not_blank() - death_causes
trace.Place_of_Occurrence('Place of Occurrence given at cell range: {}', var = excelRange(place_of_occurrrence))

measure_type = 'Deaths'
trace.Measure_Type('Hardcoded value as: Deaths')
unit = 'Count'
trace.Unit('Hardcoded value as: Count')
local_authority = 'England'
trace.Local_Authority('Hardcoded value as: England')
observations = week_ending.fill(DOWN).is_not_blank()  
        
dimensions = [
    HDim(week_ending, 'Week Ending', DIRECTLY, ABOVE),
    HDim(death_causes, 'Death Causes', CLOSEST, ABOVE),
    HDim(place_of_occurrrence, 'Place of Occurrence', DIRECTLY, LEFT),
    HDimConst('Local Authority', local_authority),
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
tidy = df[["Week Ending", "Place of Occurrence",'Value', "Death Causes","Local Authority", "Measure Type", "Unit"]]

trace.Place_of_Occurrence("Remove any prefixed whitespace from all values in column and pathify")
trace.Death_Causes("Remove any prefixed whitespace from all values in column and pathify")
trace.Local_Authority("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Place of Occurrence', 'Death Causes', "Local Authority"):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
tidy['Value'] = tidy['Value'].astype(int)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

# Notes taken from Table : 4

notes = """
1. Data provided by Care Quality Commission.
2. Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 3 Jul 2020, and may be an underestimate due to notification delays.
3. Figures are for persons who were resident in a care home.
4. Figures don't include 10 April 2020 as the first full week of data for deaths involving COVID-19 began on 11 April 2020.
"""

from datetime import datetime, timedelta
df = df.rename(columns={'Week Ending': 'Period', 'Death Causes': 'Cause of Death', 'Place of Occurrence': 'Location of Death'})
df['Period'] = pd.to_datetime(df['Period'])
df['Period'] = df['Period'] - timedelta(days=6)
df['Period'] = df['Period'].dt.strftime('%Y-%m-%d')
df['Period'] = 'gregorian-interval/' + df['Period'].str.strip() + 'T00:00:00/P7D'
df2 = df

cols = ['Period', 'Location of Death', 'Local Authority', 'Cause of Death', 'Measure Type', 'Unit', 'Value']

df1 = df1[cols]
df2 = df2[cols]

joined_dat = pd.concat([df1, df2])

from rdflib import Graph
import rdflib as rd
g = Graph()
g.parse("../../Reference/reference-geography.ttl", format="ttl")

laslist = list(joined_dat['Local Authority'].unique())
las = pd.DataFrame(joined_dat['Local Authority'].unique())
las.rename(columns={0 : 'Category'}, inplace=True)
las['Code'] = ''

for la in laslist:
    q = (f"SELECT ?s ?p ?o WHERE  {{ ?s ?p '{la.strip()}' . ?s <http://www.w3.org/2000/01/rdf-schema#label> ?o . }}")
    try:
        qres = g.query(q)
        for row in qres:
            las['Code'][las['Category'] == la.strip()] = row[2].strip()
            break
    except Exception as e:
        print("No Match!")

joined_dat['Local Authority'] = joined_dat['Local Authority'].map(las.set_index('Category')['Code'])

joined_dat['Location of Death'] = joined_dat['Location of Death'].apply(pathify)
joined_dat['Local Authority'] = joined_dat['Local Authority'].apply(pathify)
joined_dat['Cause of Death'] = joined_dat['Cause of Death'].apply(pathify)
joined_dat['Measure Type'] = joined_dat['Measure Type'].apply(pathify)
joined_dat['Unit'] = joined_dat['Unit'].apply(pathify)

joined_dat = joined_dat.rename(columns={'Cause of Death' : 'ONS Cause of Death'})
joined_dat = joined_dat.rename(columns={'Location of Death' : 'ONS Location of Death'})
joined_dat.head(10)

# Output the data to CSV
csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat.drop_duplicates().to_csv(out / csvName, index = False)

# +
scraper.dataset.family = 'covid-19'
scraper.dataset.description = 'ONS Number of deaths in care homes notified to the Care Quality Commission, England.\n ' + notes

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name)) + '-' + pathify(csvName)
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
#### scraper.dataset.title = 'ONS Number of deaths in care homes notified to the Care Quality Commission'
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

joined_dat.head(6)

info = json.load(open('info.json')) 
codelistcreation = info['transform']['codelists'] 
print(codelistcreation)
print("-------------------------------------------------------")
print(joined_dat.columns)


codeclass = CSVCodelists()
for cl in codelistcreation:
    if cl in joined_dat.columns:
        joined_dat[cl] = joined_dat[cl].str.replace("-"," ")
        joined_dat[cl] = joined_dat[cl].str.capitalize()
        codeclass.create_codelists(pd.DataFrame(joined_dat[cl]), 'codelists', scraper.dataset.family, Path(os.getcwd()).name)



