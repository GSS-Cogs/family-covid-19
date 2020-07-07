# # ONS Online job advert estimates 

# +
from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import numpy as np

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
distribution = scraper.distributions[0]

datasetTitle = 'Online job advert estimates'
tabs = { tab: tab for tab in distribution.as_databaker() }
trace = TransformTrace()
df = pd.DataFrame()

# +
tab = next(t for t in tabs.values() if t.name.startswith('Vacancies'))
datacube_name = "Online job advert estimates"
columns=["Date", "Industry", 'Marker', "Measure Type", "Unit"]
trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)

date = tab.filter(contains_string('Date')).shift(1,0).expand(RIGHT).is_not_blank()
trace.Date('Date given at cell range: {}', var = excelRange(date))

industry = tab.filter(contains_string('Date')).shift(0,1).expand(DOWN).is_not_blank()
trace.Industry('Industry given at cell range: {}', var = excelRange(date))

imputed_values = tab.filter(contains_string('Imputed values')).shift(1,0).expand(RIGHT)
trace.Marker('Imputed Values given at cell range: {}', var = excelRange(date))

measure_type = 'Adverts'
trace.Measure_Type('Hardcoded value as: Adverts')
unit = 'Count'
trace.Unit('Hardcoded value as: Count')
observations = industry.fill(RIGHT).is_not_blank() - imputed_values

dimensions = [
    HDim(date, 'Date', DIRECTLY, ABOVE),
    HDim(industry, 'Industry', DIRECTLY, LEFT),
    HDim(imputed_values, 'Marker', DIRECTLY, BELOW),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
    ]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet) 
trace.store("combined_dataframe", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

trace.Marker("Fixing up marker column with information taken from the notes : 'Furthermore some weeks have no observation. The missing values have been imputed using linear interpolation, and have been highlighted.'")
f1=((df['Marker'] =='Education only') & (df['Industry'] =='Education'))
df.loc[f1,'Marker'] = 'Values have been imputed using linear interpolation'

df = df.replace({'Marker' : {'All' : 'Values have been imputed using linear interpolation', 'Education only' : np.nan, '' : np.nan }})

tidy = df[["Date", "Industry",'Value', "Marker", "Measure Type", "Unit"]]


trace.Industry("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Industry'):
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

# Output Tidy data

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
scraper.dataset.comment = notes
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
scraper.dataset.family = 'covid-19'

import os
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
trace.output()
tidy
