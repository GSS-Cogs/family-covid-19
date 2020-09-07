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

unit = 'Standardised Scale'
trace.Unit('Hardcoded as : standardised to a scale')
trace.Unit("Information regarding The standardised exposure to disease / infections measure found here: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11 ")

observations = measure_type.fill(DOWN).is_not_blank()

dimensions = [
    HDim(soc_codes, 'UK SOC 2010 Code', DIRECTLY, LEFT),
    HDim(occupation_title, 'Occupation', DIRECTLY, LEFT),
    HDim(measure_type, 'Measure type', DIRECTLY, ABOVE),
    HDim(measure_type, 'Working Condition Category', DIRECTLY, ABOVE),
    HDim(total_employment, 'Total in employment', DIRECTLY, RIGHT),
    HDim(median_hourly_pay, 'Median hourly pay', DIRECTLY, RIGHT),
    HDim(workforce_female, 'Percentage Workforce Female', DIRECTLY, RIGHT),
    HDim(workforce_55_plus, 'Percentage Workforce Aged 55plus', DIRECTLY, RIGHT),
    HDim(workforce_bame, 'Percentage Workforce BAME', DIRECTLY, RIGHT),
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
df["UK SOC 2010 Code"] = pd.to_numeric(df["UK SOC 2010 Code"])
df["UK SOC 2010 Code"] = df["UK SOC 2010 Code"].astype(int)
df = df.replace({'Measure type' : {'Proximity to others' : 'Proximity', 'Exposure to disease' : 'Exposure'}})
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

# +
tidy = df[['UK SOC 2010 Code', 'Occupation','Total in employment', 'Median hourly pay', 'Percentage Workforce Female', 'Percentage Workforce Aged 55plus', 'Percentage Workforce BAME', 'Working Condition Category', 'Measure type', 'Unit', 'Value']]

trace.Occupation_title("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Occupation', 'Working Condition Category'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))


# -


# ________________________________________________________________________
# REMOVING OBS WITH MEASURETYPE "PROXIMITY TO OTHERS" FOR NOW DUE TO NOT CURRENTLY BEING ABLE TO HANDEL MULTPLE MEASURE TYPES. WILL NEED TO BE ADDED BACK IN. 
# _________________________________________________________________________

df.drop(df[df['Measure type'] == 'Proximity'].index, inplace=True)


# _______________________________________________________________________________________________________________

#Removing columns as they are defined in info.json 
del tidy['Measure type']
del tidy['Unit']

notes = """Some occupations are excluded due to no exposure and/or proximity measures being available
Please note the exposure to disease and proximity to others data was calculated by O*NET prior to the coronavirus (COVID-19) outbreak, therefore will not reflect any changes to working practices implemented since the outbreak.
The BAME group includes: Mixed/Multiple ethnic groups; Indian; Pakistani; Bangladeshi; Chinese; any other Asian background; Black/African/Caribbean/Black British
This measure of pay comes from the Annual Survey of Hours and Earnings (ASHE). It is hourly earnings excluding overtime. It's calculated as (gross pay excluding overtime/basic paid hours). The pay period in question was not affected by absence. It includes people aged 16+ both full-time and part-time.
For the percentage of women in each occupation, figures have been grouped together for percentages greater than 95% for disclosure reasons

please follow link for more information on how The standardised exposure to disease or infections measure is defined:
https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11
"""

# +
#SET UP OUTPUT FOLDER AND OUTPUT DATA TO CSV
csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / csvName, index = False)
scrape.dataset.family = 'covid-19'
scrape.dataset.description = scrape.dataset.description + '\n ' + notes
scrape.dataset.comment = 'ONS has created an estimate of exposure to generic disease, and physical proximity to others, for UK occupations based on US analysis of these factors.'

# CREATE MAPPING CLASS INSTANCE, SET UP VARIABLES AND WRITE FILES
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')


# -
# CREATE AND OUTPUT TRIG FILE
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())

trace.output()
#tidy

# +
#info = json.load(open('info.json')) 
#codelistcreation = info['transform']['codelists'] 
#print(codelistcreation)
#print("-------------------------------------------------------")

#codeclass = CSVCodelists()
#for cl in codelistcreation:
#    if cl in tidy.columns:
#        tidy[cl] = tidy[cl].str.replace("-"," ")
#        tidy[cl] = tidy[cl].str.capitalize()
#        codeclass.create_codelists(pd.DataFrame(tidy[cl]), 'codelists', 'covid-19', Path(os.getcwd()).name.lower())
# -




# Notes taken from Tables / https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11



# #### Sheet : Total workforce data
#
# COMMENTED OUT FOR NOW, ONLY 3 OBSERVATIONS AND THEY ARE DERRIABLE FROM SHEET ABOVE 

# tab = tabs['Total_workforce_population']
# datacube_name = "Which occupations have the highest potential exposure to the coronavirus (COVID-19)?"
# columns=['Occupation title', 'Workforce category',  'Unit', 'Measure type']
# trace.start(datacube_name, tab, columns, scrape.distributions[0].downloadURL)
#
# cell = tab.filter(contains_string('Total workforce population'))
# cell.assert_one()
#
# workforce_cat = cell.shift(1,-1).expand(RIGHT).is_not_blank()
# trace.Workforce_category('Workforce category given at cell range: {}', var = excelRange(workforce_cat))
#
# unit = 'Percent'
# trace.Unit('Hardcoded as : Percent')
# measure_type = 'Percentage'
# trace.Unit('Hardcoded as : Percentage')
#
# observations = workforce_cat.fill(DOWN).is_not_blank()
# dimensions = [
#     HDim(workforce_cat, 'Workforce Category', DIRECTLY, ABOVE),
#     HDimConst('Measure type', measure_type),
#     HDimConst('Unit', unit),
# ]
# tidy_sheet = ConversionSegment(tab, dimensions, observations)
# trace.with_preview(tidy_sheet)
# #savepreviewhtml(tidy_sheet) 
# trace.store("combined_dataframe_2", tidy_sheet.topandas())
#
# df = trace.combine_and_trace(datacube_name, "combined_dataframe_2")
# trace.add_column("Value")
# trace.multi([ "Value"], "Rename databaker columns OBS to Value")
# df.rename(columns={'OBS' : 'Value'}, inplace=True)
# df = df.replace({'Workforce Category' : {'Percentage of the workforce that are female(%)' : 'Females', 
#                                    'Percentage of the workforce that are BAME (%)' : 'BAME',
#                                    'Percentage of the workforce that are aged 55+ (%)': 'Aged 55plus'}})
#
#
# tidy = df[['Workforce Category', 'Measure type', 'Unit', 'Value']]






