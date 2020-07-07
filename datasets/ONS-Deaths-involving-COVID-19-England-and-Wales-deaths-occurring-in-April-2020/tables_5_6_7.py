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
datasetTitle = 'Deaths involving COVID-19 by main and pre-existing condition, England and Wales'
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

month_look_up = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 
                  'July':'07','August':'08','September':'09', 'October':'10','November':'11', 'December':'12'}
def date_time(time_value):
    date_string = time_value.strip()
    if len(date_string)  == 2:
        return 'month/2020-' + date_string


# -

for tab in tabs:
    
    datacube_name = "Deaths involving COVID-19 by main and pre-existing condition, England and Wales"
    
    if tab.name.lower() == 'table 5':
        columns=["Pre existing condition", "Main pre existing condition", "Country","Period", 'Age Group', 'Sex', "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
        
        remove_notes = tab.filter(contains_string('Based on boundaries')).expand(RIGHT).expand(UP)
        country = tab.filter(contains_string('England and Wales')).expand(RIGHT).is_not_blank() - remove_notes
        trace.Country('Country detailed at cell value: {}', var = cellLoc(country))
        
        pre_existing_condition = tab.filter(contains_string('Main pre-existing condition')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Pre_existing_condition('pre-existing condition detailed at cell value: {}', var = cellLoc(pre_existing_condition))
        
        main_pre = 'Yes'
        sex = 'All'
        trace.Sex('Hardcoded value as: All')
        age_group = 'All'
        trace.Age_Group('Hardcoded value as: All') 
        measure_type = 'Count'
        trace.Measure_Type('Hardcoded value as: Count')
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: Deaths') 
        
        observations = tab.filter(contains_string('Number of deaths')).shift(0,1).expand(DOWN).is_not_blank()
        
        dimensions = [
            #HDim(period_month, 'Period', DIRECTLY, ABOVE),
             HDim(country, 'Country', CLOSEST, LEFT),
             HDim(pre_existing_condition, 'Pre existing condition', DIRECTLY, LEFT),
             HDimConst('Measure Type', measure_type),
             HDimConst('Unit', unit),
             HDimConst('Sex', sex),
             HDimConst('Age Group', age_group),
             HDimConst('Main pre existing condition', main_pre),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
        
    if (tab.name == 'Table 6a') or (tab.name == 'Table 6b') or (tab.name == 'Table 6c'):
        columns=["Pre existing condition", "Main pre existing condition", "Country","Period", 'Age Group', 'Sex', "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
   
        pre_existing_condition = tab.filter(contains_string('Main pre-existing condition')).shift(0,1).expand(DOWN).is_not_blank()            
        trace.Pre_existing_condition('Main pre-existing condition detailed at cell value: {}', var = cellLoc(pre_existing_condition))
                
        country = tab.filter(contains_string('Country')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Country('Country detailed at cell value: {}', var = cellLoc(country))
                
        main_pre = 'Yes'
                
        age_group = tab.filter(contains_string('Age')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Age_Group('Age_Group detailed at cell value: {}', var = cellLoc(age_group))
                
        sex = tab.filter(contains_string('Sex')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))
                
        observations = tab.filter(contains_string('Main pre-existing condition')).shift(1,1).expand(DOWN).is_not_blank()
        measure_type = 'Count'
        trace.Measure_Type('Hardcoded value as: Count')
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: Deaths') 
            
        dimensions = [
                #HDim(period_month, 'Period', DIRECTLY, ABOVE),
                HDim(country, 'Country', DIRECTLY, LEFT),
                HDim(sex, 'Sex', DIRECTLY, LEFT),
                HDim(age_group, 'Age Group', DIRECTLY, LEFT),
                HDim(pre_existing_condition, 'Pre existing condition', DIRECTLY, LEFT),
                HDimConst('Measure Type', measure_type),
                HDimConst('Unit', unit),
                HDimConst('Main pre existing condition', main_pre),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
    
    if (tab.name == 'Table 7a') or (tab.name == 'Table 7b') or (tab.name == 'Table 7c'):
        columns=["Pre existing condition", "Main pre existing condition", "Country","Period", 'Age Group', 'Sex', "Measure Type", "Unit"]
        trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
  
        pre_existing_condition = tab.filter(contains_string('Country')).shift(2,1).expand(DOWN).is_not_blank()
        trace.Pre_existing_condition('pre-existing condition detailed at cell value: {}', var = cellLoc(pre_existing_condition))
        
        country = tab.filter(contains_string('Country')).shift(0,1).expand(DOWN).is_not_blank()
        trace.Country('Country detailed at cell value: {}', var = cellLoc(country))
        
        main_pre = 'No'
        
        age_group = tab.filter(contains_string('Country')).shift(2,1).expand(RIGHT)
        trace.Age_Group('Age_Group detailed at cell value: {}', var = cellLoc(age_group))
        
        sex = tab.filter(contains_string('Country')).shift(3,0).expand(RIGHT).is_not_blank()
        trace.Sex('Sex detailed at cell value: {}', var = cellLoc(sex))
        
        observations = pre_existing_condition.fill(RIGHT).is_not_blank()
        
        measure_type = 'Count'
        trace.Measure_Type('Hardcoded value as: Count')
        unit = 'Deaths'
        trace.Unit('Hardcoded value as: Deaths') 
        
        dimensions = [
                    #HDim(period_month, 'Period', DIRECTLY, ABOVE),
                    HDim(country, 'Country', DIRECTLY, LEFT),
                    HDim(sex, 'Sex', CLOSEST, LEFT),
                    HDim(age_group, 'Age Group', DIRECTLY, ABOVE),
                    HDim(pre_existing_condition, 'Pre existing condition', DIRECTLY, LEFT),
                    HDimConst('Measure Type', measure_type),
                    HDimConst('Unit', unit),
                    HDimConst('Main pre existing condition', main_pre),
                ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())



# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
trace.add_column("Value")
trace.Value("Rename databaker column OBS to Value")
df.rename(columns={'OBS': 'Value'}, inplace=True)

f1=((df['Age Group'] =="") & (df['Sex'] =='Total'))
df.loc[f1,'Age Group'] = 'Total'

temporal_date = 'gregorian-interval/2020-03-01T00:00:00/P3M'

df



# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

notes = """
1. Figures exclude deaths of non-residents
2. Figures are provisional
3. Based on deaths involving COVID-19 (ICD-10 codes U07.1 and U07.2) rather than deaths where COVID-19 was the underlying cause of death
4. Deaths occurring between March and May 2020 rather than deaths registered between March and May 2020
5. Main pre-existing causes are grouped using the ONS Leading Causes of Deaths list (https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/methodologies/userguidetomortalitystatistics/leadingcausesofdeathinenglandandwalesrevised2016) and International Classification of Disease version 10 blocks of causes.
6. Including deaths registered up until 6 June 2020.
7. Based on boundaries as of May 2020
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)
title = pathify(datasetTitle)
scraper.dataset.comment = notes
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)
scraper.dataset.family = 'covid-19'
trace.output()

scraper.dataset.temporal = "http://reference.data.gov.uk/id/" + temporal_date
import os
df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()


