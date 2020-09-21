#!/usr/bin/env python
# coding: utf-8

# In[17]:


#!/usr/bin/env python
# coding: utf-8
# %%


# In[18]:



# # WG Summary data about coronavirus  COVID-19  and the response to it


# In[19]:



from gssutils import *
import json
import pandas as pd
from datetime import date, datetime
from bs4 import BeautifulSoup
import urllib.request

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

scrape = Scraper('https://gov.wales/summary-data-about-coronavirus-covid-19-and-response-it')
scrape.distributions[0].title = "WG Summary data about coronavirus COVID-19 and the response to it"
scrape


# In[19]:





# In[20]:


trace = TransformTrace()


# In[21]:



xls = pd.ExcelFile(scrape.distributions[0].downloadURL, engine="odf")

with pd.ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet)
    writer.save()

tabs = loadxlstabs("data.xls")
for tab in tabs:
    print(tab.name)


# In[22]:


for tab in tabs:

    if 'Food_parcels' in tab.name:

        supportResponseTitle = 'WG COVID-19 Support Response'

        columns=["Period", "Finance Type", "Support Type", "Measure Type", "Unit"]
        #trace.start(supportResponseTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('Food parcel orders received')).shift(LEFT)

        remove = tab.filter(contains_string('Notes')).expand(LEFT).expand(DOWN).expand(RIGHT)

        #trace.multi(["Period", "Support_Type"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        #trace.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        #trace.Support_Type('Selected as non-blank values right of the pivot point.')
        supportType = 'Food Parcel'

        financeType = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        #trace.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        #trace.Measure_Type('Hard Coded to {}', var = 'Parcel')
        #trace.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(financeType, 'Finance Type', DIRECTLY, ABOVE),
                HDimConst('Finance Type 2', 'N/A'),
                HDimConst('Support Type', supportType),
                HDimConst('Measure Type', 'Parcel'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        tidy_sheet1 = tidy_sheet.topandas()
        #trace.with_preview(tidy_sheet)

        #trace.store("supportResponseDataframe", tidy_sheet.topandas())

    elif 'Discretionary_Assistance_Fund' in tab.name:

        supportResponseTitle = 'WG COVID-19 Support Response'
        """
        columns=["Period", "Finance Type", "Support Type", "Measure Type", "Unit"]
        #trace.start(supportResponseTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('COVID-19 related payments')).shift(LEFT)

        remove = tab.filter(contains_string('Notes')).expand(LEFT).expand(DOWN).expand(RIGHT)

        #trace.multi(["Period", "Finance_Type"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        #trace.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        #trace.Finance_Type('Selected as non-blank values right of the pivot point.')
        financeType = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        financeType2 = cell.shift(1,1).expand(RIGHT).is_not_blank()

        #The second column ('Total Paid') doesn't seem to be mentioned in the spec so I'm assuming it was added after it was created
        #therefore I have added the column and altered the measure type/unit later in the transform
        #trace.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        #trace.Support_Type('Hard Coded to {}', var = 'Emergency Assistance')
        #trace.Measure_Type('Hard Coded to {}', var = 'Payments')
        #trace.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(financeType, 'Finance Type', CLOSEST, LEFT),
                HDim(financeType2, 'Finance Type 2', DIRECTLY, ABOVE),
                HDimConst('Support Type', 'Emergency Assistance'),
                HDimConst('Measure Type', 'Payments'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        tidy_sheet2 = tidy_sheet.topandas()
        #trace.with_preview(tidy_sheet)

        #trace.store("supportResponseDataframe", tidy_sheet.topandas())
        """
    else:
        thingJustForThing = ''
        """
        #trace.start(supportResponseTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('Source: ')).shift(0,3)

        remove = tab.filter(contains_string('Further background')).expand(LEFT).expand(DOWN).expand(RIGHT)

        #trace.multi(["Period", "Finance_Type"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        #trace.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.fill(DOWN).is_not_blank() - remove

        #trace.Finance_Type('Selected as non-blank values right of the pivot point.')
        financeType = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        if 'Business' in tab.name:
            supportType = 'Business Rate Grants'
        elif 'DBW' in tab.name:
            supportType = 'Development Wales Bank Loans'
        elif 'ERF' in tab.name:
            supportType = 'Economic Resilience Fund'
        else:
            supportType = 'ERROR Check for new tabs'

        if 'ERF' in tab.name:
            measureType = 'Cumulative Applications'
        else:
            measureType = 'Cumulative Count'

        #trace.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        #trace.Support_Type('Hard Coded switch values {} derived from Tab name.', var = supportType)
        #trace.Measure_Type('Hard Coded switch values {} derived from Tab name.', var = measureType)
        #trace.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(financeType, 'Finance Type', DIRECTLY, ABOVE),
                HDimConst('Finance Type 2', 'N/A'),
                HDimConst('Support Type', supportType),
                HDimConst('Measure Type', measureType),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        tidy_sheet3 = tidy_sheet.topandas()
        #trace.with_preview(tidy_sheet)

        #trace.store("supportResponseDataframe", tidy_sheet.topandas())
        """


# In[23]:


tidy_sheet1


# In[24]:


"""

supportResponse = trace.combine_and_trace(supportResponseTitle, "supportResponseDataframe").fillna('')

trace.add_column("Marker")
trace.Marker("Replace '~' with 'This data item is not yet available'")
trace.Finance_Type("Replace 'Food parcel orders received' with 'Orders Received'")

trace.Measure_Type("Change to 'Cumulative GBP Million' for £m values")

supportResponse['Measure Type'] = supportResponse.apply(lambda x: 'Cumulative GBP Million' if '£m' in x['Finance Type'] else x['Measure Type'], axis = 1)

trace.Finance_Type("Change 'COVID-19 related payments' to 'COVID-19 Related'")
trace.Finance_Type("Change 'Normal EAP payments' to 'Normal EAP'")
trace.Finance_Type("Amount awarded in business rates grants (£m) (cumulative)' to 'Awarded''")
trace.Finance_Type("Number of business rates grants awarded (cumulative)' to 'Awarded''")
trace.Finance_Type("Amount approved in DBW loans (£m) (cumulative)' to 'Approved''")
trace.Finance_Type("Number of DBW loans approved (cumulative)' to 'Approved''")
trace.Finance_Type("Micro-business amount applied for (£m) (cumulative)' to 'Micro-business''")
trace.Finance_Type("Micro-business applications (cumulative)' to 'Micro-business''")
trace.Finance_Type("SME amount applied for (£m) (cumulative)' to 'SME''")
trace.Finance_Type("SME applications (cumulative)' to 'SME''")
trace.Finance_Type("Total amount applied for (£m) (cumulative)' to 'Total''")
trace.Finance_Type("Total applications (cumulative)' to 'Total''")

supportResponse = supportResponse.replace({'Finance Type' : {
    'COVID-19 related payments' : 'COVID-19 Related',
    'Normal EAP payments' : 'Normal EAP',
    'Amount awarded in business rates grants (£m) (cumulative)' : 'Awarded',
    'Number of business rates grants awarded (cumulative)' : 'Awarded',
    'Amount approved in DBW loans (£m) (cumulative)' : 'Approved',
    'Number of DBW loans approved (cumulative)' : 'Approved',
    'Micro-business amount applied for (£m) (cumulative)' : 'Micro-business',
    'Micro-business applications (cumulative)' : 'Micro-business',
    'SME amount applied for (£m) (cumulative)' : 'SME',
    'SME applications (cumulative)' : 'SME',
    'Total amount applied for (£m) (cumulative)' : 'Total',
    'Total applications (cumulative)' : 'Total',
    'Attempted deliveries' : 'Attempted Deliveries',
    'Food parcel orders received' : 'Orders Received'},
                                            'DATAMARKER' : {
    '~' : 'This data item is not yet available'}})

trace.Measure_Type("Change to 'GBP Total' for Total values")

supportResponse['Measure Type'] = supportResponse.apply(lambda x: 'GBP Total' if 'Total paid' in x['Finance Type 2'] else x['Measure Type'], axis = 1)

supportResponse['Unit'] = supportResponse.apply(lambda x: 'GBP' if 'Total paid' in x['Finance Type 2'] else x['Unit'], axis = 1)
supportResponse['Unit'] = supportResponse.apply(lambda x: 'GBP' if 'GBP Million' in x['Measure Type'] else x['Unit'], axis = 1)

trace.Period("Replace 'Total to date' with Interval between first and last date in dataset.")

indexNames = supportResponse[ supportResponse['Period'] == 'Total to date' ].index
dates = supportResponse['Period'].drop(indexNames)
intervalOfOrderPeriods = days_between(max(dates), min(dates))
supportResponse['Period'] = supportResponse.apply(lambda x: 'gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Total to date' in x['Period'] else x['Period'], axis = 1)

trace.add_column("Value")
trace.Value("Rename OBS column to Value")

trace.add_column("Value")
trace.Value("Replace 0 with 'This data is not yet available'")
supportResponse['OBS'] = supportResponse.apply(lambda x: '0' if 'This data item is not yet available' in x['DATAMARKER'] else x['OBS'], axis = 1)

supportResponse.rename(columns={'OBS' : 'Value',
                                'DATAMARKER' : 'Marker'}, inplace=True)
supportResponse.head()
"""


# In[25]:


"""

from IPython.core.display import HTML
for col in supportResponse:
    if col not in ['Value']:
        supportResponse[col] = supportResponse[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(supportResponse[col].cat.categories)
"""


# In[26]:


"""

supportResponseTidy = supportResponse[['Period','Finance Type', 'Support Type', 'Value','Measure Type','Unit']]

for column in supportResponseTidy:
    if column in ('Marker', 'Finance Type', 'Support Type'):
        supportResponseTidy[column] = supportResponseTidy[column].map(lambda x: pathify(x))

"""


# In[27]:


indexNames = tidy_sheet1[tidy_sheet1['Period'] == 'Total to date' ].index
dates = tidy_sheet1['Period'].drop(indexNames)
intervalOfOrderPeriods = days_between(max(dates), min(dates))
tidy_sheet1['Period'] = tidy_sheet1.apply(lambda x: 'gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Total to date' in x['Period'] else x['Period'], axis = 1)


# In[28]:


df = tidy_sheet1[tidy_sheet1['Support Type'] == 'Food Parcel']
df.head(5)


# In[29]:


df = df.rename(columns={'Finance Type': 'Food Parcels', 'Period': 'Date', 'OBS':'Value'})
del df['Support Type']
del df['Measure Type']
del df['Unit']
del df['Finance Type 2']
df['Date'] = df.apply(lambda x: 'day/'+ x['Date'] if 'D' not in x['Date'] else x['Date'], axis = 1)
df['Food Parcels'] = df.apply(lambda x: 'Orders Received' if 'Food\xa0parcel orders received' in x['Food Parcels'] else x['Food Parcels'], axis = 1)

df['Food Parcels'] = df['Food Parcels'].apply(pathify)
df = df[['Date', 'Food Parcels', 'Value']]

for c in df.columns:
    if (c != 'Value'):
        print(c)
        print(df[c].unique())
        print("#########################")

df.head(10)


# In[30]:


import os
from urllib.parse import urljoin

notes = '''
Guidance documentation can be found here: \n
https://gov.wales/sites/default/files/statistics-and-research/2020-09/summary-data-about-coronavirus-covid-19-and-the-response-to-it-8-september-2020-423.pdf \n
Daily order received data are revised if there was a duplicate record or a box is no longer required and so some totals may be slightly lower than previously shown. \n
Further background on food parcels for the extremely vulnerable: \n
https://gov.wales/guidance-on-shielding-and-protecting-people-defined-on-medical-grounds-as-extremely-vulnerable-from-coronavirus-covid-19-html
'''
csvName = 'food_parcels_observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
df.drop_duplicates().to_csv(out / csvName, index = False)

scrape.dataset.family = 'covid-19'
scrape.dataset.description = scrape.dataset.description + '\n' + notes
scrape.dataset.comment = 'Statistics on food parcels. The data are taken from management information and are subject to change. They have not been subject to the same validation processes undertaken for official statistics releases. However, they are provided to support transparency and understanding of the response to coronavirus in Wales.'
scrape.dataset.title = 'Summary data about Coronavirus COVID-19 and the response to it - Food Parcels'

dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scrape.dataset.family}/' + Path(os.getcwd()).name)).lower()
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)


csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
# Remove subset of data
#out / csvName).unlink()
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())


# In[30]:





# In[30]:




