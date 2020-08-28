# # ONS Online job advert estimates 

# +
from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import numpy as np
from urllib.parse import urljoin
import os

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

scrape = Scraper(landingPage)  
distribution = scrape.distributions[0]

datasetTitle = 'Online job advert estimates'
tabs = { tab: tab for tab in distribution.as_databaker() }
trace = TransformTrace()
df = pd.DataFrame()

# +
for tab in tabs:
   
    columns=["Date", "Industry", "NUTS1 Region", 'Marker', "Measure Type", "Unit"]
    trace.start(datasetTitle, tab, columns, scrape.distributions[0].downloadURL)
    
    remove_notes = tab.filter(contains_string('Notes')).expand(RIGHT).expand(DOWN)
    measure_type = 'Job Advert Indices'
    trace.Measure_Type('Hardcoded value as: Adverts')
    unit = 'Percent'
    trace.Unit('Hardcoded value as: Count')
    
    if tab.name == 'Vacancies by Adzuna Category':
        
        date = tab.filter(contains_string('Date')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Date('Date given at cell range: {}', var = excelRange(date))

        imputed_values = tab.filter(contains_string('Imputed values')).shift(1,0).expand(RIGHT)
        trace.Marker('Imputed Values given at cell range: {}', var = excelRange(date))
        
        industry = tab.filter(contains_string('Date')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Imputed values')).expand(RIGHT).expand(DOWN)
        trace.Industry('Industry given at cell range: {}', var = excelRange(date))

        nuts1_region = "United Kingdom"
        trace.NUTS1_Region("Hardcoded as United Kingdom")
        
        observations = industry.fill(RIGHT).is_not_blank() 
        dimensions = [
            HDim(date, 'Date', DIRECTLY, ABOVE),
            HDim(industry, 'Industry', DIRECTLY, LEFT),
            HDim(imputed_values, 'Marker', DIRECTLY, BELOW),
            HDimConst('NUTS1 Region', nuts1_region),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
       # savepreviewhtml(tidy_sheet) 
        trace.store("combined_dataframe", tidy_sheet.topandas())
    
    if tab.name == 'Vacancies by NUTS1 Region':
       
        date = tab.filter(contains_string('Date')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Date('Date given at cell range: {}', var = excelRange(date))
        
        imputed_values = tab.filter(contains_string('Imputed values')).shift(1,0).expand(RIGHT)
        trace.Marker('Imputed Values given at cell range: {}', var = excelRange(date))

        nuts1_region = tab.filter(contains_string('Date')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Imputed values')).expand(RIGHT).expand(DOWN)
        trace.NUTS1_Region('Industry given at cell range: {}', var = excelRange(date))
        
        industry = "All"
        trace.Industry("Hardcoded as All")
      
        observations = nuts1_region.fill(RIGHT).is_not_blank() 
        dimensions = [
            HDim(date, 'Date', DIRECTLY, ABOVE),
            HDim(nuts1_region, 'NUTS1 Region', DIRECTLY, LEFT),
            HDim(imputed_values, 'Marker', DIRECTLY, BELOW),
            HDimConst('Industry', industry),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
            ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("combined_dataframe", tidy_sheet.topandas())
        
        


# +
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)

#imputed values are highlighted in spreadsheet
f1=((df['Marker'] !='') )
df.loc[f1,'Marker'] = 'Imputed'

trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")
trace.Date("Formating to day/YYY-MM-DD")
df['Date'] = df['Date'].map(lambda x: f'day/{x}')
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

# +
tidy = df[['Date', 'Industry', 'NUTS1 Region', 'Measure Type', 'Unit', 'Value', 'Marker']]

trace.Industry("Remove any prefixed whitespace from all values in column and pathify")
trace.NUTS1_Region("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Industry', 'NUTS1 Region'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
# -

del tidy['Measure Type']
del tidy['Unit']

tidy['Marker'] = tidy['Marker'].str.lower()
tidy.head(60)

# Notes taken from tab: Vacancies

notes = """
Total job adverts by Adzuna Category, Index 2019 average = 100
1. The observations were collected on a roughly weekly basis; however they were not all collected at the same point in each week, leading to slightly irregular gaps between each observation.
2. Furthermore some weeks have no observation. The missing  values have been imputed using linear interpolation, and have been highlighted.
3. The education industry's total online job adverts estimate for the 21st of March 2019 was an anomaly, and the value was imputed through linear interpolation.
4. The 2019 average values used to index the series were calculated after imputing the missing weeks.
5. The Adzuna categories used do not correspond to SIC categories.
6. There is an increased level of duplication in the Management/exec/consulting category for the 19th June 2020, resulting in a potentially inflated value for total job adverts in this category.
7. Historically the health and social care category has shown a strong correlation with the ONS Vacancy Survey, but from April 2020 it has increasingly diverged from the vacancies data.

"""

#SET UP OUTPUT FOLDER AND OUTPUT DATA TO CSV
csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / csvName, index = False)

#SET VARIOUS ATTRIBUTES OF THE SCRAPER
scrape.dataset.family = 'covid-19'
scrape.dataset.title = datasetTitle
scrape.dataset.comment = notes
dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)

# CREATE MAPPING CLASS INSTANCE, SET UP VARIABLES AND WRITE FILES
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')

# CREATE AND OUTPUT TRIG FILE
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())

# +
newTxt = ''
info = json.load(open('info.json')) 
mtp = info['transform']['columns']['Value']['measure'].replace('http://gss-data.org.uk/def/measure/','')
mt = mtp.capitalize()
mtpath = f'''"@id": "http://gss-data.org.uk/def/measure/{mtp}",'''
h = '''"@id": "http://purl.org/linked-data/sdmx/2009/attribute#unitMeasure",'''

with open("out/observations.csv-metadata.json") as fp: 
    for line in fp: 
        if mtpath in line.strip():
            print(line)
            newTxt = newTxt + line + '''\t"rdfs:label": "''' + mt + '''",\n'''
        else:
            newTxt += line
            
f = open("out/observations.csv-metadata.json", "w")
f.write(newTxt)
f.close()
# -

trace.output()


