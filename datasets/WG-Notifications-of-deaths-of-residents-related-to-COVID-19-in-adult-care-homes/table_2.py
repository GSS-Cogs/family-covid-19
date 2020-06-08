# # WG Notifications of deaths of residents related to COVID-19 in adult care homes 

from gssutils import * 
import json 
import numpy as np

scrape = Scraper(seed="info.json")   
scrape.distributions[0].title = "Notifications of deaths of residents related to COVID-19 in adult care homes"
scrape

tabs = { tab.name: tab for tab in scrape.distributions[0].as_databaker() }
list(tabs)


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]

tab_name_expected = 'Table_2'
ref_cell_expected = 'Ambulance'
title_to_include = 'Notifications of deaths of adult care home residents with confirmed or suspected COVID-19 by location of death'
df = pd.DataFrame()
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
            print('ref cell "' +  ref_cell_expected + '" found. begining transformation...') 
        except:
            raise Exception("Expected ref cell not found")
        #Define dimensions and transform
        notification_date_range = ref_cell.shift(0,-2) # Date at end, will need to be filtered out (last 17 )
        location_of_death = ref_cell.expand(DOWN).is_not_blank()
        measure_type = 'Deaths'
        unit = 'Count'
        observations = location_of_death.fill(RIGHT).is_not_blank()
        #savepreviewhtml(observations)
        dimensions = [
            HDim(notification_date_range, 'Notification Date Range', CLOSEST, ABOVE),
            HDim(location_of_death, 'Location of Death', DIRECTLY, LEFT),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)   


df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df['Notification Date Range'] = [x.strip()[-19:] for x in df['Notification Date Range']]
df = df.replace('', np.nan, regex=True)

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Location of Death'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Notification Date Range', 'Location of Death', 'Measure Type', 'Unit', 'Value']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Notifications of Service User Deaths received from Adult Care Homes'
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# -

tidy


