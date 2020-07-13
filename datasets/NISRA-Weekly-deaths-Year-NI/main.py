# -*- coding: utf-8 -*-
# # NISRA Weekly deaths,  Year   NI 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Weekly deaths, 2020 (NI)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

# +
import glob

py_files = [i for i in glob.glob('*.{}'.format('py'))]
py_files.sort()
all_dat = []

for i in py_files:
    file = "'" + i + "'"
    if file.startswith("'main") == True:
        continue
    %run $file
    all_dat.append(tidy)
    del tidy
# -

print('Date range from Table_02 script: ' + str(date_range) + ' Days')
print('Minimum date from Table_02 script: ' + str(min_date))
date_range_str = 'gregorian-interval/' + str(min_date).replace(' ','T') + '/P' + str(date_range) + 'D'
print('Formatted date range string: ' + date_range_str)

sexMap = pd.read_csv('../../Reference/sex-mapping.csv') 
niMap = pd.read_csv('../../Reference/northern-ireland-lgd-mapping.csv')

# Sort out Table_01
all_dat[0]['Registered Death Type'] = all_dat[0]['Registered Death Type'].str.replace('-in-week-2020p','')
all_dat[0]['Registered Death Type'] = all_dat[0]['Registered Death Type'].str.replace('2019p','2019')
all_dat[0]['Registered Death Type'] = all_dat[0]['Registered Death Type'].str.replace('193','19')
all_dat[0]['Registered Death Type'] = all_dat[0]['Registered Death Type'].str.replace('respiratory2','respiratory')
all_dat[0].insert(3,'Gender', 'total')
all_dat[0].insert(3,'Age', 'All')
all_dat[0].insert(3,'Local Government District', 'total')
all_dat[0].insert(3,'Location of Death', 'all')
del all_dat[0]['Registration Week']

# +
#ll_dat[1].head(5)
# -

all_dat[1]['Period'] = all_dat[1]['Period'].replace('year/2020',date_range_str)
all_dat[1]['Gender'] = all_dat[1]['Gender'].replace('total-registered-deaths','total')
all_dat[1].insert(3,'Registered Death Type', 'total-number-of-deaths-registered')
all_dat[1].insert(3,'Local Government District', 'total')
all_dat[1].insert(3,'Location of Death', 'all')
del all_dat[1]['Week Number']


all_dat[2].insert(3,'Gender', 'total')
all_dat[2].insert(3,'Age', 'All')
all_dat[2].insert(3,'Registered Death Type', 'total-number-of-deaths-registered')
all_dat[2].insert(3,'Location of Death', 'all')
del all_dat[2]['Registration Week']

# +
#all_dat[2].head(5)
# -

all_dat[3]['Period'] = all_dat[3]['Period'].replace('year/2020',date_range_str)
all_dat[3]['Gender'] = all_dat[3]['Gender'].replace('total-registered-deaths','total')
all_dat[3].insert(3,'Registered Death Type', 'covid-19-registered-deaths')
all_dat[3].insert(3,'Local Government District', 'total')
all_dat[3].insert(3,'Location of Death', 'all')
del all_dat[3]['Week Number']

# +
#all_dat[3].head(5)
# -

all_dat[4].insert(3,'Gender', 'total')
all_dat[4].insert(3,'Age', 'All')
all_dat[4].insert(3,'Registered Death Type', 'covid-19-registered-deaths')
all_dat[4].insert(3,'Location of Death', 'all')
del all_dat[4]['Registration Week']

# +
#all_dat[4].head(5)
# -

all_dat[5] = all_dat[5].rename(columns={'Place of Death': 'Location of Death'})
all_dat[5]['Location of Death'] = all_dat[5]['Location of Death'].replace('care-home3','care-home')
all_dat[5]['Location of Death'] = all_dat[5]['Location of Death'].replace('other4','other')
all_dat[5].insert(3,'Gender', 'total')
all_dat[5].insert(3,'Age', 'All')
all_dat[5].insert(3,'Local Government District', 'total')
all_dat[5].insert(3,'Registered Death Type', 'covid-19-registered-deaths')
del all_dat[5]['Week of Death']

# +
#all_dat[5].head(5)
# -

all_dat[6].insert(3,'Gender', 'total')
all_dat[6].insert(3,'Age', 'All')
all_dat[6].insert(3,'Registered Death Type', 'covid-19-registered-deaths')
all_dat[6].insert(3,'Location of Death', 'all')
del all_dat[6]['Week of Death']

# +
#all_dat[6].head(60)
# -

joined_dat = pd.concat([all_dat[0], all_dat[1], all_dat[2], all_dat[3], all_dat[4], all_dat[5], all_dat[6]])

# +
#print(str(all_dat[0].count()))
#print(str(all_dat[1].count()))
#print(str(all_dat[2].count()))
#print(str(all_dat[3].count()))
#print(str(all_dat[4].count()))
#print(str(all_dat[5].count()))
#print(str(all_dat[6].count()))
#print(str(joined_dat.count()))

# +
#test_dat = joined_dat
# -

