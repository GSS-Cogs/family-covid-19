# # ONS Deaths involving COVID-19, England and Wales 

from gssutils import * 
import json 
from datetime import datetime

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper 

distribution = scraper.distributions[0]
distribution

# +
datasetTitle = 'Number of deaths due to COVID-19, age-specific and age-standardised rates by sex, England and Wales'
tabs = { tab: tab for tab in distribution.as_databaker() }
tidied_sheets = []
trace = TransformTrace()
df = pd.DataFrame()

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

def decimal(s):
    try:
        float(s)
        if float(s) >= 1:
            return True
        else:
            return False
    except ValueError:
        return False

month_look_up = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 
                  'July':'07','August':'08','September':'09', 'October':'10','November':'11', 'December':'12'}
def date_time(time_value):
    date_string = time_value.strip()
    if len(date_string)  == 2:
        return 'month/2020-' + date_string


# +
#df = trace.combine_and_trace(datacube_name, "combined_dataframe")
#df.rename(columns={'OBS' : 'Value'}, inplace=True)
#trace.add_column("Value")
#trace.Value("Rename databaker columns OBS to Value")
#tidy = df[['Period', 'Value', 'All causes 2020', 'Five year average', 'Measure Type', 'Unit']]

# +
trace = TransformTrace()
tab = next(t for t in tabs.values() if t.name.startswith('Table 3'))
print(tab.name)

datacube_name = "Number of deaths due to COVID-19, age-specific and age-standardised rates by sex, England and Wales"

columns=['Period', 'Age Group', 'Sex', 'Country', 'Rate', 'Lower CI', 'Upper CI', 'Measure Type', 'Unit']
trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)

period = tab.filter(contains_string('March')).expand(RIGHT).is_not_blank()
trace.Period('Period detailed at cell value: {}', var = cellLoc(period))

age_group = tab.filter(contains_string('All ages')).expand(DOWN).is_not_blank()
trace.Age_Group('All ages detailed at cell value: {}', var = cellLoc(age_group))

country_type = ['England and Wales', 'England', 'Wales']
country = tab.excel_ref('B10').expand(DOWN).one_of(country_type)
trace.Country('Country detailed at cell value: {}', var = cellLoc(country))

sex = tab.filter(contains_string('All ages')).shift(0,-3).expand(RIGHT).is_not_blank()
trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))

remove = tab.filter(contains_string('Number of deaths')).expand(RIGHT)
rate = tab.filter(contains_string('Lower 95% CI')).shift(-2,1).expand(DOWN).is_not_blank() - remove
trace.Rate('Rate detailed at cell value: {}', var = cellLoc(rate))

marker = tab.filter(contains_string('Lower 95% CI')).shift(-1,0).expand(DOWN) - remove

lower_CI = tab.filter(contains_string('Lower 95% CI')).shift(0,1).expand(DOWN) - remove
trace.Lower_CI('Values found in range: {}')

upper_CI = tab.filter(contains_string('Upper 95% CI')).shift(0,1).expand(DOWN).is_not_blank() - remove
trace.Upper_CI('Values found in range: ')

remove_all_country = tab.filter(contains_string('All ages')).shift(0,-4).expand(RIGHT).is_not_blank()

observations = tab.filter(contains_string('Lower 95% CI')).shift(-3,1).expand(DOWN).is_not_blank() - remove - sex - remove_all_country


measure_type = 'Count'
trace.Measure_Type('Hardcoded value as: Count')
unit = 'Deaths'
trace.Unit('Hardcoded value as: Deaths')

dimensions = [
    HDim(period, 'Period', CLOSEST, LEFT),
    HDim(age_group, 'Age Group', DIRECTLY, LEFT),
    HDim(country, 'Country', CLOSEST, ABOVE),
    HDim(sex, 'Sex', DIRECTLY, ABOVE),
    HDim(rate, 'Rate', DIRECTLY, RIGHT),
    HDim(lower_CI, 'Lower CI', DIRECTLY, RIGHT),
    HDim(upper_CI, 'Upper CI', DIRECTLY, RIGHT),
    HDim(marker, 'Marker', DIRECTLY, RIGHT),
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
trace.Period("Formating period column to month/{year}-{month}")
df['Period'] = df['Period'].apply(lambda x: month_look_up[x])
df["Period"] = df["Period"].apply(date_time)

df = df.replace({'Marker' : {
    'U' : 'unreliable - Age-specific rates, fewer than 20 deaths'}})

tidy = df[['Period', 'Value', 'Age Group', 'Country', 'Sex', 'Rate', 'Lower CI', 'Upper CI', 'Marker', 'Measure Type', 'Unit' ]]
trace.Country("Remove any prefixed whitespace from all values in column and pathify")
trace.Sex("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Country', "Sex"):
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


# Notes taken from Table 

notes = """
1. England and Wales includes deaths of non-residents. England and Wales separately excludes deaths of non-residents
2. Based on boundaries as of May 2020
3. COVID-19 defined as ICD10 codes U07.1 and U07.2
4. Based on the date a death occurred rather than when a death was registered
5. : Rates are not available where there are less than 3 deaths
6. Age-specific rates where there were fewer than 20 deaths are unreliable and denoted with a u
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

