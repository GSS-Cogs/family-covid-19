# -*- coding: utf-8 -*-
# # WG Summary data about coronavirus  COVID-19  and the response to it 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Testing data for coronavirus (COVID-19)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

try :
    tab = tabs['Food_parcels']
    cell = tab.filter('Food parcel orders received')
    cell.assert_one()
    food = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
    obs = tab.filter('Total to date').expand(RIGHT).expand(DOWN)
    observations = food.fill(DOWN).is_not_blank().is_not_whitespace() - obs
    Dimensions = [
                HDim(food,'Food Parcel Status',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Parcel')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    next_table = pd.concat([next_table, new_table])
except:
    print ('Sheet not found')
    Marker = False 

from IPython.core.display import HTML
for col in next_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

# +
next_table['Marker'] = next_table['Marker'].map(
    lambda x: {
        '~' : 'The data item is not yet available'
    }.get(x, x))

def user_perc3(x,y):
    if (str(x) ==  'The data item is not yet available'): 

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

list(next_table)

tidy = next_table[['Food Parcel Status', 'Period', 'Unit', 'Measure Type','Value', 'Marker']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'WG COVID-19 Food Parcel Support.csv', index = False)
