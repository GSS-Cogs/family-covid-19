# # DfE Coronavirus  COVID-19   attendance in education and early years settings 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
dist = scraper.distributions[1]
dist

tabs = { tab.name: tab for tab in dist.as_databaker() }
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
        return 'gregorian-instant/' + time_string[:10] + 'T00:00:00'
    
df = pd.DataFrame()
# -



for name, tab in tabs.items():
    if 'Index' in name or 'Table 2' in name:
        continue
    period = tab.excel_ref('A4').expand(DOWN).is_not_blank()
    attendance_in_education = tab.excel_ref('C3').expand(RIGHT).is_not_blank() - tab.excel_ref('L3').expand(RIGHT)
    marker = tab.excel_ref('L4').expand(DOWN)
    measure_type = 'People' #People or Percentage, will be filtered. 
    unit = 'Count' #Count or Percent, will be filtered. 
    observations = attendance_in_education.fill(DOWN).is_not_blank()
    Dimensions = [
        HDim(period,'Period',DIRECTLY,LEFT),
        HDim(attendance_in_education,'Attendance in Education Setting',DIRECTLY,ABOVE),
        HDim(marker,'DATAMARKER',DIRECTLY,RIGHT),
        HDimConst('Measure Type', measure_type),
        HDimConst('Unit', unit)
    ]
    c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
    savepreviewhtml(c1, fname=tab.name + "Preview.html")
    new_table = c1.topandas()
    df = pd.concat([df, new_table], sort=False)

# +
import numpy as np
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

f1=((df['Attendance in Education Setting'] =='Response rate') | (df['Attendance in Education Setting'] == 'Proportion of settings open') | (df['Attendance in Education Setting'] == 'Proportion of children attending'))   
df.loc[f1,'Measure Type'] = 'Percentage'

f2=((df['Measure Type'] =='Percentage'))
df.loc[f2,'Unit'] = 'Percent'

df = df.replace({'Attendance in Education Setting' : {'Children of critical workers attending3' : 'Children of critical workers attending', 
                                               'Vulnerable children attending3' : 'Vulnerable children attending', 
                                               }})
df = df.replace({'Marker' : {'Changes to methodology - see footnote 4' : 'Figures from Friday 27 March relate to data as at 4pm on each day, prior to this figures related to data as at 6pm. Negligible changes to the estimates were seen between 4pm and 6pm.',
                             'See footnote 5' : 'The response rate for Friday 1 May was only 14% due to technical issues with DfE sign-in, the online system used by educational establishments to submit attendance data. This may have affected the accuracy of the figures. A lower response rate makes the methodology used to account for non-response slightly less reliable.',
                             'See footnote 6' : 'The response rates for Wednesday 13 May and Friday 15 May were impacted slightly due to technical issues which made it more difficult for some schools to complete the survey. A lower response rate makes the methodology used to account for non-response slightly less reliable.'
                            }})
df = df.replace('', np.nan, regex=True)
# -

from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories) 

df["Period"] = df["Period"].apply(date_time)
df['Value'] = df['Value'].round(decimals = 2)
for column in df:
    if column in ('Attendance in Education Setting'):
        df[column] = df[column].str.lstrip()
        df[column] = df[column].map(lambda x: pathify(x))

tidy = df[['Period', 'Attendance in Education Setting','Marker', 'Measure Type', 'Unit','Value']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)

# +
scraper.dataset.family = 'covid-19'

## Adding short metadata to description
additional_metadata = """ The following education settings are included: academies (including free schools and studio schools), local authority maintained schools (including local authority nursery schools), independent schools, non-maintained special schools, alternative provision, university technical colleges, FE colleges and sixth form colleges, and special post-16 institutions/specialist colleges. 

All figures are adjusted for non-response. This methodology was adjusted from Friday 27 March.

Settings are asked to provide a count of the number of children of critical workers and the number of vulnerable children. Some children are classified as both a child of a critical worker and a vulnerable child. Some settings have been counting these pupils as children of critical workers, but not in the count of vulnerable children. Therefore, the number of vulnerable children is an under-estimate. We estimate the true figure is up to 5% higher.
"""
scraper.dataset.description = scraper.dataset.description + additional_metadata

#from gssutils.metadata import THEME
#with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    #metadata.write(scraper.generate_trig())
# -

tidy


