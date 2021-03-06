# # HO Statistics relating to Covid-19 and the immigration system 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper

scraper.select_dataset(title=lambda t: 'Statistics relating to Covid-19 and the immigration system' in t)
scraper

dist = scraper.distribution(mediaType = ODS)
tabs = {t.name: t for t in dist.as_databaker()}
tabs.keys()

# +
df = pd.DataFrame()

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    if len(date_string)  == 4:
        return 'year/' + date_string


# +
trace = TransformTrace()
tab = next(t for t in tabs.values() if t.name.startswith('Air'))
print(tab.name)

datacube_name = "HO Statistics relating to Covid-19 and the immigration system"
columns=['Period', 'Air Arrivals']
trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)

trace.Period("Selected as non blank values below and including cell A6 and cell E6")
period = tab.excel_ref('A6').expand(DOWN).expand(RIGHT).is_not_blank()  - tab.excel_ref('B6').expand(DOWN) - tab.excel_ref('C6').expand(DOWN) - tab.excel_ref('F6').expand(DOWN) - tab.excel_ref('G6').expand(DOWN)

trace.Air_Arrivals("Selected as non blank values across row 5 excluding cells A5 and E5")     
air_arrivals = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('E5')

trace.OBS('All non-blank values to the right of Period Values.')
observations = period.fill(RIGHT).is_not_blank() - period.expand(DOWN)

dimensions = [
    HDim(period, 'Period', DIRECTLY, LEFT),
    HDim(air_arrivals, 'Air Arrivals', DIRECTLY, ABOVE),
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)

trace.store("combined_dataframe", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
trace.add_column("Marker")
trace.add_column("Value")
trace.multi(["Marker", "Value"], "Rename databaker columns OBS and DATAMARKER columns to Value and Marker respectively")
df.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)

trace.Marker("Replace 'n/a' with 'not applicable'")
df['Marker'].replace('n/a', 'not applicable', inplace=True)

trace.Air_Arrivals("Replace 'of which:\nBritish nationals' with 'of which British nationals'")
df['Air Arrivals'].replace('of which:\nBritish nationals', 'of which British nationals', inplace=True)

trace.Period('Removing n/a values')
df = df[df['Period'] != 'n/a']
            
tidy = df[['Period', 'Air Arrivals', 'Value']]
trace.Air_Arrivals("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Air Arrivals'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
tidy['Value'] = tidy['Value'].astype(int)
tidy
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

# Output Tidy data

out = Path('out')
out.mkdir(exist_ok=True)
trace.ALL("Remove all duplicate rows from dataframe.")
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)
scraper.dataset.family = 'covid-19'

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

# +
scraper.dataset.family = 'covid-19'
scraper.dataset.title = 'Statistics relating to Covid-19 and the immigration system'
scraper.dataset.comment = 'A statistical report showing the impact of Covid-19 on the immigration system.'

import os
from urllib.parse import urljoin
dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / 'observations.csv')
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / 'observations.csv-metadata.json')
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

trace.output()
