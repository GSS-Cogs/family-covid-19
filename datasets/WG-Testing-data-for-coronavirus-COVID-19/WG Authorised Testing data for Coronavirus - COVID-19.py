# # WG Authorised Testing data for Coronavirus - COVID-19

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Testing data for coronavirus (COVID-19)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

# +
tab = tabs['tests_authorised']
cell = tab.excel_ref('A9')
test = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
date = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = test.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(test,'Authorised Tests',DIRECTLY,ABOVE),
            HDim(date, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Cumulative Count'),  
            HDimConst('Measure Type','Tests')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
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

next_table['Marker'] = ''


def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
next_table["Period"] = next_table["Period"].apply(date_time)

list(next_table)

tidy = next_table[['Period','Authorised Tests' , 'Marker', 'Measure Type',
                          'Unit',  'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'wg authorised corona virus testing data.csv', index = False)
