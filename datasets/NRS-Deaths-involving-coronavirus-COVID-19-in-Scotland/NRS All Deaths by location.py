# # NRS Deaths by location

from gssutils import * 
import json 

#info = json.load(open('info.json')) 
#landingPage = info['landingPage'] 
#landingPage 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "COVID-19 Statistical Report"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

tab = tabs['Table 3 - deaths by location']
cell = tab.filter(contains_string('Deaths where COVID-19'))
cell.assert_one()

date = tab.filter(contains_string('Table 3'))
date.assert_one()

board = tab.filter(contains_string ('Deaths by NHS Board'))
board.assert_one()
location = cell.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace()
deaths = cell.expand(RIGHT).is_not_blank().is_not_whitespace()

area = tab.filter(contains_string ('Deaths by Council Area of usual residence'))
area.assert_one()

nhs = board.fill(DOWN).is_not_blank().is_not_whitespace() - \
        area.expand(DOWN)

# +
observations2 = nhs.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions2 = [
            HDim(nhs,'Deaths by NHS Board',DIRECTLY,LEFT),
            HDim(deaths, 'Deaths Registered', CLOSEST, LEFT),
            HDim(location, 'Deaths by location', DIRECTLY, ABOVE),
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
        tab.filter(contains_string('Footnotes')).expand(DOWN) | \
        tab.filter(contains_string('All areas'))
allareas = tab.filter(contains_string('All areas')).fill(RIGHT).is_not_blank().is_not_whitespace()
observations3 = council.fill(RIGHT).is_not_blank().is_not_whitespace() | allareas
Dimensions3 = [
            HDim(council,'Deaths by Council Area',DIRECTLY,LEFT),
            HDim(deaths, 'Deaths Registered', CLOSEST, LEFT),
            HDim(location, 'Deaths by location', DIRECTLY, ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Deaths')

]  
c4 = ConversionSegment(observations3, Dimensions3, processTIMEUNIT=True)
new_table3 = c4.topandas()
import numpy as np
new_table3.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table3])
# -

next_table.fillna('All', inplace = True)

from IPython.core.display import HTML
for col in next_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

next_table['Deaths by location'] = next_table['Deaths by location'].map(
    lambda x: { 'Care\nHome': 'Care Home', 'Home / Non-institution' : 'Home or Non-institution',
        'Other\ninstitution3'  :  'Other institution'   
        }.get(x, x))

tidy = next_table[['Deaths Registered',
                 'Deaths by Council Area',
                 'Deaths by location',
                 'Deaths by NHS Board',
                 'Measure Type',
                 'Unit',
                 'Value']]

tidy['Deaths Registered'] = tidy['Deaths Registered'].str.replace('Deaths from all causes','Total deaths from all causes')

tidy['Deaths by Council Area'] = tidy['Deaths by Council Area'].str.replace('All areas','All')

# +
#tidy['Deaths by Council Area'].unique()
# -

tidy.head(60)
