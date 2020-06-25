# # NHS-D Potential COVID-19 symptoms reported through NHS Pathways and 111 online 

# +

from gssutils import *
import json
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import string
# -

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage

# +
#### Add transformation script here #### 

#scraper = Scraper(landingPage) 
#scraper.select_dataset(latest=True) 
#scraper 

# +
dataLinks = []

parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen(landingPage)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

for link in soup.find_all('a', href=True):
    if not "CCG" in link.text:continue
    dataLinks.append(link['href'])

for i in dataLinks:
    print(i)
# -

for link in dataLinks:
    if link == 'https://files.digital.nhs.uk/0D/F87186/NHS%20Pathways%20Covid-19%20data%20CCG%20mapped.csv':
        pathway_covid_data = pd.read_csv(link)
    elif link == 'https://files.digital.nhs.uk/73/5CE08B/111%20Online%20Covid-19%20data_CCG%20mapped.csv':
        online_covid_data = pd.read_csv(link)
    else:
        raise Exception("Expected File not found")

# +
#online_covid_data = pd.read_csv('111 Online Covid-19 data_CCG mapped.csv')

# +
online_covid_data = online_covid_data.dropna() 
online_covid_data = online_covid_data.drop(['CCGName', 'April20 mapped CCGCode', 'April20 mappedCCGName' ], axis=1)
online_covid_data['Measure Type'] = 'Journeys completed'
online_covid_data['Unit'] = 'Count'
online_covid_data['Site Type'] = '111 Online'

online_covid_data = online_covid_data.rename(columns={'journeydate':'Period',
                                        'gender':'Sex',
                                        'ageband' : 'Age',
                                        'CCGCode' : 'ONS Geography Code',
                                        'Total' : 'Value'})

online_covid_data = online_covid_data.replace({'Sex' : {'Male' : 'M', 'Female' : 'F', 'Unknown' : 'U'}})
online_covid_data = online_covid_data[['Period', 'Site Type', 'Sex', 'Age', 'ONS Geography Code', 'Measure Type', 'Unit', 'Value']]

online_covid_data.head()

# +
#NHS Pathways Covid-19 data CCG mapped.csv
#pathway_covid_data = pd.read_csv('NHS Pathways Covid-19 data CCG mapped.csv')

# +
pathway_covid_data = pathway_covid_data.drop(['CCGName', 'April20 mapped CCGCode', 'April20 mapped CCGName' ], axis=1)
pathway_covid_data['Measure Type'] = 'Triage'
pathway_covid_data['Unit'] = 'Count'

pathway_covid_data = pathway_covid_data.rename(columns={'Call Date':'Period',
                                        'Gender':'Sex',
                                        'AgeBand' : 'Age',
                                        'CCGCode' : 'ONS Geography Code',
                                        'TriageCount' : 'Value',
                                        'SiteType' : 'Site Type' })

pathway_covid_data = pathway_covid_data.replace({'Sex' : {'Male' : 'M', 'Female' : 'F', 'Unknown' : 'U'}})
pathway_covid_data = pathway_covid_data[['Period', 'Site Type', 'Sex', 'Age', 'ONS Geography Code', 'Measure Type', 'Unit', 'Value']]

pathway_covid_data.head()
# -

data = [online_covid_data, pathway_covid_data]
tidy = pd.concat(data)

tidy

from IPython.core.display import HTML
for col in tidy:
    if col not in ['Value']:
        tidy[col] = tidy[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(tidy[col].cat.categories) 

# +
out = Path('out')
out.mkdir(exist_ok=True)

tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)


# +
######### Commented out for now #############

#from gssutils.metadata import THEME

#with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

#trace.output()
