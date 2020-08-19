# # Deaths involving COVID-19 by local area and deprivation

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

month_look_up = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
                  'Jul':'07','Aug':'08','Sep':'09', 'Oct':'10','Nov':'11', 'Dec':'12'}

def date_time (date):
    if len(date)  > 10:
        #gregorian-interval/2020-01-03T00:00:00/P4M
        duration = left(date,1)
        return 'gregorian-interval/2020-01-03T00:00:00/P' + duration + 'M'
    else:
        month = month_look_up[left(date,3)]
        return 'gregorian-month/2020-' + month 

trace = TransformTrace()
df = pd.DataFrame()


# -

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
distribution = scraper.distributions[0]
#display(distribution)

tabs = { tab: tab for tab in distribution.as_databaker() }

# ________________________________________________________________________________________________________________
# Table 3
# ________________________________________________________________________________________________________________
#

datasetTitle = 'Deaths involving COVID-19 by local area and deprivation'
for tab in tabs:
    if tab.name in ['Table 3']:
        columns=["Period", "Cause of detah", "Sex", "Decile", "Country", "Rate", "Lower CI", "Upper CI", 'Marker', "Measure type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)

        cause_of_death = tab.filter(contains_string('Cause of death')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Footnotes')).expand(DOWN)
        trace.Cause_of_detah('Cause of death given at cell range: {}', var = excelRange(cause_of_death))
        
        sex = tab.filter(contains_string('Sex')).shift(0,1).expand(DOWN).is_not_blank() 
        trace.Sex('Sex given at cell range: {}', var = excelRange(sex))

        decile = tab.filter(contains_string('Decile')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Footnotes')).expand(DOWN)
        trace.Decile('Decile given at cell range: {}', var = excelRange(decile))

        country = "England"
        trace.Country("Country hardcoded as England")
        
        period = tab.filter(contains_string('March')).expand(RIGHT).is_not_blank()
        trace.Period('Period / Month given at cell range: {}', var = excelRange(period))

        rate = tab.filter(contains_string('Rate')).shift(0,1).expand(DOWN).is_not_blank() - tab.filter(contains_string('Footnotes')).expand(DOWN)
        trace.Rate('Rate given at cell range: {}', var = excelRange(rate))

        lower_ci = tab.filter(contains_string('Lower CI')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Lower_CI('Lower CI given at cell range: {}', var = excelRange(lower_ci))

        upper_ci = tab.filter(contains_string('Upper CI')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Upper_CI('Upper CI given at cell range: {}', var = excelRange(upper_ci))
        
        death_cell = tab.filter(contains_string('Death'))
        observations = death_cell.fill(DOWN).is_not_blank()
        
        measure_type = 'Count'
        trace.Measure_type("Unit hardcoded as Count")
        unit = 'Deaths'
        trace.Unit("Unit hardcoded as Deaths")
        
        dimensions = [
            HDim(period, 'Period', CLOSEST, LEFT),
            HDim(cause_of_death, 'Cause of death', DIRECTLY, LEFT),
            HDim(sex, 'Sex', DIRECTLY, LEFT),
            HDim(decile, 'Decile', DIRECTLY, LEFT),
            HDim(rate, 'Rate', DIRECTLY, RIGHT),
            HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
            HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
            HDimConst('Country', country),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
       # savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())

# Notes from tab

notes = """ 
1 Age-standardised mortality rates are presented per 100,000 people and standardised to the 2013 European Standard Population. Age-standardised mortality rates allow for differences in the age structure of populations and therefore allow valid comparisons to be made between geographical areas, the sexes and over time.
2 The lower and upper 95% confidence limits have been provided. These form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the estimated figure. Calculations based on small numbers of events are often subject to random fluctuations. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
3 Rates have been calculated using 2018 mid-year population estimates as a base, the most up-to-date estimates when published. Rates have not been adjusted to take into account the period of interest and may differ from rates presented in other publications.
4 Coronavirus (COVID-19) as a causes of death was defined using the International Classification of Diseases, Tenth Revision (ICD-10) codes U07.1 and U07.2. Figures include deaths where coronavirus (COVID-19) was the underlying cause or was mentioned on the death certificate as a contributory factor. Figures do not include neonatal deaths (deaths under 28 days).
5 Figures for England exclude deaths of non-residents and are based on May 2020 boundaries.
6 Figures are based on the date of death occurrence in each month between 1 March and 30 June 2020 and registered up to (and including) 11 July 2020. More information on registration delays can be found on the ONS website:
https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/2018
7 Deprivation deciles are based on the Index of Multiple Deprivation, version 2019 (IMD 2019) which is the official measure of relative deprivation for small areas in England. It is designed to identify those small areas where there are the highest concentrations of several different types of deprivation. IMD deciles range from 1 to 10, with 1 being the most deprived and 10 being the least deprived. The IMD classification works by grouping together 2011 census Lower Super Output Areas (LSOAs) based on their level of deprivation. LSOA's are based on postcode boundaries as of May 2020. For more information on IMD, and the latest version of the classification system, please follow this link:
https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
"""

# +
df = trace.combine_and_trace(datasetTitle, "df")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

trace.Period("Formating to /id/gregorian-month/{year}-{month}")
df['Period'] =  df["Period"].apply(date_time)

tidy_3 = df[['Period', 'Cause of death', 'Sex', 'Country', 'Decile', 'Rate', 'Lower CI', 'Upper CI', 'Value', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
output_title = title + "Number_of_deaths_and_age-standardised_rates_by_sex_deprivation_deciles_in_England,"
scraper.dataset.comment = notes
tidy_3.drop_duplicates().to_csv(out / f'{output_title}.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy_3

# -


