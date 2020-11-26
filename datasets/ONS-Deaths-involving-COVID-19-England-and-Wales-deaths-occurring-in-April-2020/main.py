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

# Note: This dataset has been split up into 6 cubes atm. 
# Joined Table 1 and Table 2
# Joined Tables: 5, 6a, 6b, 6c, 7a, 7b, 7c,  
# then tables 3, 4, 8 and 9 are sperately transformed.  

# +
#import glob
#all_dat = []
#py_files = [i for i in glob.glob('*.{}'.format('py'))]

#for i in py_files:
#    file = "'" + i + "'"
#    if file.startswith("'main") == True:
#        continue
#    %run $file
#    all_dat.append(tidy)
# -

# %run tables_1_2.py
tidy0 = tidy
del tidy

tidy0 = tidy0[tidy0['Measure Type'] != 'Percentage of deaths in age-group']
tidy0['Sex'][tidy0['Sex'] == 'female'] = 'F'
tidy0['Sex'][tidy0['Sex'] == 'male'] = 'M'
tidy0['Sex'][tidy0['Sex'] == 'persons'] = 'T'
tidy0['Country'][tidy0['Country'] == 'england-and-wales'] = 'K04000001'
tidy0['Country'][tidy0['Country'] == 'england'] = 'E92000001'
tidy0['Country'][tidy0['Country'] == 'wales'] = 'W92000004'
tidy0['Age Group'][tidy0['Age Group'] == 'All ages'] = 'all'
tidy0['Age Group'][tidy0['Age Group'].str.strip() == '<1'] = 'less-than-1'
tidy0['Age Group'][tidy0['Age Group'].str.strip() == '90+'] = '90plus'
tidy0['Age Group'] = tidy0['Age Group'].apply(pathify)

del tidy0['Measure Type']
del tidy0['Unit']
del tidy0['Cause of death groups']

tidy0 = tidy0[['Period','ICD 10 Codes','Age Group','Sex','Country','Value']]
tidy0.tail(5)

# %run table_4.py
tidy1 = tidy
del tidy

del tidy1['Measure Type']
del tidy1['Unit']

d1 = tidy1[['Period','Value']]
d1['ICD 10 Codes'] = 'U07.1-U07.2'
d2 = tidy1[['Period','All causes 2020']]
d2['ICD 10 Codes'] = 'all'
d2 = d2.rename(columns={'All causes 2020':'Value'})
d3 = tidy1[['Period','Five year average']]
d3['ICD 10 Codes'] = 'all-causes-five-year-average'
d3 = d3.rename(columns={'Five year average':'Value'})
tidy1 = pd.concat([d1,d2,d3])
tidy1['Age Group'] = 'all'
tidy1['Sex'] = 'T'
tidy1['Country'] = 'K04000001'
tidy1['Period'] = 'day/' + tidy1['Period'].astype(str)
tidy1 = tidy1[['Period','ICD 10 Codes','Age Group','Sex','Country','Value']]

tidy1.head(5)

joined_dat = pd.concat([tidy0,tidy1])
del tidy0
del tidy1
joined_dat = joined_dat.rename(columns={'ICD 10 Codes':'Cause of Death'})

joined_dat['Sex'][joined_dat['Sex'] == 'all'] = 'T'
joined_dat['Cause of Death'] = joined_dat['Cause of Death'].str.strip()
joined_dat['Cause of Death'] = joined_dat['Cause of Death'].apply(pathify)
joined_dat['Age Group'] = joined_dat['Age Group'].apply(pathify)
joined_dat['Value'] = pd.to_numeric(joined_dat['Value'], downcast='integer')

# +
import os
from urllib.parse import urljoin

notes = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853104/sub-national-methodology-guidance.pdf'

csvName = 'covid19_deaths_observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
# Output a smaller temp csv fie for the CSVWMapping class, which uses it to create the metadata.json file
joined_dat.drop_duplicates().to_csv(out / csvName, index = False)
joined_dat.drop_duplicates().to_csv(out / (csvName + '.gz'), index = False, compression='gzip')

scraper.dataset.family = 'covid-19'
scraper.dataset.description = scraper.dataset.description + '\nPublication that uses this data: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/bulletins/deathsinvolvingcovid19englandandwales/latest'
scraper.dataset.comment = 'Number of deaths registered each month in England and Wales, including deaths involving the coronavirus (COVID-19), by age, sex and country. THis dataset is based on the date a death occured rather then when a death was registered.'
scraper.dataset.title = 'Deaths involving COVID-19, England and Wales - by Age, Sex and Leading cause'

dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scraper.dataset.family}/' + Path(os.getcwd()).name)).lower() + 'dateofdeathcount'
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)

csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')

with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

testing = False
if testing:
    for c in joined_dat.columns:
        if c not in 'Value':
            print(c)
            print(joined_dat[c].unique())
            print("----------------------------------------------")



# +
#codelistcreation = ['Cause of Death'] 
#df = joined_dat
#codeclass = CSVCodelists()
#for cl in codelistcreation:
#    if cl in df.columns:
#        df[cl] = df[cl].str.replace("-"," ")
#        df[cl] = df[cl].str.capitalize()
#        codeclass.create_codelists(pd.DataFrame(df[cl]), 'codelists', scraper.dataset.family, Path(os.getcwd()).name.lower())
# -


