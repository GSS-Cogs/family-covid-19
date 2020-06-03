# # WG NHS activity and capacity during the coronavirus  COVID-19  pandemic 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "NHS activity and capacity during the coronavirus (COVID-19) pandemic"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

try :
    tab = tabs['Cases_by_LHB']
    cell = tab.filter('Local Health board')
    cell.assert_one()
    board = cell.fill(DOWN).is_not_blank().is_not_whitespace()
    date = cell.shift(0,-1).fill(RIGHT).is_not_blank().is_not_whitespace()  
    cases = cell.fill(RIGHT).is_not_blank().is_not_whitespace() 
    observations = cases.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(board,'Local Health Board',DIRECTLY,LEFT),
                HDim(date, 'Period',DIRECTLY,ABOVE),
                HDim(cases, 'Case Count Type', DIRECTLY,ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Cases')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['Cases']
    cell = tab.filter('New cases reported')
    cell.assert_one()
    case = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    observations = case.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', DIRECTLY,ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Cases')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['Deaths']
    cell = tab.filter('Newly reported deaths')
    cell.assert_one()
    case = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    observations = case.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', DIRECTLY,ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Deaths')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table = new_table[new_table['Marker'] !=  '..' ]
    new_table['Case Count Type'] = new_table['Case Count Type'].map(
        lambda x: {
            'ONS deaths by actual date of death, registered by 15 May' : 'ONS deaths by actual date of death'
            }.get(x, x))
    Marker = True
except:
    print ('Sheet not found')
    Marker = False

next_table = pd.concat([next_table, new_table])

# Add Local Health Board column with value All
# based on  source data Admission `Local Health Board` added as dimension 

try : 
    tab = tabs['Admissions']
    cell = tab.filter(contains_string('Aneurin Bevan'))
    cell.assert_one()
    board = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    observations = board.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDimConst('Case Count Type', 'Hospital Admissions'),
                HDim(board, 'Local Health Board', DIRECTLY, ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Patients')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

# Add Local Health Board column with value All
# based on  source data Hospitalisations `Local Health Board` added as dimension

try : 
    tab = tabs['Hospitalisations']
    cell = tab.filter(contains_string('Aneurin Bevan'))
    cell.assert_one()
    board = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    case = cell.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace()
    observations = case.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', DIRECTLY,ABOVE),
                HDim(board, 'Local Health Board', CLOSEST, LEFT),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Hospitalisations')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['Invasive_ventilated_beds']
    cell = tab.filter(contains_string('Aneurin Bevan'))
    cell.assert_one()
    board = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    case = cell.shift(0,2).expand(RIGHT).is_not_blank().is_not_whitespace()
    observations = case.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', DIRECTLY,ABOVE),
                HDim(board, 'Local Health Board', CLOSEST, LEFT),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Beds')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Case Count Type'] = new_table['Case Count Type'].map(
        lambda x: {
            'COVID19 Patients' : 'Critical Care Beds COVID-19 Patients Occupied', 
            'Non-COVID19 Patients' : 'Critical Care Beds Non-COVID-19 Patients Occupied',
            'Vacant' : 'Critical Spare Beds Vacant'
            }.get(x, x))
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['General_and_Acute_Beds']
    cell = tab.filter(contains_string('Aneurin Bevan'))
    cell.assert_one()
    board = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    case = cell.shift(0,2).expand(RIGHT).is_not_blank().is_not_whitespace()
    observations = case.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', DIRECTLY,ABOVE),
                HDim(board, 'Local Health Board', CLOSEST, LEFT),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Beds')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Case Count Type'] = new_table['Case Count Type'].map( lambda x : {
        'COVID19 Patients' : 'General and Acute Beds COVID-19 Patients Occupied', 
        'Non-COVID19 Patients' : 'General and Acute Beds Non-COVID-19 Patients Occupied',
            'Vacant' : 'General and Acute Beds Vacant'
    }.get(x, x))
except : 
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['Ambulance_Calls']
    cell = tab.filter(contains_string('Emergency ambulance calls'))
    cell.assert_one()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    incident = cell
    observations = cell.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(incident, 'Case Count Type', DIRECTLY,ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Incidents')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Case Count Type'] = new_table['Case Count Type'].map( lambda x : {
        'Emergency ambulance calls' : 'Ambulances Attendance'
    }.get(x, x))
except : 
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

# +
try : 
    tab = tabs['111_Calls']
    cell = tab.filter(contains_string('Answered calls'))
    cell.assert_one()
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    call = cell
    observations = cell.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(call, 'Case Count Type',DIRECTLY,ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Calls')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Case Count Type'] = new_table['Case Count Type'].map( lambda x : {
        'Answered calls or abandoned calls after 60 seconds without answer to 111 and NHS Direct' : \
        '111 or NHS Direct Answered or Abandoned Calls'
    }.get(x, x))

except : 
    print ('Sheet not found')
# -

next_table.fillna('All', inplace = True)

from IPython.core.display import HTML
for col in new_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

if Marker == True :
    next_table['Marker'] = next_table['Marker'].map(
        lambda x: {
            '~' : 'Not all tests completed'
        }.get(x, x))

    def user_perc3(x,y):
        if (str(x) ==  'Not all tests completed'): 

            return 0
        else:
            return y

    next_table['Value'] = next_table.apply(lambda row: user_perc3(row['Marker'], row['Value']), axis = 1)


def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
next_table["Period"] = next_table["Period"].apply(date_time)

list(next_table)

if Marker == True :
    tidy = next_table[['Period','Case Count Type', 'Local Health Board','Marker', 'Measure Type',
                          'Unit',  'Value']]
else :
    tidy = next_table[['Period','Case Count Type', 'Local Health Board','Measure Type','Unit',  'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'WG NHS activity and capacity during the coronavirus COVID-19 pandemic.csv', index = False)
