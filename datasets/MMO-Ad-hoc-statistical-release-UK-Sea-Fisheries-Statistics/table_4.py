# -*- coding: utf-8 -*-
# # MMO Ad hoc statistical release  UK Sea Fisheries Statistics 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

# +
#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper 
# -

tabs = { tab.name: tab for tab in scraper.distribution(latest=True).as_databaker() }
list(tabs)

# +
tab_name_expected = 'Table 4'
ref_cell_expected = 'UK total'
title_to_include = 'Activity (value and volume landed) of the UK fishing fleet by country and vessel length'
df = pd.DataFrame()

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    if len(date_string)  == 4:
        return 'year/' + date_string


# -

#Check the tab/sheet has expected name before continuing. 
if (tab_name_expected in tabs) != True:
    raise Exception(tab_name_expected + " not found. Something has changed with the naming of sheets within this dataset")
else:
    tab = tabs[tab_name_expected]
    #Checking the title of the sheet in question is what is expected.
    title_of_tab = tab.excel_ref('A1')
    title_of_tab = str(title_of_tab)
    expected_title = title_to_include #Change this as needed / dataset is updated
    if expected_title in title_of_tab:
        print('correct tab title found, ')
        try: 
            ref_cell = tab.filter(ref_cell_expected)
            print(ref_cell)
            ref_cell.assert_one()  
        except:
            raise Exception("Expected ref cell not found")
        print('ref cell "' +  ref_cell_expected + '" found. begining transformation...') 
        #Define Dimensions and transform 
        period = ref_cell.shift(1,-2).expand(RIGHT).is_not_blank() 
        country = ref_cell.expand(DOWN).is_not_blank()  #to be changed to ONS Geography Code (9 Digit code)
        vessel_length = ref_cell.shift(1,0).expand(DOWN)#.is_not_blank() #to be changed to ONS Geography Code (9 Digit code), ignoring unkown rows 
        unit = '' #Will be changed later once measure time has been defined. 
        measure_type = ref_cell.shift(1,-3).expand(RIGHT).is_not_blank()
        observations = period.fill(DOWN).is_not_blank() 
       # savepreviewhtml(period)
        dimensions = [
            HDim(period, 'Period', CLOSEST, LEFT),
            HDim(country, 'Country', CLOSEST, ABOVE),
            HDim(vessel_length, 'Vessel Length', DIRECTLY, LEFT),
            HDim(measure_type, 'Measure Type', CLOSEST, LEFT),
           # HDimConst('Vessel Length', vessel_length),
            HDimConst('Unit', unit),
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)  


df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
#df = df.replace('', np.nan, regex=True)

# +

df = df.replace({'Measure Type' : { "Value (£'000s)" : 'GBP Thousands', 'Quantity (t)' : 'Weight', 'Number of trips' : 'Count' }})
df = df.replace({'Vessel Length' : { "" : 'All'}})
df = df.replace({'Country' : { "" : 'UK total'}})
df = df.replace({'Marker' : { ".." : 'Figure less than 1'}})

f1=(df['Period'] =='Change')
df.loc[f1,'Measure Type'] = 'Percentage Change'
df.loc[f1,'Period'] = '2020.0'


def unit_type(x):
    if 'GBP Thousands' in str(x) :
        return 'GBP'
    elif 'Weight' in str(x) :
        return 'Tonnes'
    elif 'Count' in str(x) :
        return 'Trips'
    elif 'Percentage Change' in str(x) :
        return 'Percent'
df['Unit'] = df.apply(lambda row: unit_type(row['Measure Type']), axis = 1)
df['Period'] = df.apply(lambda x: x['Period'].replace('.0', ''), axis = 1)
df["Period"] = df["Period"].apply(date_time)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

tidy = df[['Period', 'Country', 'Vessel Length', 'Measure Type', 'Unit', 'Value']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = title_to_include
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

# +
######## BELOW COMMENT OUT FOR NOW ######


#from gssutils.metadata import THEME
#scraper.set_base_uri('http://gss-data.org.uk')
#scraper.set_dataset_id(f'{GROUP_ID}/{OBS_ID}')
#scraper.dataset.title = TITLE

#scraper.dataset.family = 'covid-19'
#with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#schema = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
