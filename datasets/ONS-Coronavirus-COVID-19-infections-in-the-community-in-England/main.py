# -*- coding: utf-8 -*-
# # ONS-Coronavirus-COVID-19-infections-in-the-community-in-England

# +
import pandas as pd
from gssutils import *
import json
import string
from datefinder import find_dates
import numpy as np

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

scraper = Scraper(seed='info.json')
scraper

trace = TransformTrace()
cubes = Cubes('info.json')

dist = scraper.distribution(latest = True, mediaType = Excel)
datasetTitle = info['title']
dist
datasetTitle

tabs_name = ['1a', '1b', '2a', '2b', '2c', '2d']
tabs = {tab: tab for tab in dist.as_databaker() if tab.name in tabs_name}
if len(set(tabs_name)-{x.name for x in tabs}) != 0:
    raise ValueError(f'Aborting. A tab named {set(tabs_name)-{x.name for x in tabs}} required but not found')


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


def format_date(date_str):
    date_str = date_str.replace('between', '')
    date_results = list(find_dates(date_str))
    from_date = date_results[0].strftime('%Y-%m-%dT%H:%M:%S')
    to_date = date_results[1].strftime('%Y-%m-%dT%H:%M:%S')
    return from_date + '-' + to_date


def pathify_columns(df, columns_arr):
    for col in df.columns:
        if col in columns_arr:
            try:
                df[col] = df[col].apply(lambda x: pathify(str(x)))
            except Exception as err:
                raise Exception('Failed to pathify column "{}".'.format(col)) from err


def convert_category_datatype(df, columns_arr):
    for col in df.columns:
        if col in columns_arr:
            try:
                df[col] = df[col].astype('category')
            except ValueError as err:
                raise ValueError('Failed to convert category data type for column "{}".'.format(col)) from err


def convert_column_type_numeric(df, column_arr, datatype):
    for col in df.columns:
        if col in column_arr:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(datatype).replace(np.nan, 'None')
            except ValueError as err:
                raise ValueError('Failed to convert column datatype "{}".'.format(col)) from err


