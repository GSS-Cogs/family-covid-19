# # WG Survey of public views on the coronavirus  COVID-19 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Survey of public views on the coronavirus (COVID-19)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

# +
tab = tabs['Data']
cell = tab.filter('Public views & outlook')
cell.assert_one()
response = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()  
question = response.shift(-1,0)
survey = cell.expand(DOWN).is_not_blank().is_not_whitespace() - question
observations = date.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(response,'Average Response',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDim(question, 'Survey Question', DIRECTLY,LEFT),
            HDim(survey,'Survey Question Category', CLOSEST,ABOVE ),
            HDimConst('Unit','percent'),  
            HDimConst('Measure Type','percentage')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

from IPython.core.display import HTML
for col in new_table:
    if col not in ['Value']:
        new_table[col] = new_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(new_table[col].cat.categories) 

# +
new_table['Marker'] = new_table['Marker'].map(
    lambda x: {
        '-' : 'Statistical disclosure'
        }.get(x, x))

def user_perc(x,y):
    
    if (str(x) ==  'Statistical disclosure'): 
        
        return 0
    else:
        return y
    
new_table['Value'] = new_table.apply(lambda row: user_perc(row['Marker'], row['Value']), axis = 1)

# +
month_num_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 
                  'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 
                  'November': '11', 'December': '12'}

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    month_string = time_value.strip().split(' ')[-1]
    month_num = month_num_dict[month_string]
    if len(date_string)  == 1:
        date_string = '0' + date_string
    return 'gregorian-day/2020-'+ month_num + '-' + date_string + 'T00:00/P3D'
new_table["Period"] = new_table["Period"].apply(date_time)
# -

tidy = new_table[['Period','Survey Question Category','Survey Question','Average Response','Measure Type',
                  'Unit','Marker', 'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)
