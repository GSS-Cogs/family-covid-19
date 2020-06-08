#!/usr/bin/env python
# coding: utf-8

# In[192]:


# # WG Summary data about coronavirus  COVID-19  and the response to it


# In[193]:


from gssutils import *
import json
import pandas as pd
from datetime import date, datetime

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[194]:


#### Add transformation script here ####


#scraper = Scraper(landingPage)
#scraper

# The URL was changed from the landing page taken from the info.json since the scraper is not made to use it.
# Could go back and edit the scraper but kinda seems like a pain in the ass considering the landing page is non-specific to the dataset.


# In[195]:


#dist = scraper.distributions[0]
#dist


# In[196]:


traceFoodParcel = TransformTrace()

traceSupportResponse = TransformTrace()


# In[197]:


dataURL = 'https://gov.wales/sites/default/files/statistics-and-research/2020-06/summary-data-about-coronavirus-covid-19-and-the-response-to-it-1-june-2020.ods'

xls = pd.ExcelFile(dataURL, engine="odf")

with pd.ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet)
    writer.save()

tabs = loadxlstabs("data.xls")
for tab in tabs:
    print(tab.name)


# In[198]:


food_parcel = []
support_response = []

for tab in tabs:

    if 'Food_parcels' in tab.name:

        foodParcelTitle ='WG COVID-19 Food Parcel Support'

        columns=["Period", "Food Parcel Status", "Measure Type", "Unit"]
        traceFoodParcel.start(foodParcelTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('Food parcel orders received')).shift(LEFT)

        remove = tab.filter(contains_string('Notes')).expand(LEFT).expand(DOWN).expand(RIGHT)

        traceFoodParcel.multi(["Period", "Food_Parcel_Status"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        traceFoodParcel.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        traceFoodParcel.Food_Parcel_Status('Selected as non-blank values right of the pivot point.')
        foodParcelStatus = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        traceFoodParcel.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        traceFoodParcel.Measure_Type('Hard Coded to {}', var = 'Parcel')
        traceFoodParcel.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(foodParcelStatus, 'Food Parcel Status', DIRECTLY, ABOVE),
                HDimConst('Measure Type', 'Parcel'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        traceFoodParcel.with_preview(tidy_sheet)

        traceFoodParcel.store("foodParcelDataframe", tidy_sheet.topandas())

    elif 'Discretionary_Assistance_Fund' in tab.name:

        supportResponseTitle = 'WG COVID-19 Support Response'

        columns=["Period", "Finance Type", "Support Type", "Measure Type", "Unit"]
        traceSupportResponse.start(supportResponseTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('COVID-19 related payments')).shift(LEFT)

        remove = tab.filter(contains_string('Notes')).expand(LEFT).expand(DOWN).expand(RIGHT)

        traceSupportResponse.multi(["Period", "Finance_Type"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        traceSupportResponse.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        traceSupportResponse.Finance_Type('Selected as non-blank values right of the pivot point.')
        financeType = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        financeType2 = cell.shift(1,1).expand(RIGHT).is_not_blank()

        #The second column ('Total Paid') doesn't seem to be mentioned in the spec so I'm assuming it was added after it was created
        #therefore I have added the column and altered the measure type/unit later in the transform
        traceSupportResponse.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        traceSupportResponse.Support_Type('Hard Coded to {}', var = 'Emergency Assistance')
        traceSupportResponse.Measure_Type('Hard Coded to {}', var = 'Payments')
        traceSupportResponse.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(financeType, 'Finance Type', CLOSEST, LEFT),
                HDim(financeType2, 'Finance Type 2', DIRECTLY, ABOVE),
                HDimConst('Support Type', 'Emergency Assistance'),
                HDimConst('Measure Type', 'Payments'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        traceSupportResponse.with_preview(tidy_sheet)

        traceSupportResponse.store("supportResponseDataframe", tidy_sheet.topandas())

    else:

        traceSupportResponse.start(supportResponseTitle, tab, columns, dataURL)

        cell = tab.filter(contains_string('Source: ')).shift(0,3)

        remove = tab.filter(contains_string('Further background')).expand(LEFT).expand(DOWN).expand(RIGHT)

        traceSupportResponse.multi(["Period", "Finance_Type"], "Pivot Point is taken as the position of left most horizontal header (allows for small variations in table location in subsequent )")

        traceSupportResponse.Period('Selected as non-blank values below and to left of pivot point.')
        period = cell.fill(DOWN).is_not_blank() - remove

        traceSupportResponse.Finance_Type('Selected as non-blank values right of the pivot point.')
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

        traceSupportResponse.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank()

        traceSupportResponse.Support_Type('Hard Coded switch values {} derived from Tab name.', var = supportType)
        traceSupportResponse.Measure_Type('Hard Coded switch values {} derived from Tab name.', var = measureType)
        traceSupportResponse.Unit('Hard Coded to {}', var = 'Count')
        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(financeType, 'Finance Type', DIRECTLY, ABOVE),
                HDimConst('Finance Type 2', 'N/A'),
                HDimConst('Support Type', supportType),
                HDimConst('Measure Type', measureType),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        traceSupportResponse.with_preview(tidy_sheet)

        traceSupportResponse.store("supportResponseDataframe", tidy_sheet.topandas())


# In[199]:


foodParcelSupport = traceFoodParcel.combine_and_trace(foodParcelTitle, "foodParcelDataframe").fillna('')

traceFoodParcel.add_column("Marker")
traceFoodParcel.Marker("Replace '~' with 'This data item is not yet available'")
traceFoodParcel.Food_Parcel_Status("Replace 'Food parcel orders received' with 'Orders Received'")

foodParcelSupport = foodParcelSupport.replace({'DATAMARKER' : {
    '~' : 'This data item is not yet available'},
                                                'Food Parcel Status' : {
    'Attempted deliveries' : 'Attempted Deliveries',
    'Food parcel orders received' : 'Orders Received'}})

traceFoodParcel.add_column("Value")
traceFoodParcel.Value("Replace 0 with 'This data is not yet available'")

foodParcelSupport['OBS'] = foodParcelSupport.apply(lambda x: '0' if 'This data item is not yet available' in x['DATAMARKER'] else x['OBS'], axis = 1)

traceFoodParcel.Period("Replace 'Total to date' with Interval between first and last date in dataset.")

indexNames = foodParcelSupport[ foodParcelSupport['Period'] == 'Total to date' ].index
dates = foodParcelSupport['Period'].drop(indexNames)
intervalOfOrderPeriods = days_between(max(dates), min(dates))
foodParcelSupport['Period'] = foodParcelSupport.apply(lambda x: 'gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Total to date' in x['Period'] else x['Period'], axis = 1)

traceFoodParcel.multi(["Marker", "Value"], "Rename columns OBS and DATAMARKER columns to Value and Marker respectively")

foodParcelSupport.rename(columns={'OBS' : 'Value',
                                  'DATAMARKER' : 'Marker'}, inplace=True)

foodParcelSupport.head()


# In[200]:


supportResponse = traceSupportResponse.combine_and_trace(supportResponseTitle, "supportResponseDataframe").fillna('')

traceSupportResponse.Measure_Type("Change to 'Cumulative GBP Million' for £m values")

supportResponse['Measure Type'] = supportResponse.apply(lambda x: 'Cumulative GBP Million' if '£m' in x['Finance Type'] else x['Measure Type'], axis = 1)

traceSupportResponse.Finance_Type("Change 'COVID-19 related payments' to 'COVID-19 Related'")
traceSupportResponse.Finance_Type("Change 'Normal EAP payments' to 'Normal EAP'")
traceSupportResponse.Finance_Type("Amount awarded in business rates grants (£m) (cumulative)' to 'Awarded''")
traceSupportResponse.Finance_Type("Number of business rates grants awarded (cumulative)' to 'Awarded''")
traceSupportResponse.Finance_Type("Amount approved in DBW loans (£m) (cumulative)' to 'Approved''")
traceSupportResponse.Finance_Type("Number of DBW loans approved (cumulative)' to 'Approved''")
traceSupportResponse.Finance_Type("Micro-business amount applied for (£m) (cumulative)' to 'Micro-business''")
traceSupportResponse.Finance_Type("Micro-business applications (cumulative)' to 'Micro-business''")
traceSupportResponse.Finance_Type("SME amount applied for (£m) (cumulative)' to 'SME''")
traceSupportResponse.Finance_Type("SME applications (cumulative)' to 'SME''")
traceSupportResponse.Finance_Type("Total amount applied for (£m) (cumulative)' to 'Total''")
traceSupportResponse.Finance_Type("Total applications (cumulative)' to 'Total''")

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
    'Total applications (cumulative)' : 'Total'}})

traceSupportResponse.Measure_Type("Change to 'GBP Total' for Total values")

supportResponse['Measure Type'] = supportResponse.apply(lambda x: 'GBP Total' if 'Total paid' in x['Finance Type 2'] else x['Measure Type'], axis = 1)

supportResponse['Unit'] = supportResponse.apply(lambda x: 'GBP' if 'Total paid' in x['Finance Type 2'] else x['Unit'], axis = 1)
supportResponse['Unit'] = supportResponse.apply(lambda x: 'GBP' if 'GBP Million' in x['Measure Type'] else x['Unit'], axis = 1)

traceSupportResponse.Period("Replace 'Total to date' with Interval between first and last date in dataset.")

indexNames = supportResponse[ supportResponse['Period'] == 'Total to date' ].index
dates = supportResponse['Period'].drop(indexNames)
intervalOfOrderPeriods = days_between(max(dates), min(dates))
supportResponse['Period'] = supportResponse.apply(lambda x: 'gregorian-interval/'+ min(dates) + 'T00:00:00/P' + str(intervalOfOrderPeriods) + 'D' if 'Total to date' in x['Period'] else x['Period'], axis = 1)

traceSupportResponse.Value("Rename OBS column to Value")

supportResponse.rename(columns={'OBS' : 'Value'}, inplace=True)

supportResponse.head()


# In[201]:



from IPython.core.display import HTML
for col in foodParcelSupport:
    if col not in ['Value']:
        foodParcelSupport[col] = foodParcelSupport[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(foodParcelSupport[col].cat.categories)

from IPython.core.display import HTML
for col in supportResponse:
    if col not in ['Value']:
        supportResponse[col] = supportResponse[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(supportResponse[col].cat.categories)


# In[202]:


foodParcelTidy = foodParcelSupport[['Period','Food Parcel Status', 'Value','Measure Type','Unit']]

for column in foodParcelTidy:
    if column in ('Marker', 'Food Parcel Status'):
        foodParcelTidy[column] = foodParcelTidy[column].map(lambda x: pathify(x))

foodParcelTidy.head(25)


# In[203]:


supportResponseTidy = supportResponse[['Period','Finance Type', 'Support Type', 'Value','Measure Type','Unit']]

for column in supportResponseTidy:
    if column in ('Marker', 'Finance Type', 'Support Type'):
        supportResponseTidy[column] = supportResponseTidy[column].map(lambda x: pathify(x))

supportResponseTidy.head(25)


# In[204]:


out = Path('out')
out.mkdir(exist_ok=True)

foodParcelTitle = pathify(foodParcelTitle)

supportResponseTitle = pathify(supportResponseTitle)

import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

foodParcelTidy.drop_duplicates().to_csv(out / f'{foodParcelTitle}.csv', index = False)

supportResponseTidy.drop_duplicates().to_csv(out / f'{supportResponseTitle}.csv', index = False)

traceFoodParcel.output()

traceSupportResponse.output()

"""
scraper.dataset.family = 'homelessness'
scraper.dataset.theme = THEME['housing-planning-local-services']
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-homelessness/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')"""

