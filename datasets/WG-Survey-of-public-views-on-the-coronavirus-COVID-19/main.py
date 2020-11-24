#!/usr/bin/env python
# coding: utf-8
# %%
# WG Survey of public views on the coronavirus  COVID-19

from gssutils import *
import json

# %%
scrape = Scraper(seed="info.json")
scrape.distributions[0].title = "Survey of public views on the coronavirus (COVID-19)"
scrape

# %%
tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)


# %%


tab = tabs['Data']
cell = tab.filter('Public views & outlook')
cell.assert_one()
response = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()
question = response.shift(-1,0)
survey = cell.expand(DOWN).is_not_blank().is_not_whitespace() - question
observations = date.fill(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            #HDim(response,'Average Response',DIRECTLY,LEFT),
            HDim(response,'Public Response',DIRECTLY,LEFT),
            HDim(date, 'Period',DIRECTLY,ABOVE),
            HDim(question, 'Survey Question', DIRECTLY,LEFT),
            HDim(survey,'Survey Question Category', CLOSEST,ABOVE ),
            HDimConst('Unit','percent'),
            HDimConst('Measure Type','percentage')

]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)


# %%


from IPython.core.display import HTML
for col in new_table:
    if col not in ['Value']:
        new_table[col] = new_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(new_table[col].cat.categories)


# %%


new_table['Marker'] = new_table['Marker'].map(
    lambda x: {
        #'-' : 'Statistical disclosure'
        '-' : 'Question not included in Survey'
        }.get(x, x))

def user_perc(x,y):

    #if (str(x) ==  'Statistical disclosure'):
    if (str(x) ==  'Question not included in Survey'):

        return 0
    else:
        return y

new_table['Value'] = new_table.apply(lambda row: user_perc(row['Marker'], row['Value']), axis = 1)


# %%


month_num_dict = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                  'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
                  'November': '11', 'December': '12'}

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    month_string = time_value.strip().split(' ')[-1]
    month_num = month_num_dict[month_string]
    if len(date_string)  == 1:
        date_string = '0' + date_string
    return 'gregorian-interval/2020-'+ month_num + '-' + date_string + 'T00:00:00/P3D'
new_table["Period"] = new_table["Period"].apply(date_time)


# %%


tidy = new_table[['Period','Survey Question Category','Survey Question','Public Response','Measure Type',
                  'Unit','Marker', 'Value']]


# %%

tidy['Survey Question Category'] = tidy['Survey Question Category'].apply(pathify)
tidy['Survey Question'] = tidy['Survey Question'].apply(pathify)
tidy['Public Response'] = tidy['Public Response'].apply(pathify)
tidy['Marker'] = tidy['Marker'].replace(np.NaN,'')
tidy['Marker'] = tidy['Marker'].apply(pathify)
del tidy['Measure Type']
del tidy['Unit']


# %%
tidy.head(10)

# %%
import os
from urllib.parse import urljoin

csvName = "observations.csv"
out = Path('out')
out.mkdir(exist_ok=True)
tidy[:5].drop_duplicates().to_csv(out / csvName, index = False)
tidy.drop_duplicates().to_csv(out / (csvName + '.gz'), index = False, compression='gzip')

scrape.dataset.family = 'covid-19'
scrape.dataset.comment = 'Information on public views and behaviours during the coronavirus crisis.'
scrape.dataset.description = """
These are selected results from a weekly survey tracking public views and behaviours on coronavirus. 
The study uses IPSOS Mori’s Global Advisor online platform to collect information from adults aged 16 to 74. 
The Welsh Government has funded a boost in the sample size for Wales since 19 to 21 March 2020, and the sample size 
after boosting is in the region of 500-600. It is broadly representative at population level, and the data is 
weighted to reflect the demographic profile of the adult population (in terms of gender and age) according to 
mid year population estimates. While online panels can have some limitations they do provide rapid turnaround of 
data in situations such as this.

The content of the survey changes from time to time, partly reflecting changes in the policy response to the pandemic 
and the different guidance relevant at different times. 
The column Public Response gives the (sometimes combined) response categories to the question described in the 
Survey Question column. For example if the public response to the question 'Threat posed to the Country?' is 
'Very high or high' then the given value is the proportion of respondents who regarded the threat posed to the 
country as high or very high.

Likely credibility intervals around the indicators will be in the region of +/- 4% to 5% for the Welsh boosted sample. Given the credibility intervals differences between weeks should be interpreted with some caution.
"""

dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scrape.dataset.family}/' + Path(os.getcwd()).name))
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / 'observations.csv')
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / 'observations.csv-metadata.json')

# Remove subset of data
(out / csvName).unlink()

with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())


# %%


"""
info = json.load(open('info.json'))
codelistcreation = info['transform']['codelists']
print(codelistcreation)
print("-------------------------------------------------------")
codeclass = CSVCodelists()
for cl in codelistcreation:
    if cl in tidy.columns:
        tidy[cl] = tidy[cl].str.replace("-"," ")
        tidy[cl] = tidy[cl].str.capitalize()
        codeclass.create_codelists(pd.DataFrame(tidy[cl]), 'codelists', scrape.dataset.family, Path(os.getcwd()).name.lower())
"""


# %%
scrape.dataset.description


# %%
