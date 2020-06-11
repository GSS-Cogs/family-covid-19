# -*- coding: utf-8 -*-
# # WG Summary data about coronavirus  COVID-19  and the response to it 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Testing data for coronavirus (COVID-19)"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

# Discretionary_Assistance_Fund  - Need to change data spec

try :
    tab = tabs['Discretionary_Assistance_Fund']
    cell = tab.filter('COVID-19 related  payments')
    cell.assert_one()
    payment = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
    measure = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
    obs = tab.filter('Total to date').expand(RIGHT).expand(DOWN)
    observations = measure.fill(DOWN).is_not_blank().is_not_whitespace() - obs
    Dimensions = [
                HDim(payment,'Finance Type',CLOSEST,LEFT),
                HDim(measure,'Measure Type',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(measure, 'Unit',DIRECTLY,ABOVE),
                HDimConst('Support Type', 'Emergency Assistance')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Measure Type'] = new_table['Measure Type'].map(lambda x: { 'Number' : 'People' , 
               'Total paid £': 'Payments'          
        }.get(x, x))
    new_table['Unit'] = new_table['Unit'].map(lambda x: { 'Number' : 'Count' , 
               'Total paid £': 'GBP'          
        }.get(x, x))
    new_table['Finance Type'] = new_table['Finance Type'].map( lambda x: { 
        'COVID-19 related Payments' : 'COVID-19 Related' , 
         'Normal EAP Payments': 'Normal EAP'          
        }.get(x, x))    
except:
    print ('Sheet not found')
    Marker = False 

next_table = pd.concat([next_table, new_table])

try :
    tab = tabs['Business_Rates_Grants']
    cell = tab.filter((contains_string('Number of business')))
    cell.assert_one()
    award = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
    obs = tab.filter('Total to date').expand(RIGHT).expand(DOWN)
    observations = award.fill(DOWN).is_not_blank().is_not_whitespace() - obs
    Dimensions = [
                HDim(award,'Finance Type',DIRECTLY,ABOVE),
                HDim(award,'Measure Type',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(award,'Unit',DIRECTLY,ABOVE), 
                HDimConst('Support Type', 'Business Rate Grants')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Measure Type'] = new_table['Measure Type'].map(lambda x: { 
        'Number of business rates grants awarded (cumulative)' : 'Cumulative Count' , 
        'Amount awarded in business rates grants (£m) (cumulative)': 'Cumulative GBP Million'          
        }.get(x, x))
    new_table['Unit'] = new_table['Unit'].map(lambda x: { 
        'Number of business rates grants awarded (cumulative)' : 'Count' , 
        'Amount awarded in business rates grants (£m) (cumulative)': 'GBP'          
        }.get(x, x))
    new_table['Finance Type'] = new_table['Finance Type'].map(lambda x: { 
        'Number of business rates grants awarded (cumulative)' : 'Awarded' , 
         'Amount awarded in business rates grants (£m) (cumulative)': 'Awarded'          
        }.get(x, x))
except:
    print ('Sheet not found')
    Marker = False 

next_table = pd.concat([next_table, new_table])

try :
    tab = tabs['DBW_loans']
    cell = tab.filter((contains_string('Number of DBW loans')))
    cell.assert_one()
    loan = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
    obs = tab.filter('Total to date').expand(RIGHT).expand(DOWN)
    observations = loan.fill(DOWN).is_not_blank().is_not_whitespace() - obs
    Dimensions = [
                HDim(loan,'Finance Type',DIRECTLY,ABOVE),
                HDim(loan,'Measure Type',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(loan,'Unit',DIRECTLY,ABOVE), 
                HDimConst('Support Type', 'Development Wales Bank Loans')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Measure Type'] = new_table['Measure Type'].map(lambda x: { 
        'Number of DBW loans approved (cumulative)' : 'Cumulative Count' , 
        'Amount approved in DBW loans (£m) (cumulative)': 'Cumulative GBP Million'          
        }.get(x, x))
    new_table['Unit'] = new_table['Unit'].map(lambda x: { 
        'Number of DBW loans approved (cumulative)' : 'Count' , 
        'Amount approved in DBW loans (£m) (cumulative)': 'GBP'          
        }.get(x, x))
    new_table['Finance Type'] = new_table['Finance Type'].map(lambda x: { 
        'Number of DBW loans approved (cumulative)' : 'Approved' , 
         'Amount approved in DBW loans (£m) (cumulative)': 'Approved'          
        }.get(x, x))
except:
    print ('Sheet not found')
    Marker = False 

next_table = pd.concat([next_table, new_table])

try :
    tab = tabs['ERF']
    cell = tab.filter((contains_string('Micro-business applications')))
    cell.assert_one()
    applications = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace() 
    obs = tab.filter('Total to date').expand(RIGHT).expand(DOWN)
    observations = applications.fill(DOWN).is_not_blank().is_not_whitespace() - obs
    Dimensions = [
                HDim(applications,'Finance Type',DIRECTLY,ABOVE),
                HDim(applications,'Measure Type',DIRECTLY,ABOVE),
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(applications,'Unit',DIRECTLY,ABOVE), 
                HDimConst('Support Type', 'Economic Resilience Fund')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Measure Type'] = new_table['Measure Type'].map(lambda x: { 
        'Micro-business applications (cumulative)' : 'Cumulative Applications',
        'Micro-business amount applied for (£m) (cumulative)' : 'Cumulative GBP Million',
        'SME applications (cumulative)' : 'Cumulative Applications',
        'SME amount applied for (£m) (cumulative)' : 'Cumulative GBP Million',
        'SME amount applied for  (£m) (cumulative)' : 'Cumulative GBP Million',
        'Total applications (cumulative)' : 'Cumulative Applications',
        'Total amount applied for (£m) (cumulative)' : 'Cumulative Applications',
        'Total amount applied for (£m)(cumulative)' : 'Cumulative GBP Million'           
        }.get(x, x))
    new_table['Unit'] = new_table['Unit'].map(lambda x: { 
        'Micro-business applications (cumulative)' : 'Count',
        'Micro-business amount applied for (£m) (cumulative)' : 'GBP',
        'SME applications (cumulative)' : 'Count',
        'SME amount applied for (£m) (cumulative)' : 'GBP',
        'SME amount applied for  (£m) (cumulative)' : 'GBP',
        'Total applications (cumulative)' : 'Count',
        'Total amount applied for (£m) (cumulative)' : 'GBP',
        'Total amount applied for (£m)(cumulative)' : 'GBP'          
        }.get(x, x))
    new_table['Finance Type'] = new_table['Finance Type'].map(lambda x: { 
        'Micro-business applications (cumulative)' : 'Micro-business',
        'Micro-business amount applied for (£m) (cumulative)' : 'Micro-business',
        'SME applications (cumulative)' : 'SME',
        'SME amount applied for (£m) (cumulative)' : 'SME',
        'SME amount applied for  (£m) (cumulative)' : 'SME',
        'Total amount applied for (£m) (cumulative)' : 'Total',
        'Total applications (cumulative)' : 'Total',
        'Total amount applied for (£m)(cumulative)' : 'Total'          
        }.get(x, x))
except:
    print ('Sheet not found')
    Marker = False 

next_table = pd.concat([next_table, new_table])

from IPython.core.display import HTML
for col in next_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 


def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
next_table["Period"] = next_table["Period"].apply(date_time)

tidy = next_table[['Period','Finance Type','Support Type', 'Unit', 'Measure Type','Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'WG COVID-19 Support Response.csv', index = False)
