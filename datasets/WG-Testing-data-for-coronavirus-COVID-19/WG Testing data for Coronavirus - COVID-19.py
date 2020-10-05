# # WG Testing data for coronavirus  COVID-19 

from gssutils import * 
import json 

info = json.load(open('info.json'))

# +

"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


req = Request(info["landingPage"], headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
plaintext = html.decode('utf8')
soup = BeautifulSoup(plaintext)
for a in soup.select('#series--content > div:nth-child(1) > div > div > ul > li > div > div.index-list__title > a'):
    dataPage = a['href']
req = Request(dataPage, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
plaintext = html.decode('utf8')
soup = BeautifulSoup(plaintext)
for a in soup.select('.accordion__content > div > div > div > div > div > div > div.document__details > h3 > a'):
    dataURL = a['href']

with open('info.json', 'r+') as info:
    data = json.load(info)
    data["dataURL"] = dataURL
    info.seek(0)
    json.dump(data, info, indent=4)
    info.truncate()
"""

# +

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Testing data for coronavirus (COVID-19)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

# +
tab = tabs['Individuals_tested']
cell = tab.excel_ref('A14')
test = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
date = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = test.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(test,'Test Outcome',DIRECTLY,ABOVE),
            HDim(date, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Cumulative Count'),  
            HDimConst('Measure Type','People')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table])

# +
tab = tabs['Critical_workers_category']
cell = tab.filter('Category')
cell.assert_one()
cases = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()  
category = cell.fill(DOWN).is_not_blank().is_not_whitespace()
observations = cases.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(cases,'Test Outcome',DIRECTLY,ABOVE),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDim(category, 'Critical Worker Category', DIRECTLY,LEFT),
            HDimConst('Unit','Cumulative Count'),  
            HDimConst('Measure Type','People')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table])

# +
tab = tabs['Critical_workers_detail']
cell = tab.filter('Category')
cell.assert_one()
cases = cell.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace()
date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()  
category = cell.fill(DOWN).is_not_blank().is_not_whitespace()
description = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = cases.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(cases,'Test Outcome',DIRECTLY,ABOVE),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDim(category, 'Critical Worker Category', DIRECTLY,LEFT),
            HDim(description, 'Emergency Services Worker',DIRECTLY,LEFT ),
            HDimConst('Unit','Cumulative Count'),  
            HDimConst('Measure Type','People')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
next_table = pd.concat([next_table, new_table])

# +
tab = tabs['Location_tests']
cell = tab.filter('Location')
cell.assert_one()
test = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()  
location = cell.fill(DOWN).is_not_blank().is_not_whitespace()
description = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = test.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(test,'Test Outcome',DIRECTLY,ABOVE),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDim(location, 'Test Location', DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Tests')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
def user_perc1(x,y):
    
    if (str(x) ==  'Cumulative tests completed'): 
        
        return y
    else:
        return 'Percentage'
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc1(row['Test Outcome'], row['Measure Type']), axis = 1)
def user_perc2(x,y):
    
    if (str(x) ==  'Cumulative tests completed'): 
        
        return y
    else:
        return 'Percent'
    
new_table['Unit'] = new_table.apply(lambda row: user_perc2(row['Test Outcome'], row['Unit']), axis = 1)
next_table = pd.concat([next_table, new_table])
# -

# Test outcome codelist not complete missing codes labelled as `error`

next_table.fillna('All', inplace = True)

from IPython.core.display import HTML
for col in next_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

next_table['Test Outcome'] = next_table['Test Outcome'].map(
    lambda x: {
        'Individuals tested (testing episodes) by test date' : 'error',
       'Cumulative individuals tested (testing episodes)' : 'Total',
       'Positive cases by test date' : 'error',
        'Cumulative positive cases' : 'Positive',
       'Cumulative negative cases' : 'Negative', 
        'Cumulative number of tests' : 'error',
       'Cumulative tests completed' : 'Total', 
        '% results within 1 day' : 'Results within 1 Day',
       '% results within 2 days' : 'Results within 2 Day', 
        '% results within 3 days' : 'Results within 3 Day'             
        }.get(x, x))

next_table['Test Location'] = next_table['Test Location'].map(
    lambda x: { 'Tested in hospital' : 'Hospital' , 
               'Tested at coronavirus testing unit': 'Coronavirus Testing Unit' ,
       'Testing at drive-through centres' : 'Drive-through Centres'          
        }.get(x, x))

# +
next_table['Marker'] = next_table['Marker'].map(
    lambda x: {
        '*' : 'Statistical disclosure',
        'All' : ''        
        }.get(x, x))

def user_perc3(x,y):
    
    if (str(x) ==  'Statistical disclosure'): 
        
        return 0
    else:
        return y
    
next_table['Value'] = next_table.apply(lambda row: user_perc3(row['Marker'], row['Value']), axis = 1)


# -

def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
next_table["Period"] = next_table["Period"].apply(date_time)

tidy = next_table[['Period','Critical Worker Category', 'Emergency Services Worker',
                         'Test Location','Test Outcome',  'Marker', 'Measure Type',
                          'Unit',  'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'wg corona virus testing data.csv', index = False)