# Sex Mapping
joined_dat = joined_dat.rename(columns={'Gender': 'Sex'})
joined_dat['Sex'] = joined_dat['Sex'].str.strip()
joined_dat['Sex'] = joined_dat['Sex'].map(sexMap.set_index('Category')['Code'])

# Geography code Mapping
joined_dat['Local Government District'] = joined_dat['Local Government District'].str.strip()
joined_dat['Local Government District'] = joined_dat['Local Government District'].map(niMap.set_index('Category')['Code'])

joined_dat = joined_dat[['Period', 'Local Government District','Registered Death Type','Location of Death','Age','Sex','Measure Type','Unit','Marker','Value']]

# Hopefully all NaN values have been accounted for in the Marker column
joined_dat['Value'] = joined_dat['Value'].replace(np.nan,0)

joined_dat['Age'] = joined_dat['Age'].replace('<7 days','less than 7 Days')
joined_dat['Age'] = joined_dat['Age'].replace('>=7 days and < 1 year','more than equal to 7 days and less than 1 year')
joined_dat['Age'] = joined_dat['Age'].replace('85+','85 plus')
joined_dat['Age'] = joined_dat['Age'].apply(pathify)

#joined_dat['Age'] - joined_dat['Age'].apply(pathify)
joined_dat['Age'].unique()

# Output the data to CSV
csvName = 'registered-deaths-observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat.drop_duplicates().to_csv(out / csvName, index = False)

notes = """
P Weekly published data are provisional.
1 This data is based on registrations of deaths, not occurrences. The majority of deaths are registered within five days in Northern Ireland.
2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
3Includes deaths in care homes only. Care home residents who have died in a different location will be counted elsewhere in this table.
4 The 'Other' category includes deaths at a residential address which was not the usual address of the deceased and all other places.
"""

# +
scrape.dataset.family = 'covid-19'
scrape.dataset.description = 'NISRA Registered Deaths including COVID-19.\n' + notes

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / f'{csvName}.csv-metadata.json')
with open(out / f'{csvName}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())
# -
del joined_dat
del all_dat[7]['Week of Death']
del all_dat[7]['Covid-19 Deaths']
all_dat[7].insert(3,'Location of Death', 'all')

# +
#all_dat[7].head(5)
# -


all_dat[8]['Place of Death'] = all_dat[8]['Place of Death'].replace('other3','other')
del all_dat[8]['Week of Death']
all_dat[8] = all_dat[8].rename(columns={'Place of Death': 'Location of Death'})

# +
#all_dat[8].head(5)
# -

all_dat[9]['Place of Death'] = all_dat[9]['Place of Death'].replace('care-home3a','care-home')
all_dat[9]['Place of Death'] = all_dat[9]['Place of Death'].replace('hospital3b','hospital')
all_dat[9]['Place of Death'] = all_dat[9]['Place of Death'].replace('-of-all-covid-19-hospital-deaths','hospital')
all_dat[9]['Place of Death'] = all_dat[9]['Place of Death'].replace('-of-all-covid-19-deaths','all')
all_dat[9] = all_dat[9].rename(columns={'Place of Death': 'Location of Death'})
del all_dat[9]['Week Ending']

# +
#all_dat[9].head(5)
# -

all_dat[10]['Place of Death'] = all_dat[10]['Place of Death'].replace('care-home3','care-home')
all_dat[10]['Place of Death'] = all_dat[10]['Place of Death'].replace('other4','other')
all_dat[10]['Place of Death'] = all_dat[10]['Place of Death'].replace('cumulative-total','all')
all_dat[10] = all_dat[10].rename(columns={'Place of Death': 'Location of Death'})

# +
#all_dat[10].head(10)

# +
#print(all_dat[7].columns)
#print(all_dat[8].columns)
#print(all_dat[9].columns)
#print(all_dat[10].columns)
# -

joined_dat = pd.concat([all_dat[7], all_dat[8], all_dat[9], all_dat[10]])

# +
#joined_dat.head(10)
# -

# Hopefully all NaN values have been accounted for in the Marker column
joined_dat['Value'] = joined_dat['Value'].replace(np.nan,0)

joined_dat = joined_dat[['Period','Location of Death','Measure Type','Unit','Marker','Value']]

notes = """
P Weekly published data are provisional.
1 This data is based on the actual date of death, from those deaths registered by GRO up to 1st July 2020. All data in this table are subject to change, as some deaths will have occurred but haven’t been registered yet.  The first covid-19 death in Northern Ireland occurred on 18th March 2020.
2 COVID-19 deaths include any death where Coronavirus or COVID-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
3Includes deaths in care homes only. Care home residents who have died in a different location will be counted elsewhere in this table.
4 The 'Other' category includes deaths at a residential address which was not the usual address of the deceased and all other places.
"""

# Output the data to CSV
csvName = 'covid-19-death-occurrences-observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat.drop_duplicates().to_csv(out / csvName, index = False)

# +
scrape.dataset.family = 'covid-19'
scrape.dataset.description = 'NISRA COVID-19 Death Occurrences by Date and Location.\n ' + notes

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / f'{csvName}.csv-metadata.json')
with open(out / f'{csvName}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())
# -






