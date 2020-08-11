# -*- coding: utf-8 -*-
# # ONS Which occupations have the highest potential exposure to the coronavirus  COVID-19 

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

df = pd.DataFrame()
trace = TransformTrace()
# -

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Which occupations have the highest potential exposure to the coronavirus (COVID-19)?"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

# ##### Sheet: Occupations and exposure

# +
tab = tabs['Occupations and exposure']
datacube_name = "Which occupations have the highest potential exposure to the coronavirus (COVID-19)?"
columns=['Measure type', 'UK SOC 2010 Code', 'Occupation title', 'Total in employment', 'Median hourly pay', 'Percentage of the workforce that are female', 'Percentage of the workforce that are aged 55 plus', 'Percentage of the workforce that are BAME', 'Unit']
trace.start(datacube_name, tab, columns, scrape.distributions[0].downloadURL)

cell = tab.filter(contains_string('Occupations and exposure to disease data'))
cell.assert_one()

soc_codes = cell.shift(0,3).expand(DOWN).is_not_blank()
trace.UK_SOC_2010_Code('UK SOC 2010 Code given at cell range: {}', var = excelRange(soc_codes))

occupation_title = cell.shift(1,3).expand(DOWN).is_not_blank()
trace.Occupation_title('Occupation title given at cell range: {}', var = excelRange(occupation_title))

measure_type = cell.shift(2,2).expand(RIGHT).is_not_blank() - cell.shift(4,2).expand(RIGHT)
trace.Measure_type('Measure type given at cell range: {}', var = excelRange(measure_type))

#attributes
total_employment = cell.shift(4,3).expand(DOWN).is_not_blank()
trace.Total_in_employment('Total in employment given at cell range: {}', var = excelRange(total_employment))

median_hourly_pay = cell.shift(5,3).expand(DOWN).is_not_blank()
trace.Median_hourly_pay('Median hourly pay (£) given at cell range: {}', var = excelRange(median_hourly_pay))

workforce_female = cell.shift(6,3).expand(DOWN).is_not_blank()
trace.Percentage_of_the_workforce_that_are_female('Percentage of the workforce that are female given at cell range: {}', var = excelRange(workforce_female))

workforce_55_plus = cell.shift(7,3).expand(DOWN).is_not_blank()
trace.Percentage_of_the_workforce_that_are_aged_55_plus('Percentage of the workforce that are aged 55+ given at cell range: {}', var = excelRange(workforce_55_plus))

workforce_bame = cell.shift(8,3).expand(DOWN).is_not_blank()
trace.Percentage_of_the_workforce_that_are_BAME('Percentage of the workforce that are BAME given at cell range: {}', var = excelRange(workforce_bame))

unit = 'standardised to a scale'
trace.Unit('Hardcoded as : standardised to a scale')
trace.Unit("Information regarding The standardised exposure to disease / infections measure found here: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11 ")

observations = measure_type.fill(DOWN).is_not_blank()

dimensions = [
    HDim(soc_codes, 'UK SOC 2010 Code', DIRECTLY, LEFT),
    HDim(occupation_title, 'Occupation title', DIRECTLY, LEFT),
    HDim(measure_type, 'Measure type', DIRECTLY, ABOVE),
    HDim(total_employment, 'Total in employment', DIRECTLY, RIGHT),
    HDim(median_hourly_pay, 'Median hourly pay (£)', DIRECTLY, RIGHT),
    HDim(workforce_female, 'Percentage of the workforce that are female', DIRECTLY, RIGHT),
    HDim(workforce_55_plus, 'Percentage of the workforce that are aged 55+', DIRECTLY, RIGHT),
    HDim(workforce_bame, 'Percentage of the workforce that are BAME', DIRECTLY, RIGHT),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet) 
trace.store("combined_dataframe", tidy_sheet.topandas())

df = trace.combine_and_trace(datacube_name, "combined_dataframe")
trace.add_column("Value")
trace.multi([ "Value"], "Rename databaker columns OBS to Value")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

tidy = df[['UK SOC 2010 Code', 'Occupation title', 'Total in employment', 'Median hourly pay (£)', 'Percentage of the workforce that are female', 'Percentage of the workforce that are aged 55+', 'Percentage of the workforce that are BAME', 'Measure type', 'Unit', 'Value']]


# Notes taken from Tables / https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11

notes = """
Some occupations are excluded due to no exposure and/or proximity measures being available
Please note the exposure to disease and proximity to others data was calculated by O*NET prior to the coronavirus (COVID-19) outbreak, therefore will not reflect any changes to working practices implemented since the outbreak.
The BAME group includes: Mixed/Multiple ethnic groups; Indian; Pakistani; Bangladeshi; Chinese; any other Asian background; Black/African/Caribbean/Black British
This measure of pay comes from the Annual Survey of Hours and Earnings (ASHE). It is hourly earnings excluding overtime. It's calculated as (gross pay excluding overtime/basic paid hours). The pay period in question was not affected by absence. It includes people aged 16+ both full-time and part-time.
For the percentage of women in each occupation, figures have been grouped together for percentages greater than 95% for disclosure reasons

The standardised exposure to disease or infections measure is defined by:
0 – Never
25 – Once a year or more but not every month
50 – Once a month or more but not every week
75 – Once a week or more but not every day
100 – Every day
please follow link for more information. 
https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11

"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
scrape.dataset.comment = notes
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)
scrape.dataset.family = 'covid-19'

trace.output()
tidy

# -

# #### Sheet : Total workforce data

# +
tab = tabs['Total_workforce_population']
datacube_name = "Which occupations have the highest potential exposure to the coronavirus (COVID-19)?"
columns=['Occupation title', 'Workforce category',  'Unit', 'Measure type']
trace.start(datacube_name, tab, columns, scrape.distributions[0].downloadURL)

cell = tab.filter(contains_string('Total workforce population'))
cell.assert_one()

occupation_title = cell
trace.Occupation_title('Occupation title given at cell range: {}', var = excelRange(occupation_title))

workforce_cat = cell.shift(1,-1).expand(RIGHT).is_not_blank()
trace.Workforce_category('Workforce category given at cell range: {}', var = excelRange(workforce_cat))

unit = 'Percent'
trace.Unit('Hardcoded as : Percent')
measure_type = 'Percentage'
trace.Unit('Hardcoded as : Percentage')

observations = workforce_cat.fill(DOWN).is_not_blank()
dimensions = [
    HDim(occupation_title, 'Occupation title', DIRECTLY, LEFT),
    HDim(workforce_cat, 'Workforce category', DIRECTLY, ABOVE),
    HDimConst('Measure type', measure_type),
    HDimConst('Unit', unit),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet) 
trace.store("combined_dataframe_2", tidy_sheet.topandas())

df = trace.combine_and_trace(datacube_name, "combined_dataframe_2")
trace.add_column("Value")
trace.multi([ "Value"], "Rename databaker columns OBS to Value")
df.rename(columns={'OBS' : 'Value'}, inplace=True)

tidy = df[['Occupation title', 'Workforce category', 'Measure type', 'Unit', 'Value']]


# +
out = Path('out')
out.mkdir(exist_ok=True)
scrape.dataset.comment = notes
tidy.drop_duplicates().to_csv(out / 'observations_1.csv', index = False)
scrape.dataset.family = 'covid-19'

trace.output()
tidy

# -




