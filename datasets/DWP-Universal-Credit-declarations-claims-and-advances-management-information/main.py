# # DWP Universal Credit declarations  claims  and advances  management information 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper

tabs = { tab.name: tab for tab in scraper.distribution(latest=True).as_databaker() }
list(tabs)

df = pd.DataFrame()


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]

def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-instant/' + time_string[:10] + 'T00:00:00'   


# -

# List of tables:	
# Table 1	Number of households and individuals making a Universal Credit declaration
# Table 2	Number of households and individuals making a Universal Credit declaration Totals by time period
# Table 3	Number of Universal Credit Advances, by type of advance
# Table 4	Number of Universal Credit Advances Time Periods Totals by type of advance
#
# Tables 1 and 3 only transformed as 2 and 4 can be derived. 

for name, tab in tabs.items():
    if 'Front' in name or 'Contents' in name or 'Notes' in name or 'Definitions' in name or '2' in name or '4' in name:
        continue
    measure_type = 'Advances' #or Households and Individuals, will be filtered out 
    period = tab.excel_ref('C7').expand(RIGHT).is_not_blank() 
    
    if tab.name == '3':
        print('now at tab 3')
        period = tab.excel_ref('C8').expand(RIGHT).is_not_blank() 

    univeral_credit_stage = tab.excel_ref('B12').expand(DOWN).is_not_blank() 
    observations = period.fill(DOWN).is_not_blank().is_not_whitespace()
    Dimensions = [
        HDim(period,'Period',DIRECTLY,ABOVE),
        HDim(univeral_credit_stage,'Universal Credit Stage',DIRECTLY,LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit','Count')
    ]
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    savepreviewhtml(c1, fname=tab.name + "Preview.html")
    new_table = c1.topandas()
    df = pd.concat([df, new_table], sort=False)


import numpy as np
df.rename(columns={'OBS': 'Value'}, inplace=True)
f1=((df['Universal Credit Stage'] =='Households making a Universal Credit declaration') | (df['Universal Credit Stage'] == 'Individuals making a Universal Credit declaration'))   
df.loc[f1,'Measure Type'] = 'Households and Individuals'

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

df["Period"] = df["Period"].apply(date_time)
for column in df:
    if column in ('Universal Credit Stage'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Period', 'Universal Credit Stage', 'Measure Type', 'Unit','Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)

# +
scraper.dataset.family = 'covid-19'

## Adding short metadata to description
additional_metadata = """ The management information is a view of what is recorded on the administrative data and have not been quality assured and processed to the standards required to be official statistics. Moreover, they will not have been derived to the same methodology as official statistics, and therefore the MI and official statistics will not be directly comparable. 

Figures relate to Great Britain only, as such Northern Ireland is not included. Figures are rounded to the nearest 10. 
Components may not sum to total due to rounding. 
Figures fewer than 5 are supressed due to rounding to avoid disclosure required by the Data Protection Act 2018 and in accordance with principle T6 of the Code of Practice for Statistics.             

"""
scraper.dataset.description = scraper.dataset.description + additional_metadata

#from gssutils.metadata import THEME
#with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    #metadata.write(scraper.generate_trig())

# +
#csvw = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')
