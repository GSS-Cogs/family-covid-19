# -*- coding: utf-8 -*-
# # NRS Deaths involving coronavirus  COVID-19  in Scotland 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "COVID-19 Statistical Report"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

tab = tabs['Table 1 - COVID deaths']
cell = tab.filter('Week beginning')
cell.assert_one()

date = cell.fill(RIGHT)
#date = cell.fill(RIGHT).is_not_blank().is_not_whitespace() 

sex = tab.filter('Persons') | tab.filter('Females') | tab.filter('Males')

agegroup = tab.filter('Deaths by age group')
agegroup.assert_one()

board = tab.filter(contains_string ('Deaths by NHS Board of usual residence'))
board.assert_one()

location = tab.filter(contains_string ('Deaths by location'))
location.assert_one()

age = agegroup.fill(DOWN).is_not_blank().is_not_whitespace() - \
                tab.filter(contains_string('Deaths by NHS Board')).expand(DOWN).is_not_blank().is_not_whitespace()

deaths = cell.fill(DOWN).is_not_blank().is_not_whitespace() - sex -tab.filter('Footnotes').expand(DOWN)

area = tab.filter(contains_string ('Deaths by Council Area of usual residence'))
area.assert_one()

nhs = board.fill(DOWN).is_not_blank().is_not_whitespace() - \
        tab.filter(contains_string('Deaths by Council Area of usual residence')).expand(DOWN)

# +
observations = deaths.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(deaths,'Deaths Registered',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table])
# -

new_table.head(60)

# +
observations1 = age.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions1 = [
            HDim(age,'NRS Age Group',DIRECTLY,LEFT),
            HDim(sex, 'Deaths by Gender', CLOSEST,ABOVE),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c2 = ConversionSegment(observations1, Dimensions1, processTIMEUNIT=True)
new_table1 = c2.topandas()
import numpy as np
new_table1.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table1])

# +
observations2 = nhs.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions2 = [
            HDim(nhs,'Deaths by NHS Board',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c3 = ConversionSegment(observations2, Dimensions2, processTIMEUNIT=True)
new_table2 = c3.topandas()
import numpy as np
new_table2.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table2])

# +
council = area.fill(DOWN).is_not_blank().is_not_whitespace() - \
        tab.filter(contains_string('Deaths by location')).expand(DOWN)
observations3 = council.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions3 = [
            HDim(council,'Deaths by Council Area',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c4 = ConversionSegment(observations3, Dimensions3, processTIMEUNIT=True)
new_table3 = c4.topandas()
import numpy as np
new_table3.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table3])

# +
place = location.fill(DOWN).is_not_blank().is_not_whitespace() - \
        tab.filter(contains_string('Other institution')).fill(DOWN)
observations4 = place.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions4 = [
            HDim(place,'Deaths by location',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c5 = ConversionSegment(observations4, Dimensions4, processTIMEUNIT=True)
new_table4 = c5.topandas()
import numpy as np
new_table4.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table4])
# -

next_table.fillna('All', inplace = True)


def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-interval/' + time_string[:10] + 'T00:00:00/P1D'
next_table["Period"] = next_table["Period"].apply(date_time)

from IPython.core.display import HTML
for col in next_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

next_table['Deaths Registered'] = next_table['Deaths Registered'].map(
    lambda x: { 'All' : 'Deaths involving COVID-19' , 
               'Deaths involving COVID-194' : 'Deaths involving COVID-19',
       'Deaths involving COVID-194 - females' : 'Deaths involving COVID-19 - females',
       'Deaths involving COVID-194 - males'  :'Deaths involving COVID-194 - males'       
        }.get(x, x))

tidy = next_table[['Period','Deaths Registered',
                     'Deaths by Council Area',
                     'Deaths by NHS Board',
                     'NRS Age Group',
                     'Deaths by location', 'Deaths by Gender', 'Measure Type','Unit','Value']]

tidy['Deaths Registered'] = tidy['Deaths Registered'].str.replace('-194','-19')
tidy['Deaths by Gender'][tidy['Deaths Registered'].str.contains('19 - males')] = 'Males'
tidy['Deaths by Gender'][tidy['Deaths Registered'].str.contains('19 - females')] = 'Females'
tidy['Deaths Registered'] = tidy['Deaths Registered'].str.replace('-19 - females','-19')
tidy['Deaths Registered'] = tidy['Deaths Registered'].str.replace('-19 - males','-19')

tidy.head(60)

# +
#### "landingPage": "https://www.nrscotland.gov.uk/covid19stats",
