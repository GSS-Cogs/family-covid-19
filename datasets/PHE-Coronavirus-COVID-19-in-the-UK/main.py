#!/usr/bin/env python
# coding: utf-8
# %%

# %%


# # PHE Coronavirus  COVID-19  in the UK

from gssutils import *
import pandas as pd
import json

scraper = Scraper(seed="info.json")


# %%
"""
Note that the scraper for this page doesn't currently work/exist.
Therefore to run this pipeline you will need to download the TWO csv files from https://coronavirus.data.gov.uk/
to the folder which contains main.py/main.ipynb
"""

info = json.load(open('info.json'))
etl_title = info["title"]

scraper.dataset.issued = '2020-09-17'
scraper.distributions[0].title = etl_title
scraper.distributions[0]


# %%
import csv
import requests

CSV_URL = scraper.distributions[0].downloadURL

with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
        
df = pd.DataFrame(my_list, columns=['Area name','Area code','Area type','Specimen date','Daily lab-confirmed cases','Cumulative lab-confirmed cases','Cumulative lab-confirmed cases rate'])
df = df[1:] # First row is the column names, get rid
print(df['Area type'].unique())
# Lower Tier Local Authority
# Upper Tier Local Authorities
# Nation
# Region
df = df.rename(columns={'Specimen date':'Date','Area code':'Area Code'})
# Separate out the three columns
cc1 = df[['Date','Area Code','Daily lab-confirmed cases']]
cc2 = df[['Date','Area Code','Cumulative lab-confirmed cases']]
cc3 = df[['Date','Area Code','Cumulative lab-confirmed cases rate']]
# Rename each measure colunm to Value
cc1 = cc1.rename(columns={'Daily lab-confirmed cases':'Value'})
cc2 = cc2.rename(columns={'Cumulative lab-confirmed cases':'Value'})
cc3 = cc3.rename(columns={'Cumulative lab-confirmed cases rate':'Value'})
# Set a measure type, not needed yet as we are only uploading one Measure Type
cc1['Measure Type'] = 'count'
cc2['Measure Type'] = 'cumulative'
cc3['Measure Type'] = 'rate'
#######################################################################################
# WHEN WE CAN PUBLISH WITH MORE THAN ONE MEASYRE TYPE THEN ALSO ADD CUMULATIVE DATA #
#covidCases = pd.concat([cc1,cc2,cc3])
covidCases = cc1[['Date', 'Area Code', 'Measure Type', 'Value']]
del covidCases['Measure Type']
#######################################################################################
covidCases['Date'] = 'day/' + covidCases['Date'].astype(str)
covidCases.head(10)

# %%

covidCases1 = pd.read_csv('spec_cases_data_2020.csv')

covidCases1 = covidCases1.drop(['areaName', 'areaType'], axis=1)


covidCases1 = covidCases1.rename(columns={'areaCode':'Area Code',
                                        'date':'Date'})


cc1 = covidCases1[['Date', 'Area Code', 'newCasesBySpecimenDate']]
cc1['Measure Type'] = 'count'
cc1 = cc1.rename(columns={'newCasesBySpecimenDate':'Value',})
cc2 = covidCases1[['Date', 'Area Code', 'cumCasesBySpecimenDate']]
cc2['Measure Type'] = 'cumulative'
cc2 = cc2.rename(columns={'cumCasesBySpecimenDate':'Value',})

#######################################################################################
# WHEN WE CAN PUBLISH WITH MORE THAN ONE MEASYRE TYPE THEN ALSO ADD CUMULATIVE DATA #
#covidCases = pd.concat([cc1,cc2])
covidCases1 = cc1
#######################################################################################

covidCases1['Date'] = 'day/' + covidCases1['Date'].astype(str)
covidCases1 = covidCases1[['Date', 'Area Code', 'Measure Type', 'Value']]

del covidCases1['Measure Type']

covidCases1.head(1)


# %%
print(covidCases.count())
print(covidCases1.count())
covidCases2 = pd.concat([covidCases,covidCases1])
print(covidCases2.count())
covidCases2 = covidCases2.drop_duplicates()
print(covidCases2.count())
covidCases2.head(10)

