# # ONS Death registrations and occurrences by local authority and health board 

from gssutils import * 
import json 
import numpy as np

scraper = Scraper(seed="info.json")  
scraper.distributions[0].title = "ONS Death registrations and occurrences by local authority and health board"
scraper

dat = scraper.distributions[0].as_pandas(sheet_name='Registrations - All data')
# Area code,Geography type,Area name,Cause of death,Week number,Place of death,Number of deaths

headline = dat.iloc[0,0]
print(headline)
dat.head(4)

cols = list(dat.iloc[2,0:7])
dat.columns = cols
dat = dat[dat['Geography type'].notna()]
dat = dat[dat['Geography type'] != 'Geography type']
dat.head(10)

dat = dat.drop(dat.columns[1], axis=1)
dat = dat.drop(dat.columns[1], axis=1)
dat = dat.rename(columns={str(dat.columns[len(dat.columns) - 1]): 'Value', 'Week number':'Week'})
dat['Week'] = np.where(dat['Week'] < 10, '0' + dat['Week'].astype(str), dat['Week'].astype(str))
dat['Week'] = 'week/2020-W' + dat['Week'].astype(str)
dat = dat[['Week','Area code','Cause of death','Place of death','Value']]
dat['Cause of death'] = dat['Cause of death'].apply(pathify)
dat['Place of death'] = dat['Place of death'].apply(pathify)
dat.head()

# +
import os
from urllib.parse import urljoin

notes = headline

csvName = 'registrations-observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
dat.drop_duplicates().to_csv(out / csvName, index = False)

scraper.dataset.family = 'covid-19'
scraper.dataset.description = notes + '\n' + scraper.dataset.description
scraper.dataset.comment = 'Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.'
scraper.dataset.title = 'Death Registrations by Local Authority and Health Board'

dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scraper.dataset.family}/' + Path(os.getcwd()).name)).lower()
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)


csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')

with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

# +
#for c in dat.columns:
#    print(c)
#    print(dat[c].unique())
#    print("#############################################")

# +
#scraper.dataset.family = 'covid-19'
#codelistcreation = ['Place of death','Cause of death'] 
#df = dat
#codeclass = CSVCodelists()
#for cl in codelistcreation:
#    if cl in df.columns:
#        df[cl] = df[cl].str.replace("-"," ")
#        df[cl] = df[cl].str.capitalize()
#        codeclass.create_codelists(pd.DataFrame(df[cl]), 'codelists', scraper.dataset.family, Path(os.getcwd()).name.lower())

# +
#import io
#import pandas as pd
#from gssutils import *
#import json
#import re
#from urllib.request import Request, urlopen

#req = Response.content("https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/healthandsocialcare/causesofdeath/datasets/deathregistrationsandoccurrencesbylocalauthorityandhealthboard/2020/lahbtablesweek39.xlsx", headers={'User-Agent': 'Mozilla/5.0'})

#html = urlopen(req).read()

#toread = io.BytesIO()
#toread.write(html)  # pass your `decrypted` string as the argument here
#toread.seek(0)  # reset the pointer

#df = pd.read_excel(toread)  # now read to dataframe
