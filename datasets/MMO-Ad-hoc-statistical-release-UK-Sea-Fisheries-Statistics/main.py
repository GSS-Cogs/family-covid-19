# -*- coding: utf-8 -*-
# # MMO Ad hoc statistical release  UK Sea Fisheries Statistics 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

# +
#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper 
# -

tabs = { tab.name: tab for tab in scraper.distribution(latest=True).as_databaker() }
list(tabs)

# +
# %%capture

all_dat = []

# Value and volumn landed by country, vessel length and species group
# %run "table_1.py"
all_dat.append(tidy)
# Value, volume landed and number of trips by country and admin port
# %run "table_2.py"
all_dat.append(tidy)
# Value and volumn landed by species group and country
# %run "table_3.py"
all_dat.append(tidy)
# Value and volumn landed by country and vessel length
# %run "table_4.py"
all_dat.append(tidy)

# +
import numpy as np

vllookup = {
    'u10m total': 'All',
    '10-12m total': 'All',
    'o12m total': 'All'
}
all_dat[0]["Species Group"] = all_dat[0]["Species Group"].map(lambda x: vllookup.get(x, x))

geoglookup = {
    'Northern Ireland total': 'N07000001',
    'Wales total': 'W08000001', 
    'Scotland total': 'S04000001',
    'England total': 'E92000001',
    'UK total': 'K02000001',
    'Northern Ireland': 'N07000001',
    'Wales': 'W08000001', 
    'Scotland': 'S04000001',
    'England': 'E92000001',
    'UK': 'K02000001'
}

fishlookup = {
    'Demersal total': 'Demersal',
    'Pelagic total': 'Pelagic',
    'Shellfish total': 'Shellfish'
}

all_dat[0]["Country"] = all_dat[0]["Country"].map(lambda x: geoglookup.get(x, x))

all_dat[0] = all_dat[0].replace(np.nan, '', regex=True)

all_dat[0]['Admin Port'] = 'UK total'
all_dat[0] = all_dat[0][['Period','Country','Vessel Length','Species Group','Admin Port','Measure Type','Unit','Marker','Value']]
# -

all_dat[0].head(5)

#all_dat[0]['Value'] = round(all_dat[0]['Value'],1)
all_dat[1]["Country"] = all_dat[1]["Country"].map(lambda x: geoglookup.get(x, x))
all_dat[1] = all_dat[1].replace(np.nan, '', regex=True)
all_dat[1] = all_dat[1][['Period','Country','Vessel Length','Species Group','Admin Port','Measure Type','Unit','Marker','Value']]
all_dat[1].head(5)

# +
all_dat[2]["Country"] = all_dat[2]["Country"].map(lambda x: geoglookup.get(x, x))
all_dat[2] = all_dat[2].replace(np.nan, '', regex=True)
all_dat[2]['Admin Port'] = 'UK total'
all_dat[2] = all_dat[2][['Period','Country','Vessel Length','Species Group','Admin Port','Measure Type','Unit','Marker','Value']]

all_dat[2].head(5)

# +
if 'Marker' not in all_dat[3].columns:
    all_dat[3]['Marker'] = ''
all_dat[3]["Country"] = all_dat[3]["Country"].map(lambda x: geoglookup.get(x, x))
all_dat[3] = all_dat[3].replace(np.nan, '', regex=True)
all_dat[3]['Admin Port'] = 'UK total'
all_dat[3]['Species Group'] = 'All'
all_dat[3] = all_dat[3][['Period','Country','Vessel Length','Species Group','Admin Port','Measure Type','Unit','Marker','Value']]

all_dat[3].head(5)
# -

joined_dat = pd.concat([all_dat[0],all_dat[1],all_dat[2],all_dat[3]])

joined_dat = joined_dat.rename(columns={'Period':'Year'})
joined_dat['Value'][joined_dat['Marker'] == 'Figure less than 1'] = 0
joined_dat["Species Group"] = joined_dat["Species Group"].map(lambda x: fishlookup.get(x, x))

# +
joined_dat_ton = joined_dat[joined_dat['Unit'] == 'Tonnes']
print('Ton count 1: ' + str(joined_dat_ton['Country'].count()))
# Some columns are duplicates but have different rounding on the Value column, get rid based on rest of columns
print('Getting rid of duplicates')
joined_dat_ton = joined_dat_ton.drop_duplicates(['Year','Country','Vessel Length','Species Group','Admin Port'], keep='first')
print('Ton count 2: ' + str(joined_dat_ton['Country'].count()))
joined_dat_ton['Vessel Length'][joined_dat_ton['Vessel Length'] == 'Total'] = 'All'
joined_dat_ton['Admin Port'][joined_dat_ton['Admin Port'] == 'UK total'] = 'UK'

joined_dat_ton['Vessel Length'] = joined_dat_ton['Vessel Length'].apply(pathify).str.strip()
joined_dat_ton['Species Group'] = joined_dat_ton['Species Group'].apply(pathify).str.strip()
joined_dat_ton['Admin Port'] = joined_dat_ton['Admin Port'].apply(pathify).str.strip()

del joined_dat_ton['Measure Type']
del joined_dat_ton['Unit']
# -

for c in joined_dat_ton.columns:
    if 'Value' not in c:
        print(c)
        print(joined_dat_ton[c].unique())
        print("#############################################")
print('Dataset 1: ' + str(all_dat[0]['Country'].count()))
print('Dataset 2: ' + str(all_dat[1]['Country'].count()))
print('Dataset 3: ' + str(all_dat[2]['Country'].count()))
print('Dataset 4: ' + str(all_dat[3]['Country'].count()))
print('JoinedDataset: ' + str(joined_dat['Country'].count()))
print('JoinedDatasetTON: ' + str(joined_dat_ton['Country'].count()) + ' - only Quantity')

joined_dat_ton.head(60)

# +
import os
from urllib.parse import urljoin

notes = ''

csvName = 'quantity_observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
#print(joined_dat_ton.count())
joined_dat_ton = joined_dat_ton.drop_duplicates()
#print(joined_dat_ton.count())
joined_dat_ton.drop_duplicates().to_csv(out / csvName, index = False)

scraper.dataset.family = 'covid_19'
#scraper.dataset.description = scraper.dataset.description + '\nGuidance documentation can be found here:\n' + notes
scraper.dataset.comment = 'Total domestic electricity consumption for LSOA regions across England, Wales & Scotland'
scraper.dataset.title = 'Ad hoc statistical release UK Sea Fisheries Statistics - Quantity (t)'

dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scraper.dataset.family}/' + Path(os.getcwd()).name)).lower()
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)


csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
# Remove subset of data
#out / csvName).unlink()
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

# +
#info = json.load(open('info.json')) 
#codelistcreation = info['transform']['codelists'] 
#print(codelistcreation)
#print("-------------------------------------------------------")
#dat = joined_dat_ton
#codeclass = CSVCodelists()
#for cl in codelistcreation:
#    if cl in joined_dat.columns:
#        dat[cl] = dat[cl].str.replace("-"," ")
#        dat[cl] = dat[cl].str.capitalize()
#        codeclass.create_codelists(pd.DataFrame(dat[cl]), 'codelists', scraper.dataset.family, Path(os.getcwd()).name.lower())

# +
#a = joined_dat_ton[joined_dat_ton['Value'] == 16265.8369]
#b = joined_dat_ton[joined_dat_ton['Value'] == 18953.1509]
#b
# -


