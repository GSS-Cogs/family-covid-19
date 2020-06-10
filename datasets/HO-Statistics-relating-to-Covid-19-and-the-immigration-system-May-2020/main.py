# # HO Statistics relating to Covid-19 and the immigration system 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper

dist = scraper.distributions[1]
tabs = (t for t in dist.as_databaker())

# +
df = pd.DataFrame()

def date_time(time_value):
    date_string = time_value.strip().split(' ')[0]
    if len(date_string)  == 4:
        return 'year/' + date_string


# -

trace = TransformTrace()
for tab in tabs:
    if tab.name == 'Air_01':
        print(tab.name)
        
        datacube_name = "HO Statistics relating to Covid-19 and the immigration system"
        columns=['Period', 'Air Arrivals', 'Measure Type', 'Unit']
        trace.start(datacube_name, tab, columns, scraper.distributions[1].downloadURL)
        
        trace.Period("Selected as non blank values below and including cell A6 and cell E6")
        period = tab.excel_ref('A6').expand(DOWN).expand(RIGHT).is_not_blank()  - tab.excel_ref('B6').expand(DOWN) - tab.excel_ref('C6').expand(DOWN) - tab.excel_ref('F6').expand(DOWN) - tab.excel_ref('G6').expand(DOWN)
        
        trace.Air_Arrivals("Selected as non blank values across row 5 excluding cells A5 and E5")     
        air_arrivals = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - tab.excel_ref('E5')
        
        trace.OBS('All non-blank values to the right of Period Values.')
        observations = period.fill(RIGHT).is_not_blank() - period.expand(DOWN)
        
        trace.Measure_Type('Hard Coded to {}', var = 'People')
        trace.Unit('Hard Coded to {}', var = 'Count')
        
        dimensions = [
            HDim(period, 'Period', DIRECTLY, LEFT),
            HDim(air_arrivals, 'Air Arrivals', DIRECTLY, ABOVE),
            HDimConst('Measure Type', 'People'),
            HDimConst('Unit', 'Count'),
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
            
tidy = df[['Period', 'Air Arrivals', 'Value', 'Measure Type', 'Unit']]
trace.Air_Arrivals("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Air Arrivals'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))
tidy
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

out = Path('out')
out.mkdir(exist_ok=True)
trace.ALL("Remove all duplicate rows from dataframe.")
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)
scraper.dataset.family = 'covid-19'

# +
######### Commented out for now #############

#from gssutils.metadata import THEME

#with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
#    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-covid-19/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

trace.output()
