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
# Table 5
# ________________________________________________________________________________________________________________
#

datasetTitle = 'Deaths involving COVID-19 by local area and deprivation'
for tab in tabs:
    if tab.name in ['Table 5']:
        columns=["Period", "Cause of detah", "Country", "House of Commons Library MSOA Names", "ONS geography MSOA name", "MSOA code", 'Marker', "Measure type", "Unit"]
        trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)

        cause_of_death = tab.filter(contains_string('COVID-19')).expand(RIGHT).is_not_blank() 
        trace.Cause_of_detah('Cause of death given at cell range: {}', var = excelRange(cause_of_death))

        country = "England and Wales"
        trace.Country("Country hardcoded as England and Wales")
        
        period = tab.filter(contains_string('House of Commons Library MSOA Names')).shift(1,0).expand(RIGHT).is_not_blank()
        trace.Period('Period / Month given at cell range: {}', var = excelRange(period))
        
        house_of_commons_mosa_names = tab.filter(contains_string('House of Commons Library MSOA Names')).shift(0,1).expand(DOWN).is_not_blank()
        trace.House_of_Commons_Library_MSOA_Names('House of Commons Library MSOA Names given at cell range: {}', var = excelRange(house_of_commons_mosa_names))
        
        ons_geo_mosa_names = tab.filter(contains_string('ONS geography MSOA name')).shift(0,1).expand(DOWN).is_not_blank()
        trace.ONS_geography_MSOA_name('ONS geography MSOA name given at cell range: {}', var = excelRange(ons_geo_mosa_names))

        msoa_code = tab.filter(contains_string('MSOA code')).shift(0,1).expand(DOWN).is_not_blank()
        trace.MSOA_code('MSOA code given at cell range: {}', var = excelRange(msoa_code))
        
        observations = period.fill(DOWN).is_not_blank()
        
        measure_type = 'Count'
        trace.Measure_type("Unit hardcoded as Count")
        unit = 'Deaths'
        trace.Unit("Unit hardcoded as Deaths")
        
        dimensions = [
            HDim(period, 'Period', DIRECTLY, ABOVE),
            HDim(cause_of_death, 'Cause of death', CLOSEST, LEFT),
            HDim(msoa_code, 'MSOA code', DIRECTLY, LEFT),
            HDim(ons_geo_mosa_names, 'ONS geography MSOA name', DIRECTLY, LEFT),
            HDim(house_of_commons_mosa_names, 'House of Commons Library MSOA Names', DIRECTLY, LEFT),
            HDimConst('Country', country),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet) 
        trace.store("df", tidy_sheet.topandas())

# Notes from tab

notes = """
1 Coronavirus (COVID-19) as a causes of death was defined using the International Classification of Diseases, Tenth Revision (ICD-10) codes U07.1 and U07.2. Figures include deaths where coronavirus (COVID-19) was the underlying cause or was mentioned on the death certificate as a contributory factor. Figures do not include neonatal deaths (deaths under 28 days).
2 Figures for MSOA's in England and Wales exclude deaths of non-residents and are based on May 2020 boundaries.
3 Figures are based on the date of death occurrence in each month between 1 March and 30 June 2020 and registered up to (and including) 11 July 2020. More information on registration delays can be found on the ONS website:
https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/2018
4 To protect confidentiality, a small number of deaths have been reallocated between neighbouring areas. Due to the method used for this, figures for some areas may be different to previously published data.
5 Locally adopted MSOA names are provided by House of Commons Library (version 1.1.0). While these names are not officially supported for National Statistics they are provided here to help local users.
"""

# +
df = trace.combine_and_trace(datasetTitle, "df")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

trace.Period("Formating to /id/gregorian-month/{year}-{month}")
df['Period'] =  df["Period"].apply(date_time)

tidy_5 = df[['Period', 'Cause of death', 'Country', 'ONS geography MSOA name', 'ONS geography MSOA name', 'House of Commons Library MSOA Names', 'Value', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
output_title = title + "Number_of_deaths_by_Middle_Layer_Super_Output_Area"
scraper.dataset.comment = notes
tidy_5.drop_duplicates().to_csv(out / f'{output_title}.csv', index = False)
scraper.dataset.family = 'covid-19'

trace.output()
tidy_5
