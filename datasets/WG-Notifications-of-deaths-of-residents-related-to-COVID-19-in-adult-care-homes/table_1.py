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

tab_name_expected = 'Table_1'
ref_cell_expected = 'Care Provided'
df = pd.DataFrame()

#Check the tab/sheet has expected name before continuing. 
if (tab_name_expected in tabs) != True:
    raise Exception("Table_1 not found. Something has changed with the naming of sheets within this dataset")
else:
    tab = tabs[tab_name_expected]
    #Checking the title of the sheet in question is what is expected.
    title_of_tab = tab.excel_ref('A1')
    title_of_tab = str(title_of_tab)
    expected_title = "Notifications of Service User Deaths received from Adult Care Homes" #Change this as needed / dataset is updated
    if expected_title in title_of_tab:
        print('correct tab title found, ')
        try: 
            ref_cell = tab.filter(ref_cell_expected)
            print(ref_cell)
            ref_cell.assert_one()
            print('ref cell "' +  ref_cell_expected + '" found. begining transformation...') 
        except:
            raise Exception("ref cell not found")
        #Define dimensions and transform. 
        notification_date_range = ref_cell.shift(1,0).expand(RIGHT).is_not_blank()
        care_provided = ref_cell.shift(0,1).expand(DOWN).is_not_blank()
        measure_type = 'Deaths'
        unit = 'Count'
        observations = notification_date_range.fill(DOWN).is_not_blank() - ref_cell.shift(0,4).expand(RIGHT).expand(DOWN)
        #savepreviewhtml(observations)
        dimensions = [
            HDim(notification_date_range, 'Notification Date Range', DIRECTLY, ABOVE),
            HDim(care_provided, 'Care Provided', DIRECTLY, LEFT),
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
    if column in ('Care Provided'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Notification Date Range', 'Care Provided', 'Measure Type', 'Unit', 'Value']]