# %%
notes = """
This data includes legacy downloads for England at LTLA, UTLA and Regional levels
\n
Daily and cumulative numbers of cases
\n
Number of people with at least one lab-confirmed positive COVID-19 PCR test result.
\n
COVID-19 cases are identified by taking specimens from people and sending these specimens to laboratories around the UK for PCR swab testing. If the test is positive, this is a referred to as a lab-confirmed case. If a person has had more than one positive test they are only counted as one case.
\n
Data can be presented by specimen date (the date when the sample was taken from the person being tested) or by reporting date (the date the case was first included in the published totals). The availability of each of these time series varies by area.
\n
Up to 20th August, a time series of positive cases by specimen date was published on the Coronavirus daily statistics webpage for the UK and the four nations. This page has now been retired although the version published on August 20th remains available. This time series is not currently available in this dashboard for Northern Ireland or the UK but we are working to make this available in the near future.
\n
Cases are allocated to the person's area of residence.
\n
UK data include results from both pillar 1 and pillar 2 testing. Up to 1 July, these data were collected separately meaning that people who had tested positive via both methods were counted twice. In combining the data for pillars 1 and 2 on 2 July around 30,000 duplicates were found and removed from the data. This is why the number of cases reported reduced from 1 July to 2 July.
\n
For the four nations, initially only cases identified through pillar 1 testing were included but cases identified through pillar 2 testing (see below) have been included, from different dates, for all nations.
\n
England
Data include only pillar 1 cases until 2 July, from when pillar 2 cases are also included.
\n
Northern Ireland
Data include only pillar 1 cases until 26 June, from when pillar 2 cases are also included.
\n
Scotland
Data include only pillar 1 cases until 15 June, from when pillar 2 cases are also included. Scotland's data include a batch of cases for which specimen date was not available over a 10 day period between 15 and 25 April. These samples were assigned a specimen date in the midpoint within this range (20 April) causing the artificial spike in the chart.
\n
Wales
Data include mainly pillar 1 cases until 14 July, from when pillar 2 cases have been included. This included 842 historic pillar 2 cases that had not previously been reported in the UK total, causing an increase in the UK total.
\n
﻿Testing Pillars
\n
The government's mass testing programme includes four types of tests known as pillars:
\n
Pillar 1: NHS and PHE Testing – PCR swab testing in Public Health England (PHE) labs and NHS hospitals for those with a clinical need, and health and care workers
Pillar 2: Commercial partner testing – PCR swab testing for the wider population, as set out in government guidance - pillar 2 testing reported in this dashboard only includes tests that were processed by a lab
Pillar 3: Antibody testing – antibody serology testing to show if people have antibodies from having had COVID-19, reported from 1st June onwards
Pillar 4: Surveillance testing – antibody serology and PCR swab testing for national surveillance supported by PHE, ONS, Biobank, universities and other partners to learn more about the prevalence and spread of the virus and for other testing research purposes, for example on the accuracy and ease of use of home testing
More information on the government’s national testing strategy, and the methodology used to report numbers of tests, is available on the Department for Health and Social Care website:
\n
Coronavirus (COVID-19): scaling up testing programmes
\n
Coronavirus (COVID-19): testing data methodology
\n
More details of the processes for counting cases in the devolved administrations are available on their websites:
\n
Scottish Government coronavirus information
Public Health Wales coronavirus information
Northern Ireland Department of Health coronavirus information
Rolling averages
This website primarily presents daily data. Counts of cases, admissions, deaths, etc vary from day to day just through natural random changes, but also tend to vary throughout the week systematically, so that rates are consistently lower at weekends for example.
\n
In order to help to identify trends or patterns in the data over time, 7 day rolling averages can be calculated. These are updated daily, but even out the random variation and the weekly seasonality.
\n
Each day's observation is combined with the previous three days and the following three days, and the mean of all seven days' figures is presented.
\n
For indicators where the most recent days' data are incomplete, the final few points in the rolling average series should be ignored, as the averages will increase when data are complete.
"""

# %%
import os
from urllib.parse import urljoin

df = covidCases
csvName = 'cases_observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
df.drop_duplicates().to_csv(out / csvName, index = False)


scraper.dataset.family = 'covid-19'
scraper.dataset.description = scraper.dataset.description + notes
scraper.dataset.comment = 'Number of people with at least one lab-confirmed positive COVID-19 test result, by specimen date, by nation. Individuals tested positive more than once are only counted once, on the date of their first positive test.'
scraper.dataset.title = 'Coronavirus (Covid-19) Cases by specimen date, by Nation, England: LTLA, UTLA, Region'

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

# %%
covidCases = pd.read_csv('death_cases_data_2020.csv')

covidCases = covidCases.drop(['areaName', 'areaType'], axis=1)


covidCases = covidCases.rename(columns={'areaCode':'Area Code',
                                        'date':'Date'})


cc1 = covidCases[['Date', 'Area Code', 'newDeaths28DaysByDeathDate']]
cc1['Measure Type'] = 'count'
cc1 = cc1.rename(columns={'newDeaths28DaysByDeathDate':'Value',})
cc2 = covidCases[['Date', 'Area Code', 'cumDeaths28DaysByDeathDate']]
cc2['Measure Type'] = 'cumulative'
cc2 = cc2.rename(columns={'cumDeaths28DaysByDeathDate':'Value',})

