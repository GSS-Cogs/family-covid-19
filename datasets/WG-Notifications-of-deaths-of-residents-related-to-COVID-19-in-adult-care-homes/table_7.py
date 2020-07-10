# # WG Notifications of deaths of residents related to COVID-19 in adult care homes 

from gssutils import * 
import json 
import numpy as np

if is_interactive():
    from requests import Session
    from cachecontrol import CacheControl
    from cachecontrol.caches.file_cache import FileCache
    from cachecontrol.heuristics import ExpiresAfter
    scrape = Scraper(seed="info.json",
                     session=CacheControl(Session(), cache=FileCache('.cache'), heuristic=ExpiresAfter(days=1))
    )
    dist = scrape.distribution(
        latest=True,
        title=lambda x: x.startswith('Notifications of deaths of residents related to COVID-19')
    )
    tabs = { tab.name: tab for tab in dist.as_databaker() }
list(tabs)


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]

tab_name_expected = 'Table_7'
ref_cell_expected = 'Area Code'
title_to_include = 'Number of notifications of deaths of adult care home residents involving COVID-19 (both confirmed and suspected) occurring in any location, by Local Authority and day of notification'
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
        except:
            raise Exception("Expected ref cell not found")
    
        print('ref cell "' +  ref_cell_expected + '" found. begining transformation...') 
        #Define Dimensions and transform 
        area_code = ref_cell.shift(0,1).expand(DOWN).is_not_blank()
        local_authority = ref_cell.shift(1,1).expand(DOWN).is_not_blank()
        notification_date = ref_cell.shift(2,0).expand(RIGHT).is_not_blank()
        measure_type = 'Deaths'
        unit = 'Count'
        observations = notification_date.fill(DOWN).is_not_blank()
        #savepreviewhtml(observations)
        dimensions = [
            HDim(area_code, 'Area Code', DIRECTLY, LEFT),
            HDim(local_authority, 'Local Authority', DIRECTLY, LEFT),
            HDim(notification_date, 'Notification Date', DIRECTLY, ABOVE),
            HDimConst('Measure Type', measure_type),
            HDimConst('Unit', unit),
        ]
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname=tab.name + "Preview.html")
        new_table = c1.topandas()
        df = pd.concat([df, new_table], sort=False)   


df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df = df.replace('', np.nan, regex=True)

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

for column in df:
    if column in ('Local Authority'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Area Code', 'Local Authority', 'Notification Date', 'Unit', 'Value']]

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Number of notifications of deaths of adult care home residents involving COVID-19 (both confirmed and suspected) occurring in any location, by Local Authority and day of notification'
OBS_ID = pathify(TITLE)
import os
GROUP_ID = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# -

tidy


