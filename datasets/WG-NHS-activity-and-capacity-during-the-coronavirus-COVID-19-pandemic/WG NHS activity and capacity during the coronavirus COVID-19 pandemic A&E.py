# # WG NHS activity and capacity during the coronavirus  COVID-19  pandemic 

# A&E_Attendances  and NHS_Staff_absenses Tabs

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "NHS activity and capacity during the coronavirus (COVID-19) pandemic"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

try : 
    tab = tabs['A&E_Attendances']
    cell = tab.filter(contains_string('Aneurin Bevan'))
    cell.assert_one()
    board = cell.expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    observations = board.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDimConst('Case Count Type', 'A&E'),
                HDim(board, 'Local Health Board', DIRECTLY, ABOVE),
                HDimConst('Unit','Count'),  
                HDimConst('Measure Type','Attendances')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    new_table = c1.topandas()
    import numpy as np
    new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    new_table['Local Health Board'] = new_table['Local Health Board'].map(
        lambda x: {
            'Total attendances' : 'Total'
            }.get(x, x))
    def date_time(time_value):
        time_string = str(time_value).replace(".0", "").strip()
        time_len = len(time_string)
        if time_len == 10:       
            return 'gregorian-day/' + time_string[:10] + 'T00:00:00'
    new_table["Period"] = new_table["Period"].apply(date_time)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, new_table])

try : 
    tab = tabs['NHS_Staff_absenses']
    cell = tab.filter(contains_string('NHS staff absent in Wales due to COVID-19'))
    cell.assert_one()
    board = cell.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace() 
    date = cell.shift(-1,0).fill(DOWN).is_not_blank().is_not_whitespace()  
    case = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
    observations = board.fill(DOWN).is_not_blank().is_not_whitespace() 
    Dimensions = [
                HDim(date, 'Period',DIRECTLY,LEFT),
                HDim(case, 'Case Count Type', CLOSEST, LEFT),
                HDim(board, 'Local Health Board',DIRECTLY,ABOVE ),
                HDimConst('Unit','Percent'),  
                HDimConst('Measure Type','Percentage')

    ]  
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    table = c1.topandas()
    import numpy as np
    table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
    table['Case Count Type'] = table['Case Count Type'].map(
        lambda x: {
            ' NHS staff self-isolating in Wales' : 'NHS staff self-isolating in Wales'
            }.get(x, x))
    table['Period'] = table['Period'].map(lambda cell: cell.replace('/','-'))
    def date_time(time_value):
        date_string = time_value.strip().split(' ')[0]
        date_len = len(date_string)
        if date_len  == 10:
            return 'gregorian-day/'+ date_string[6:10]+ '-' + date_string[3:5] + '-'+ date_string[0:2] + 'T00:00/P7D'
    table["Period"] = table["Period"].apply(date_time)
except:
    print ('Sheet not found')

next_table = pd.concat([next_table, table])

next_table.fillna('All', inplace = True)

from IPython.core.display import HTML
for col in new_table:
    if col not in ['Value']:
        next_table[col] = next_table[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(next_table[col].cat.categories) 

tidy = next_table[['Period','Case Count Type', 'Local Health Board','Measure Type','Unit',  'Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'WG NHS activity and capacity during the coronavirus COVID-19 pandemic A&E.csv', index = False)