#######################################################################################
# WHEN WE CAN PUBLISH WITH MORE THAN ONE MEASYRE TYPE THEN ALSO ADD CUMULATIVE DATA #
#covidCases = pd.concat([cc1,cc2])
covidCases = cc1
#######################################################################################

covidCases['Date'] = 'day/' + covidCases['Date'].astype(str)
covidCases = covidCases[['Date', 'Area Code', 'Measure Type', 'Value']]

del covidCases['Measure Type']

covidCases.head()


# %%
notes = """
Daily and cumulative deaths within 28 days of positive test
\n
Total number of deaths of people who had had a positive test result for COVID-19 and died within 28 days reported on or up to the date of death or reporting date (depending on availability).
\n
﻿People who died more than 28 days after their first positive test are not included, whether or not COVID-19 was the cause of death. People who died within 28 days of a positive test are included: the actual cause of death may not be COVID-19 in all cases. People who died from COVID-19 but had not been tested or had not tested positive are not included.
\n
Death data can be presented by when death occurred (date of death) or when the death was reported (date reported) and the availability of each of these time series varies by area:
\n
Deaths by date of death - each death is assigned to the date that the person died irrespective of how long it took for the death to be reported. Previously reported data are therefore continually updated
Deaths by date reported - each death is assigned to the date when it was first included in the published totals. The specific 24 hour periods reported against each date vary by nation and are defined below
Deaths are allocated to the deceased's usual area of residence.
\n
England
Data on COVID-19 associated deaths in England are produced by Public Health England (PHE) from multiple sources linked to confirmed case data. Deaths newly reported each day cover the 24 hours up to 5pm on the previous day.
\n
Deaths are only included if the deceased had had a positive test for COVID-19 and died within 28 days of the first positive test.
\n
Regional, UTLA and LTLA death counts exclude England deaths for which the exact location of residence is unknown and therefore may not sum to the England total.
\n
Full details of the methodology are available on GOV.UK.
\n
Northern Ireland
Data for Northern Ireland include all cases reported to the Public Health Agency (PHA) where the deceased had a positive test for COVID-19 and died within 28 days. PHA sources include reports by healthcare workers (eg Health and Social Care Trusts, GPs) and information from local laboratory reports. Deaths reported against each date cover the 24 hours up to 9:30am on the same day.
\n
Scotland
Data for Scotland include deaths in all settings which have been registered with National Records of Scotland (NRS) where a laboratory confirmed report of COVID-19 in the 28 days prior to death exists. Deaths reported against each date cover the 24 hours up to 9:30am on the same day.
\n
Wales
Data for Wales include reports to Public Health Wales of deaths of hospitalised patients in Welsh Hospitals or care home residents where COVID-19 has been confirmed with a positive laboratory test and the clinician suspects this was a causative factor in the death. The figures do not include individuals who may have died from COVID-19 but who were not confirmed by laboratory testing, those who died in other settings, or Welsh residents who died outside of Wales. Deaths reported each day cover the 24 hours up to 5pm on the previous day. The majority of deaths included occur within 28 days of a positive test result.
\n
Rolling averages
This website primarily presents daily data. Counts of cases, admissions, deaths, etc vary from day to day just through natural random changes, but also tend to vary throughout the week systematically, so that rates are consistently lower at weekends for example.
\n
In order to help to identify trends or patterns in the data over time, 7 day rolling averages can be calculated. These are updated daily, but even out the random variation and the weekly seasonality.
\n
Each day's observation is combined with the previous three days and the following three days, and the mean of all seven days' figures is presented.
\n
For indicators where the most recent days' data are incomplete, the final few points in the rolling average series should be ignored, as the averages will increase when data are complete.
"""

# %%
"""
import os
from urllib.parse import urljoin

covidCases
csvName = 'deaths_observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
df.drop_duplicates().to_csv(out / csvName, index = False)


scraper.dataset.family = 'covid-19'
scraper.dataset.description = scraper.dataset.description + notes
scraper.dataset.comment = 'Number of deaths of people who had had a positive test result for COVID-19 and died within 28 days of the first positive test. The actual cause of death may not be COVID-19 in all cases. People who died from COVID-19 but had not tested positive are not included and people who died from COVID-19 more than 28 days after their first positive test are not included. Data from the four nations are not directly comparable as methodologies and inclusion criteria vary.'
scraper.dataset.title = 'Coronavirus (Covid-19) Deaths within 28 days of positive test by date of death, by nation'

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
"""


# %%

# %%
