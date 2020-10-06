# # DWP Universal Credit declarations  claims  and advances  management information 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper

tabs = { tab.name: tab for tab in scraper.distribution(latest=True).as_databaker() }
list(tabs)


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]

def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 10:       
        return 'gregorian-day/' + time_string[:10]


# -

# List of tables:	
# Table 1	Number of households and individuals making a Universal Credit declaration
# Table 2	Number of households and individuals making a Universal Credit declaration Totals by time period
# Table 3	Number of Universal Credit Advances, by type of advance
# Table 4	Number of Universal Credit Advances Time Periods Totals by type of advance
#
# Tables 1 and 3 only transformed as per spec. Tables 2 and 4 are pulled as it is and all of them is placed in sheets_dictionary.  

# +
sheets = []
sheets_dictionary = {}
for name, tab in tabs.items():
    if 'Front' in name or 'Contents' in name or 'Notes' in name or 'Definitions' in name:
        continue
    if '2' in name:
        table2 = tab
        continue
    if '4' in name:
        table4 = tab
        continue
    measure_type = 'Advances' #or Households and Individuals, will be filtered out 
    period = tab.excel_ref('C7').expand(RIGHT).is_not_blank() 
    
    if tab.name == '3':
        period = tab.excel_ref('C8').expand(RIGHT).is_not_blank() 
        
    univeral_credit_stage = tab.excel_ref('B13:B18').is_not_blank() 
    if tab.name == '1':
        univeral_credit_stage = tab.excel_ref('B9:B10').is_not_blank() 
        
    observations = period.fill(DOWN).is_not_blank().is_not_whitespace()
    Dimensions = [
        HDim(period,'Period',DIRECTLY,ABOVE),
        HDim(univeral_credit_stage,'Universal Credit Stage',DIRECTLY,LEFT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit','Count')
    ]
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    savepreviewhtml(c1, fname=tab.name + "Preview.html")
    new_table = c1.topandas()
    sheets.append(new_table)


# Process Table 2
universal_credit_declaration = table2.excel_ref('C7:D7').is_not_blank()
period = table2.excel_ref('B13:B36').is_not_blank()

obs = table2.excel_ref('C13').expand(DOWN).expand(RIGHT).is_not_blank()
Dimensions = [
        HDim(period,'Period', DIRECTLY, LEFT),
        HDim(universal_credit_declaration, 'Universal Credit Declarations', DIRECTLY, ABOVE)
    ]
c2 = ConversionSegment(table2, Dimensions, obs)
savepreviewhtml(c2)
sheets_dictionary["2"] = c2.topandas()

# Process table 4
advance_type = table4.excel_ref('C7:F7').is_not_blank()
period = table4.excel_ref('B13:B18').is_not_blank()

obs = table4.excel_ref('C13').expand(DOWN).expand(RIGHT).is_not_blank()
Dimensions = [
        HDim(period,'Period', DIRECTLY, LEFT),
        HDim(advance_type, 'Advance Type', DIRECTLY, ABOVE)
    ]
c4 = ConversionSegment(table4, Dimensions, obs)
savepreviewhtml(c4)
sheets_dictionary["4"] = c4.topandas()


dataframe = pd.concat(sheets)
# Adding advance in front of Universal credit stage, will be removed for rows having measure type Households and Individuals later
dataframe["Universal Credit Stage"] = dataframe["Universal Credit Stage"].map(lambda x: 'Advance ' + x) 
# -


import numpy as np
dataframe.rename(columns={'OBS': 'Value'}, inplace=True)
f1=((dataframe['Universal Credit Stage'] =='Advance Households making a Universal Credit declaration') | (dataframe['Universal Credit Stage'] == 'Advance Individuals making a Universal Credit declaration'))   
dataframe.loc[f1,'Measure Type'] = 'Households and Individuals'
dataframe.loc[f1,'Universal Credit Stage'] = dataframe.loc[f1,'Universal Credit Stage'].str.lstrip("Advance ")
dataframe["Period"] = dataframe["Period"].apply(date_time)
sheets_dictionary["1 and 3"] = dataframe
dataframe

# +
scraper.dataset.family = 'covid-19'

## Adding short metadata to description
additional_metadata = """ The management information is a view of what is recorded on the administrative data and have not been quality assured and processed to the standards required to be official statistics. Moreover, they will not have been derived to the same methodology as official statistics, and therefore the MI and official statistics will not be directly comparable. 

Figures relate to Great Britain only, as such Northern Ireland is not included. Figures are rounded to the nearest 10. 
Components may not sum to total due to rounding. 
Figures fewer than 5 are supressed due to rounding to avoid disclosure required by the Data Protection Act 2018 and in accordance with principle T6 of the Code of Practice for Statistics.             

"""
scraper.dataset.description = scraper.dataset.description + additional_metadata