# Transform process
for tab in tabs:
    print(tab.name)
    if tab.name == '1a':
        columns = ['Title', 'Total Survey Period', 'Measurement', 'Period', 'Measure Type', 'Unit', 'Social Distance Ability At Work', 'Lower Bound of 95 Percent Confidence Interval',
                   'Upper Bound of 95 Percent Confidence Interval', 'Number of people testing positive in sample', 'Total Number of People in sample']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        total_survey_period = tab.excel_ref('A4')
        trace.Total_Survey_Period('Defined from cell value: {}', var=cellLoc(total_survey_period))

        measurement = tab.excel_ref('A6')
        trace.Measurement('Defined from cell value: {}', var=cellLoc(measurement))

        period = tab.excel_ref('A10').expand(DOWN).is_not_blank() & tab.excel_ref('A16').expand(UP).is_not_blank()
        trace.Period('Defined from cell range: {}', var=excelRange(period))

        social_distance_ability = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
        trace.Social_Distance_Ability_At_Work('Defined from cell range: {}', var=excelRange(social_distance_ability))

        lower_bound_confidence_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.Lower_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}', var=excelRange(lower_bound_confidence_interval))

        upper_bound_confidence_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.Upper_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}', var=excelRange(upper_bound_confidence_interval))

        positive_sample_count = tab.filter('Number of people testing positive').expand(DOWN).is_not_blank()
        trace.Number_of_people_testing_positive_in_sample('Defined from cell range: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people in sample').expand(DOWN).is_not_blank()
        trace.Total_Number_of_People_in_sample('Defined from cell range: {}', var=excelRange(total_sample_count))

        measure_type = tab.excel_ref('A3')
        trace.Measure_Type('Defined from cell value: {}', var=cellLoc(measure_type))

        unit = 'Odds Ratio'
        trace.Unit('Hardcoded as Odds Ratio')

        observations = tab.filter('Odds Ratio').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(total_survey_period, 'Total Survey Period', CLOSEST, ABOVE),
            HDim(measurement, 'Measurement', CLOSEST, ABOVE),
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(social_distance_ability, 'Social Distance Ability At Work', DIRECTLY, ABOVE),
            HDim(lower_bound_confidence_interval, 'Lower Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(upper_bound_confidence_interval, 'Upper Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(positive_sample_count, 'Number of people testing positive in sample', DIRECTLY, RIGHT),
            HDim(total_sample_count, 'Total Number of People in sample', DIRECTLY, RIGHT),
            HDim(measure_type, 'Measure Type', CLOSEST, ABOVE),
            HDimConst('Unit', unit)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'Table_{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_{tab.name}', tidy_sheet.topandas())

    if tab.name == '1b':
        columns = ['Title', 'Total Survey Period', 'Measurement', 'Period', 'Measure Type', 'Unit', 'Mode of Travel to Work', 'Lower Bound of 95 Percent Confidence Interval',
                   'Upper Bound of 95 Percent Confidence Interval', 'Number of people testing positive in sample', 'Total Number of People in sample']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        total_survey_period = tab.excel_ref('A4')
        trace.Total_Survey_Period('Defined from cell value: {}', var=cellLoc(total_survey_period))

        measurement = tab.excel_ref('A6')
        trace.Measurement('Defined from cell value: {}', var=cellLoc(measurement))

        period = tab.excel_ref('A10').expand(DOWN).is_not_blank() & tab.excel_ref('A16').expand(UP).is_not_blank()
        trace.Period('Defined from cell range: {}', var=excelRange(period))

        mode_travel_to_work = tab.excel_ref('B7').expand(RIGHT).is_not_blank()
        trace.Mode_of_Travel_to_Work('Defined from cell range: {}', var=excelRange(mode_travel_to_work))

        lower_bound_confidence_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.Lower_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}', var=excelRange(lower_bound_confidence_interval))

        upper_bound_confidence_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.Upper_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}', var=excelRange(upper_bound_confidence_interval))

        positive_sample_count = tab.filter('Number of people testing positive').expand(DOWN).is_not_blank()
        trace.Number_of_people_testing_positive_in_sample('Defined from cell range: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people in sample').expand(DOWN).is_not_blank()
        trace.Total_Number_of_People_in_sample('Defined from cell range: {}', var=excelRange(total_sample_count))

        measure_type = tab.excel_ref('A3')
        trace.Measure_Type('Defined from cell value: {}', var=cellLoc(measure_type))

        unit = 'Odds Ratio'
        trace.Unit('Hardcoded as Odds Ratio')

        observations = tab.filter('Odds Ratio').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(total_survey_period, 'Total Survey Period', CLOSEST, ABOVE),
            HDim(measurement, 'Measurement', CLOSEST, ABOVE),
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(mode_travel_to_work, 'Mode of Travel to Work', DIRECTLY, ABOVE),
            HDim(lower_bound_confidence_interval, 'Lower Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(upper_bound_confidence_interval, 'Upper Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(positive_sample_count, 'Number of people testing positive in sample', DIRECTLY, RIGHT),
            HDim(total_sample_count, 'Total Number of People in sample', DIRECTLY, RIGHT),
            HDim(measure_type, 'Measure Type', CLOSEST, ABOVE),
            HDimConst('Unit', unit)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'Table_{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_{tab.name}', tidy_sheet.topandas())

    if tab.name in ['2a', '2b', '2c', '2d']:
        columns = ['Title', 'Period', 'Symptom', 'Measure Type', 'Unit', 'Lower Bound of 95 Percent Confidence Interval',
                   'Upper Bound of 95 Percent Confidence Interval', 'Positive Sample Count', 'Total Sample Count']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        title = tab.excel_ref('A3')
        trace.Title('Defined from cell value: {}', var=cellLoc(title))

        period = tab.excel_ref('A4')
        trace.Period('Defined from cell value: {}', var=cellLoc(period))

        symptom = tab.excel_ref('A7').expand(DOWN).is_not_blank() & tab.excel_ref('A23').expand(UP).is_not_blank()
        trace.Symptom('Defined from cell range: {}', var=excelRange(symptom))

        lower_bound_confidence_interval = tab.filter('Lower').expand(DOWN).is_not_blank()
        trace.Lower_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}',
                                                   var=excelRange(lower_bound_confidence_interval))

        upper_bound_confidence_interval = tab.filter('Upper').expand(DOWN).is_not_blank()
        trace.Upper_Bound_of_95_Percent_Confidence_Interval('Defined from cell range: {}',
                                                   var=excelRange(upper_bound_confidence_interval))

        positive_sample_count = tab.filter('Number of people testing positive with symptom').expand(DOWN).is_not_blank()
        trace.Positive_Sample_Count('Defined from cell range: {}', var=excelRange(positive_sample_count))

        total_sample_count = tab.filter('Total number of people testing positive').expand(DOWN).is_not_blank()
        trace.Total_Sample_Count('Defined from cell range: {}', var=excelRange(total_sample_count))

        measure_type = 'Percentage testing positive with symptom'
        trace.Measure_Type('Hardcoded as Percentage testing positive with symptom')

        unit = 'Percent'
        trace.Unit('Hardcoded as Percent')

        observations = tab.filter(contains_string('% testing positive with symptom')).expand(DOWN).is_not_blank()

        dimensions = [
            HDim(title, 'Title', CLOSEST, ABOVE),
            HDim(period, 'Period', CLOSEST, ABOVE),
            HDim(symptom, 'Symptom', DIRECTLY, LEFT),
            HDim(lower_bound_confidence_interval, 'Lower Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(upper_bound_confidence_interval, 'Upper Bound of 95 Percent Confidence Interval', DIRECTLY, RIGHT),
            HDim(positive_sample_count, 'Positive Sample Count', DIRECTLY, RIGHT),
            HDim(total_sample_count, 'Total Sample Count', DIRECTLY, RIGHT),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'Table_{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_2', tidy_sheet.topandas())

# Notes from tab
notes = """
Table 1a,1b
1. All results are provisional and subject to revision.
2. These statistics refer to infections reported in the community, by which we mean private households. These figures exclude infections reported in hospitals, care homes and/or other institutional settings.
3. The data in this table relate to those who have tested positive for COVID-19 on a nose and throat swab in the time periods specified.
4. This analysis is based on data from participants aged 16-74 who are currently working. 
5. Estimates were calculated using a logistic regression model which accounts for age, sex, region, urban/rural status, ethnicity, household size, multigenerational households, deprivation, whether individuals are currently working from home and their ability to socially distance at work if not working from home, method of travel to work and face coverings in the workplace. 													
4. Please see our methods article for more methodological information on the COVID-19 Infection Survey:
https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/methodologies/covid19infectionsurveypilotmethodsandfurtherinformation
Table 2a,2b,2c,2d
1. All results are provisional and subject to revision.
2. These statistics refer to infections reported in the community, by which we mean private households. These figures exclude infections reported in hospitals, care homes or other institutional settings.
3. Symptoms are self-reported and were not professionally diagnosed.
4. These data are unweighted percentages of people with any positive test result that had a Ct value less than 30.
"""
scraper.dataset.comment = notes
scraper.dataset.family = 'covid-19'

df_tbl_1a = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_1a')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_1a.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)
df_tbl_1a = df_tbl_1a.dropna(subset=['Period'], axis =0)

df_tbl_1b = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_1b')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_1b.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)
df_tbl_1b = df_tbl_1b.dropna(subset=['Period'], axis =0)

df_tbl_2 = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_2')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_2.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)
df_tbl_2 = df_tbl_2.dropna(subset=['Symptom'], axis =0)

df_tbl_2['Country Name'] = df_tbl_2['Title'].str.split(',').str[-1].apply(lambda x: x.strip())
trace.add_column('Country Name')
trace.Country_Name("Create Country Name Value based on 'Title' column")

country_code_dict={'England':'E92000001', 'Wales':'W92000004', 'Northern Ireland':'N92000002', 'Scotland':'S92000003'}
df_tbl_2['Country Code'] = df_tbl_2['Country Name'].replace(country_code_dict)
trace.add_column('Country Code')
trace.Country_Code("Create Country Code Value based on 'Country Name' column")

df_tbl_1a['Period'] = df_tbl_1a['Period'].apply(format_date)
df_tbl_1b['Period'] = df_tbl_1b['Period'].apply(format_date)
df_tbl_2['Period'] = df_tbl_2['Period'].apply(format_date)
df_tbl_1a['Total Survey Period'] = df_tbl_1a['Total Survey Period'].apply(format_date)
df_tbl_1b['Total Survey Period'] = df_tbl_1b['Total Survey Period'].apply(format_date)

convert_column_type_numeric(df_tbl_1a, ['Number of people testing positive in sample', 'Total Number of People in sample'], 'Int64')
convert_column_type_numeric(df_tbl_1b, ['Number of people testing positive in sample', 'Total Number of People in sample'], 'Int64')
convert_column_type_numeric(df_tbl_2, ['Positive Sample Count', 'Total Sample Count'], 'Int64')

convert_column_type_numeric(df_tbl_1a, ['Lower Bound of 95 Percent Confidence Interval', 'Upper Bound of 95 Percent Confidence Interval'], 'float64')
convert_column_type_numeric(df_tbl_1b, ['Lower Bound of 95 Percent Confidence Interval', 'Upper Bound of 95 Percent Confidence Interval'], 'float64')
convert_column_type_numeric(df_tbl_2, ['Lower Bound of 95 Percent Confidence Interval', 'Upper Bound of 95 Percent Confidence Interval'], 'float64')

convert_category_datatype(df_tbl_1a, ['Title', 'Measurement', 'Social Distance Ability At Work', 'Measure Type', 'Unit'])
convert_category_datatype(df_tbl_1b, ['Title', 'Measurement', 'Mode of Travel to Work', 'Measure Type', 'Unit'])
convert_category_datatype(df_tbl_2, ['Title', 'Country Name', 'Country Code', 'Symptom', 'Measure Type', 'Unit'])

pathify_columns(df_tbl_1a, ['Title', 'Measurement', 'Social Distance Ability At Work', 'Measure Type', 'Unit'])
pathify_columns(df_tbl_1b, ['Title', 'Measurement', 'Mode of Travel to Work', 'Measure Type', 'Unit'])
pathify_columns(df_tbl_2, ['Title', 'Country Name', 'Country Code', 'Symptom', 'Measure Type', 'Unit'])

df_tbl_1a = df_tbl_1a[['Title', 'Measurement', 'Total Survey Period', 'Social Distance Ability At Work', 'Period', 'Value', 'Measure Type', 'Unit',
                       'Lower Bound of 95 Percent Confidence Interval', 'Upper Bound of 95 Percent Confidence Interval', 'Number of people testing positive in sample', 'Total Number of People in sample']]
df_tbl_1b = df_tbl_1b[['Title', 'Measurement', 'Total Survey Period', 'Mode of Travel to Work', 'Period', 'Value', 'Measure Type', 'Unit',
                       'Lower Bound of 95 Percent Confidence Interval', 'Upper Bound of 95 Percent Confidence Interval', 'Number of people testing positive in sample', 'Total Number of People in sample']]
df_tbl_2 = df_tbl_2[['Title', 'Period', 'Country Name', 'Country Code', 'Symptom', 'Value', 'Measure Type', 'Unit', 'Lower Bound of 95 Percent Confidence Interval',
                     'Upper Bound of 95 Percent Confidence Interval', 'Positive Sample Count', 'Total Sample Count']]

cubes.add_cube(scraper, df_tbl_1a, datasetTitle+'-table-1a')
cubes.add_cube(scraper, df_tbl_1b, datasetTitle+'-table-1b')
cubes.add_cube(scraper, df_tbl_2, datasetTitle+'-table-2')

cubes.output_all()

trace.render('spec_v1.html')
