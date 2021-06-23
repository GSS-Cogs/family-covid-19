# -*- coding: utf-8 -*-
# # ONS-Deaths-involving-COVID-19-UK

# +
import pandas as pd
from gssutils import *
import json
import string
import numpy as np
from dateutil.parser import parse

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

scraper = Scraper(seed='info.json')
scraper

trace = TransformTrace()
cubes = Cubes('info.json')

dist = scraper.distribution(latest=True, mediaType=Excel)
datasetTitle = info['title']
dist
datasetTitle

tabs_name = ['Table 1', 'Table 2', 'Table 3', 'Table 4']
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


# Transform process
for tab in tabs:
    print(tab.name)
    if tab.name == 'Table 1':
        columns = ['Period', 'Country', 'Persons', 'Males', 'Females', 'Measurement', 'Rate', 'Lower 95 Percent CI',
                   'Upper 95 Percent CI', 'Percentage of all deaths', 'Difference between 2020 and average',
                   'Percentage difference', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        period = '2020-03-01T00:00:00/P2M'
        trace.Period('Hardcoded as {}', var=period)

        country = tab.excel_ref('A7:A25').is_not_blank()
        trace.Country('Defined from cell range: {}', var=excelRange(country))

        persons = tab.filter('Persons').is_not_blank()
        trace.Persons('Defined from cell value: {}', var=cellLoc(persons))

        males = tab.filter('Males').is_not_blank()
        trace.Males('Defined from cell value: {}', var=cellLoc(males))

        females = tab.filter('Females').is_not_blank()
        trace.Females('Defined from cell value: {}', var=cellLoc(females))

        measurement = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
        trace.Measurement('Defined from cell range: {}', var=excelRange(measurement))

        rate = tab.filter('Rate').expand(DOWN).is_not_blank()
        trace.Rate('Defined from cell range: {}', var=excelRange(rate))

        percentage_all_deaths = tab.filter('Percentage of all deaths').expand(DOWN).is_not_blank()
        trace.Percentage_of_all_deaths('Defined from cell range: {}', var=excelRange(percentage_all_deaths))

        lower_95_percent_ci = tab.filter('Lower 95% CI').expand(DOWN).is_not_blank()
        trace.Lower_95_Percent_CI('Defined from cell range: {}', var=excelRange(lower_95_percent_ci))

        upper_95_percent_ci = tab.filter('Upper 95% CI').expand(DOWN).is_not_blank()
        trace.Upper_95_Percent_CI('Defined from cell range: {}', var=excelRange(upper_95_percent_ci))

        percentage_all_deaths = tab.filter('Percentage of all deaths').expand(DOWN).is_not_blank()
        trace.Percentage_of_all_deaths('Defined from cell range: {}', var=excelRange(percentage_all_deaths))

        difference_2020_and_average = tab.filter('Difference between 2020 and average').expand(DOWN).is_not_blank()
        trace.Difference_between_2020_and_average('Defined from cell range: {}',
                                                  var=excelRange(difference_2020_and_average))

        percentage_difference = tab.filter('Percentage difference').expand(DOWN).is_not_blank()
        trace.Percentage_difference('Defined from cell range: {}', var=excelRange(percentage_difference))

        measure_type = measurement
        trace.Measure_Type('Defined from cell range: {}', var=excelRange(measure_type))

        unit = 'Number of deaths'
        trace.Unit('Hardcoded as {}', var=unit)

        observations = tab.filter('Number of deaths').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(country, 'Country', DIRECTLY, LEFT),
            HDim(persons, 'Persons', CLOSEST, ABOVE),
            HDim(males, 'Males', CLOSEST, ABOVE),
            HDim(females, 'Females', CLOSEST, ABOVE),
            HDim(measurement, 'Measurement', DIRECTLY, ABOVE),
            HDim(rate, 'Rate', DIRECTLY, RIGHT),
            HDim(lower_95_percent_ci, 'Lower 95 Percent CI', DIRECTLY, RIGHT),
            HDim(upper_95_percent_ci, 'Upper 95 Percent CI', DIRECTLY, RIGHT),
            HDim(percentage_all_deaths, 'Percentage of all deaths', DIRECTLY, RIGHT),
            HDim(difference_2020_and_average, 'Difference between 2020 and average', DIRECTLY, RIGHT),
            HDim(percentage_difference, 'Percentage difference', DIRECTLY, RIGHT),
            HDim(measure_type, 'Measure Type', DIRECTLY, ABOVE),
            HDimConst('Unit', unit),
            HDimConst('Period', period)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_1', tidy_sheet.topandas())
    if tab.name == 'Table 2':
        columns = ['Period', 'Age', 'Country', 'Persons', 'Males', 'Females', 'Measurement', 'Rate',
                   'Lower 95 Percent CI', 'Upper 95 Percent CI', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        period = '2020-03-01T00:00:00/P2M'
        trace.Period('Hardcoded as {}', var=period)

        age = tab.excel_ref('A7:A67').is_not_blank()
        trace.Age('Defined from cell range: {}', var=excelRange(age))

        country = 'United Kingdom'
        trace.Country('Hardcoded as {}', var=country)

        persons = tab.filter('Persons').is_not_blank()
        trace.Persons('Defined from cell value: {}', var=cellLoc(persons))

        males = tab.filter('Males').is_not_blank()
        trace.Males('Defined from cell value: {}', var=cellLoc(males))

        females = tab.filter('Females').is_not_blank()
        trace.Females('Defined from cell value: {}', var=cellLoc(females))

        measurement = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
        trace.Measurement('Defined from cell range: {}', var=excelRange(measurement))

        rate = tab.filter('Rate').expand(DOWN).is_not_blank()
        trace.Rate('Defined from cell range: {}', var=excelRange(rate))

        lower_95_percent_ci = tab.filter('Lower 95% CI').expand(DOWN).is_not_blank()
        trace.Lower_95_Percent_CI('Defined from cell range: {}', var=excelRange(lower_95_percent_ci))

        upper_95_percent_ci = tab.filter('Upper 95% CI').expand(DOWN).is_not_blank()
        trace.Upper_95_Percent_CI('Defined from cell range: {}', var=excelRange(upper_95_percent_ci))

        measure_type = measurement
        trace.Measure_Type('Defined from cell range: {}', var=excelRange(measure_type))

        unit = 'Number of deaths'
        trace.Unit('Hardcoded as {}', var=unit)

        observations = tab.filter('Number of deaths').expand(DOWN).is_not_blank()

        dimensions = [
            HDim(age, 'Age', DIRECTLY, LEFT),
            HDim(persons, 'Persons', CLOSEST, ABOVE),
            HDim(males, 'Males', CLOSEST, ABOVE),
            HDim(females, 'Females', CLOSEST, ABOVE),
            HDim(measurement, 'Measurement', DIRECTLY, ABOVE),
            HDim(rate, 'Rate', DIRECTLY, RIGHT),
            HDim(lower_95_percent_ci, 'Lower 95 Percent CI', DIRECTLY, RIGHT),
            HDim(upper_95_percent_ci, 'Upper 95 Percent CI', DIRECTLY, RIGHT),
            HDim(measure_type, 'Measure Type', DIRECTLY, ABOVE),
            HDimConst('Unit', unit),
            HDimConst('Period', period),
            HDimConst('Country', country)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_2', tidy_sheet.topandas())
    if tab.name == 'Table 3':
        columns = ['Period', 'Country', 'Measure Type', 'Unit']
        trace.start(datasetTitle, tab, columns, dist.downloadURL)

        period = tab.excel_ref('A5:A65').is_not_blank()
        trace.Period('Defined from cell range: {}', var=excelRange(period))

        country = 'United Kingdom'
        trace.Country('Hardcoded as {}', var=country)

        measure_type = tab.filter('All Deaths').expand(RIGHT).is_not_blank()
        trace.Measure_Type('Defined from cell range: {}', var=excelRange(measure_type))

        unit = 'Number of deaths'
        trace.Unit('Hardcoded as {}', var=unit)

        observations = tab.excel_ref('B5').expand(RIGHT).expand(DOWN).is_not_blank()

        dimensions = [
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(measure_type, 'Measure Type', DIRECTLY, ABOVE),
            HDimConst('Unit', unit),
            HDimConst('Country', country)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        savepreviewhtml(tidy_sheet, fname=f'{tab.name}_Preview.html')
        trace.store(f'combined_dataframe_table_3', tidy_sheet.topandas())

country_geocode_dict={'United Kingdom': 'K02000001', 'England':'E92000001', 'Wales':'W92000004', 'Northern Ireland':'N92000002', 'Scotland':'S92000003'}

df_tbl_1 = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_1')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_1.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)

df_tbl_1_marker_idx = df_tbl_1[df_tbl_1['Marker'].isin(['Number of deaths'])].index
df_tbl_1.drop(df_tbl_1_marker_idx , inplace=True)

df_tbl_1.loc[df_tbl_1['Measurement'].isin(['All deaths', '5-year average']), 'Percentage of all deaths'] = None
df_tbl_1.loc[df_tbl_1['Measurement'].isin(['All deaths', 'Deaths involving COVID-19']), 'Difference between 2020 and average'] = None
df_tbl_1.loc[df_tbl_1['Measurement'].isin(['All deaths', 'Deaths involving COVID-19']), 'Percentage difference'] = None

df_tbl_1['Percentage of all deaths'] = pd.to_numeric(df_tbl_1['Percentage of all deaths'], errors='coerce').astype('float64').replace(np.nan, 'None')
df_tbl_1['Difference between 2020 and average'] = pd.to_numeric(df_tbl_1['Difference between 2020 and average'], errors='coerce').astype('float64').replace(np.nan, 'None')
df_tbl_1['Percentage difference'] = pd.to_numeric(df_tbl_1['Percentage difference'], errors='coerce').astype('float64').replace(np.nan, 'None')

df_tbl_1.loc[(df_tbl_1['Persons'] == 'Persons'), 'Gender'] = 'All'
df_tbl_1.loc[(df_tbl_1['Males'] == 'Males'), 'Gender'] = 'Male'
df_tbl_1.loc[(df_tbl_1['Females'] == 'Females'), 'Gender'] = 'Female'

df_tbl_1['Country Geocode'] = df_tbl_1['Country'].replace(country_geocode_dict)
trace.add_column('Country Geocode')
trace.Country_Code("Create Country Geocode Value based on 'Country' column")

df_tbl_1['Marker'] = None

df_tbl_1 = df_tbl_1[['Period', 'Country', 'Country Geocode', 'Gender', 'Measurement', 'Rate', 'Lower 95 Percent CI', 'Upper 95 Percent CI', 'Percentage of all deaths', 'Difference between 2020 and average', 'Percentage difference', 'Measure Type', 'Unit', 'Marker', 'Value']]

df_tbl_2 = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_2')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_2.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)

df_tbl_2 = df_tbl_2.replace({'Rate': {':': 'None'}, 'Lower 95 Percent CI': {':': 'None'}, 'Upper 95 Percent CI': {':': 'None'}})

df_tbl_2_marker_idx = df_tbl_2[df_tbl_2['Marker'].isin(['Number of deaths'])].index
df_tbl_2.drop(df_tbl_2_marker_idx , inplace=True)

df_tbl_2.loc[(df_tbl_2['Persons'] == 'Persons'), 'Gender'] = 'All'
df_tbl_2.loc[(df_tbl_2['Males'] == 'Males'), 'Gender'] = 'Male'
df_tbl_2.loc[(df_tbl_2['Females'] == 'Females'), 'Gender'] = 'Female'

df_tbl_2['Country Geocode'] = df_tbl_2['Country'].replace(country_geocode_dict)
trace.add_column('Country Geocode')
trace.Country_Geocode("Create Country Geocode Value based on 'Country' column")

df_tbl_2['Marker'] = None

df_tbl_2 = df_tbl_2[['Period', 'Age', 'Country', 'Country Geocode', 'Gender', 'Measurement', 'Rate', 'Lower 95 Percent CI', 'Upper 95 Percent CI', 'Measure Type', 'Unit', 'Marker', 'Value']]

df_tbl_3 = trace.combine_and_trace(datasetTitle, 'combined_dataframe_table_3')
trace.add_column('Value')
trace.Value('Rename databaker column OBS to Value')
df_tbl_3.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)

df_tbl_3['Period'] = df_tbl_3['Period'].apply(lambda x: parse(str(x)).strftime('%Y-%m-%dT%H:%M:%S'))
trace.Period("Format 'Period' column with gregorian day format")

df_tbl_3['Country Geocode'] = df_tbl_3['Country'].replace(country_geocode_dict)
trace.add_column('Country Geocode')
trace.Country_Geocode("Create Country Geocode Value based on 'Country' column")

df_tbl_3['Value'] = pd.to_numeric(df_tbl_3['Value'], errors='coerce').astype('Int64')

df_tbl_3['Marker'] = None

df_tbl_3 = df_tbl_3[['Period', 'Country', 'Country Geocode', 'Measure Type', 'Unit', 'Marker', 'Value']]

# Notes from tab
notes = """
Table 1
1. Based on bounderies as of Feb 2020
2. Based on the date a death occurred rather than when a death was registered. Includes deaths registered by 15th May
3. Excludes deaths of non-residents with the exception on Northern Ireland data
4. Data for 2020 is provisional
5. COVID-19 defined as ICD10 codes U07.1 and U07.2
6. Age-standardised mortality rates per 100,000 population, standardised to the 2013 European Standard Population. Age-standardised rates are used to allow comparison between populations which may contain different proportions of people of different ages.
7. The lower and upper confidence limits have been provided. These form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the estimated figure. Calculations based on small numbers of events are often subject to random fluctuations. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
8. Figures for deaths involving COVID-19 show the number of deaths involving coronavirus (COVID-19), based on any mention of COVID-19 on the death certificate.
Table 2
1. Based on bounderies as of Feb 2020
2. Based on the date a death occurred rather than when a death was registered. Includes deaths registered by 15th May
3. Excludes deaths of non-residents with the exception on Northern Ireland data
4. Data for 2020 is provisional
5. COVID-19 defined as ICD10 codes U07.1 and U07.2
6. Rates are not available where there are less than 3 deaths
7. Age-specific rates where there were fewer than 10 deaths are unreliable and denoted with a u to indicate that rates are based on small numbers
8. Age-specific mortality rates per 100,000 population.
9. The lower and upper confidence limits have been provided. These form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the estimated figure. Calculations based on small numbers of events are often subject to random fluctuations. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
10. Figures for deaths involving COVID-19 show the number of deaths involving coronavirus (COVID-19), based on any mention of COVID-19 on the death certificate.
Table 3
1. Based on bounderies as of Feb 2020
2. Based on the date a death occurred rather than when a death was registered. Includes deaths registered by 15th May
3. Excludes deaths of non-residents with the exception on Northern Ireland data
4. Data for 2020 is provisional
5. COVID-19 defined as ICD10 codes U07.1 and U07.2
6. Figures for deaths involving COVID-19 show the number of deaths involving coronavirus (COVID-19), based on any mention of COVID-19 on the death certificate.
"""
scraper.dataset.comment = notes
scraper.dataset.family = 'covid-19'
