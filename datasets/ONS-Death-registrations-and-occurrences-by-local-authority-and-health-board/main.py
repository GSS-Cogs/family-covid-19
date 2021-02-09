# -*- coding: utf-8 -*-
# # ONS Death registrations and occurrences by local authority and health board 

from gssutils import * 
import json 
import numpy as np
import os
from urllib.parse import urljoin

scraper = Scraper(seed="info.json")  
scraper.distributions[0].title = "ONS Death registrations and occurrences by local authority and health board"
scraper

""
#################### Registrations - All data
#################### Occurrences - All data
# Area code, Geography type, Area name, Cause of death, Week number, Place of death, Number of deaths
""
all_dat = []
cubes = Cubes("info.json")
sn = ['Registrations - All data', 'Occurrences - All data']
for s in sn:
    dat = scraper.distributions[0].as_pandas(sheet_name=s)
    headline = dat.iloc[0,0]
    print('Headline title: ' + headline)

    cols = list(dat.iloc[2,0:7])
    dat.columns = cols
    dat = dat[dat['Geography type'].notna()]
    dat = dat[dat['Geography type'] != 'Geography type']

    dat = dat.drop(dat.columns[1], axis=1)
    dat = dat.drop(dat.columns[1], axis=1)
    dat = dat.rename(columns={str(dat.columns[len(dat.columns) - 1]): 'Value', 'Week number':'Week'})
    dat['Week'] = np.where(dat['Week'] < 10, '0' + dat['Week'].astype(str), dat['Week'].astype(str))
    dat['Week'] = 'week/2020-W' + dat['Week'].astype(str)
    dat = dat[['Week','Area code','Cause of death','Place of death','Value']]
    dat['Cause of death'] = dat['Cause of death'].apply(pathify)
    dat['Place of death'] = dat['Place of death'].apply(pathify)
    
    all_dat.append(dat)

""
all_dat[0]['Death Measure'] = 'registrations'
all_dat[1]['Death Measure'] = 'occurrences'

joined_dat = pd.concat(all_dat)
joined_dat = joined_dat[['Week','Area code','Cause of death','Place of death','Death Measure','Value']]
del all_dat
scraper.dataset.comment = 'Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.'
scraper.dataset.description = scraper.dataset.comment + '\n' + headline + '\nThese figures represent death occurrences and registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release:\n https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/latest'
joined_dat.head(5)

""
cubes.add_cube(scraper, joined_dat.drop_duplicates(), "ONS-Death-registrations-and-occurrences-by-local-authority-and-health-board")
cubes.output_all()

""

