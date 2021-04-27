# -*- coding: utf-8 -*-
# # NE-The-People-and-Nature-Survey-for-England

# +
import pandas as pd
from gssutils import *
import json
import datetime
import string
import re

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

scraper = Scraper(seed='info.json')
scraper

trace = TransformTrace()
cubes = Cubes('info.json')

dist = scraper.distribution(mediaType=ODS)
xls = pd.ExcelFile(dist.downloadURL, engine='odf')
with pd.ExcelWriter('data.xls') as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet, index = False)
    writer.save()
tabs = loadxlstabs('data.xls')

datasetTitle = info['title']
tabs_name = ['Q1', 'Q2', 'Q4b', 'Q4e', 'Q6', 'Q34b', 'Q49a', 'Q49b', 'Q59a']
columns=['Question', 'Response', 'Type', 'Measure Type', 'Unit', 'Period', 'Base', 'Unweighted base size']

if len(set(tabs_name)-{x.name for x in tabs}) != 0:
    raise ValueError(f'Aborting. A tab named {set(tabs_name)-{x.name for x in tabs}} required but not found')

tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset+amount]


def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]


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


def format_date(date_value):
    date_string = datetime.datetime.strptime(date_value, '%B %Y').strftime('%Y-%m')
    return date_string


# Transform process
for tab in tabs:
    trace.start(datasetTitle, tab, columns, dist.downloadURL)
    print(tab.name)

    question = tab.excel_ref('A1')
    trace.Question('Defined from cell value: {}', var=cellLoc(question))

    response = tab.excel_ref('A4').expand(DOWN).is_not_blank()
    trace.Response('Defined from cell range: {}', var = excelRange(response))

    value_type = tab.excel_ref('B2').expand(RIGHT).is_not_blank()
    trace.Type('Defined from cell range: {}', var = excelRange(value_type))

    measure_type = 'Percentage'
    trace.Measure_Type('Hardcoded as Percentage')

    unit = 'Percent'
    trace.Unit('Hardcoded as Percent')

    period = tab.excel_ref('B1')
    trace.Period('Defined from cell value: {}', var=cellLoc(period))

    base = tab.excel_ref('A2')
    trace.Base('Defined from cell value: {}', var=cellLoc(base))

    unweighted_base_size = tab.excel_ref('B3')
    trace.Unweighted_base_size('Defined from cell value: {}', var=cellLoc(unweighted_base_size))

    observations = tab.excel_ref('B4').expand(DOWN).expand(RIGHT).is_not_blank()

    dimensions = [
        HDim(question, 'Question', CLOSEST, ABOVE),
        HDim(response, 'Response', DIRECTLY, LEFT),
        HDim(value_type, 'Type', DIRECTLY, ABOVE),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit),
        HDim(period, 'Period', CLOSEST, ABOVE),
        HDim(base, 'Base', CLOSEST, ABOVE),
        HDim(unweighted_base_size, 'Unweighted base size', CLOSEST, ABOVE)
    ]

    tidy_sheet = ConversionSegment(tab, dimensions, observations)
    trace.with_preview(tidy_sheet)
    savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
    trace.store('combined_dataframe', tidy_sheet.topandas())

df = trace.combine_and_trace(datasetTitle, 'combined_dataframe')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)
df = df.replace({'Value': {'' : '0'}})
df['Value'] = pd.Series(['{0:.2%}'.format(val) for val in df['Value']], index = df.index)
df['Period'] = df['Period'].apply(format_date)
df['Unweighted base size'] = pd.to_numeric(df['Unweighted base size'], errors='coerce').astype(int)

df = df[['Question', 'Response', 'Value', 'Type', 'Measure Type', 'Unit', 'Period', 'Base',
         'Unweighted base size']]

for col in df.columns:
    if col not in ['Value', 'Type']:
        df[col] = df[col].apply(lambda x: pathify(str(x)))

cubes.add_cube(scraper, df, datasetTitle)

cubes.output_all()

trace.render('spec_v1.html')
