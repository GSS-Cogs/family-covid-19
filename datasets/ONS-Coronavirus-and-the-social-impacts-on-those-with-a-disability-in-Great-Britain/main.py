# -*- coding: utf-8 -*-
# # ONS Coronavirus and the social impacts on those with a disability in Great Britain 

from gssutils import * 
import json 

#https://www.ons.gov.uk/releases/coronavirusandthesocialimpactsonthosewithadisabilityingreatbritain
info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper 

distribution = scraper.distributions[0]

# +
datasetTitle = 'Coronavirus and the social impacts on disabled people in Great Britain'
tabs = { tab: tab for tab in distribution.as_databaker() }
tidied_sheets = []
trace = TransformTrace()
df = pd.DataFrame()

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]


# -

for tab in tabs:
        if not tab.name.lower() in ['contents', 'notes', ]:#TABS TO IGNORE
            datacube_name = "Coronavirus and the social impacts on disabled people in Great Britain"
            columns=["Period","Survey Topic","Question","Response", "Disabled Status", "Measure Type", "Unit", "Lower CI", "Upper CI", "Weighted Count", "Sample"]
            trace.start(datacube_name, tab, columns, scraper.distributions[0].downloadURL)
        
            survey_topic_cell = tab.excel_ref('A1')
            survey_topic = survey_topic_cell.is_not_blank()
            trace.Survey_Topic('Topic of Survey detailed at cell value: {}', var = cellLoc(survey_topic))
        
            period = survey_topic_cell.shift(0,1).is_not_blank()
            trace.Period('Period Range for Tab given at cell value: {}', var = cellLoc(period))
            
            disabled_status = period.shift(0,2).expand(RIGHT).is_not_blank()
            trace.Disabled_Status('Values found in range: {}', var = cellLoc(disabled_status))
            
            lower_ci_cell = tab.filter(contains_string('LCL'))
            lower_ci = lower_ci_cell.shift(0,1).expand(DOWN).is_not_blank()
        
            upper_ci_cell = tab.filter(contains_string('UCL'))    
            upper_ci = upper_ci_cell.shift(0,1).expand(DOWN).is_not_blank()
            trace.Upper_CI('Values found in range: {}', var = cellLoc(upper_ci))
            
            #Define Observations
            if right(tab.name.lstrip().rstrip().lower(), 3) in [' 19']:
                observations = tab.filter(contains_string('Mean')).shift(0,1).expand(DOWN).is_not_blank() - survey_topic.expand(DOWN)
            else:
                observations = tab.filter(contains_string('%')).shift(0,1).expand(DOWN).is_not_blank()
            
            #Sample size and Weightd Count
            if right(tab.name.lstrip().rstrip().lower(), 3) in ['e 1', 'e 5', ' 15', ' 19']:
                weighted_count = tab.filter(contains_string('Weighted')).shift(0,1).expand(DOWN).is_not_blank()
                sample = tab.filter(contains_string('Sample')).shift(0,1).expand(DOWN).is_not_blank()
            elif right(tab.name.lstrip().rstrip().lower(), 3) in ['e 2']:  
                weighted_count = tab.filter(contains_string('Weighted')).shift(1,0).expand(RIGHT).is_not_blank() 
                sample = tab.filter(contains_string('Sample')).shift(1,0).expand(RIGHT)
                lower_ci = lower_ci - sample - weighted_count
                observations = observations - sample - weighted_count
            else:
                weighted_count = tab.filter(contains_string('Weighted')).shift(1,0).expand(RIGHT).is_not_blank() 
                sample = tab.filter(contains_string('Sample')).shift(1,0).expand(RIGHT).is_not_blank()
                lower_ci = lower_ci - sample - weighted_count
                observations = observations - sample - weighted_count
            
            trace.Weighted_Count('Values found in range: {}', var = cellLoc(weighted_count))
            trace.Sample('Values found in range: {}', var = cellLoc(sample))
            trace.Lower_CI('Values found in range: {}', var = cellLoc(lower_ci))
            
            
            #Pulling out all the questions and responses from each tab
            question_and_response = survey_topic_cell.shift(0,2).expand(DOWN).is_not_blank() 
            remove_weighted = tab.filter(contains_string('Weighted'))
            remove_sample = tab.filter(contains_string('Sample'))         
            if right(tab.name.lstrip().rstrip().lower(), 3) in [' 19']:
                response = question_and_response.filter(contains_string('answered on a scale of 0 to 10'))
                question = question_and_response - question_and_response.filter(contains_string('Source')).expand(DOWN)
            else: 
                question = question_and_response - lower_ci.fill(LEFT) - remove_weighted - remove_sample
                response = question_and_response - question - remove_weighted - remove_sample
            
            trace.Response('Values found in range: {}', var = cellLoc(response))
            trace.Question('Values found in range: {}', var = cellLoc(question))
            
            unit = 'Percent'
            trace.Unit('Hardcoded value as: Percent')
        
            measure_type = 'Percentage'
            trace.Measure_Type('Hardcoded value as: Percentage')
  
            if right(tab.name.lstrip().rstrip().lower(), 3) in ['e 1', 'e 5', ' 15']:
                dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(survey_topic, 'Survey Topic', CLOSEST, ABOVE),
                    HDim(question, 'Question', CLOSEST, ABOVE),
                    HDim(response, 'Response', DIRECTLY, LEFT),
                    HDim(disabled_status, 'Disabled Status', CLOSEST, LEFT),
                    HDimConst('Measure Type', measure_type),
                    HDimConst('Unit', unit),
                    HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
                    HDim(weighted_count, 'Weighted Count', DIRECTLY, RIGHT),
                    HDim(sample, 'Sample', DIRECTLY, RIGHT),
                ]
            elif right(tab.name.lstrip().rstrip().lower(), 3) in [' 19']:
                dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(survey_topic, 'Survey Topic', CLOSEST, ABOVE),
                    HDim(question, 'Question', DIRECTLY, LEFT),
                    HDim(response, 'Response', CLOSEST, LEFT),
                    HDim(disabled_status, 'Disabled Status', CLOSEST, LEFT),
                    HDimConst('Measure Type', 'Mean'),
                    HDimConst('Unit', 'Mean'),
                    HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
                    HDim(weighted_count, 'Weighted Count', DIRECTLY, RIGHT),
                    HDim(sample, 'Sample', DIRECTLY, RIGHT),
                ]
            elif right(tab.name.lstrip().rstrip().lower(), 3) in ['e 2']:
                dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(survey_topic, 'Survey Topic', CLOSEST, ABOVE),
                    HDim(question, 'Question', CLOSEST, ABOVE),
                    HDim(response, 'Response', DIRECTLY, LEFT),
                    HDim(disabled_status, 'Disabled Status', CLOSEST, LEFT),
                    HDimConst('Measure Type', measure_type),
                    HDimConst('Unit', unit),
                    HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
                    HDim(weighted_count, 'Weighted Count', DIRECTLY, BELOW),
                    HDim(sample, 'Sample', DIRECTLY, BELOW),
                ]
            elif right(tab.name.lstrip().rstrip().lower(), 3) in ['e 3']:
                dimensions = [
                    HDim(period, 'Period', CLOSEST, ABOVE),
                    HDim(survey_topic, 'Survey Topic', CLOSEST, ABOVE),
                    HDim(question, 'Question', CLOSEST, ABOVE),
                    HDim(response, 'Response', DIRECTLY, LEFT),
                    HDim(disabled_status, 'Disabled Status', CLOSEST, LEFT),
                    HDimConst('Measure Type', measure_type),
                    HDimConst('Unit', unit),
                    HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
                    HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
                    HDim(weighted_count, 'Weighted Count', CLOSEST, RIGHT),
                    HDim(sample, 'Sample', CLOSEST, RIGHT),
                ]
            else:
                dimensions = [
                        HDim(period, 'Period', CLOSEST, ABOVE),
                        HDim(survey_topic, 'Survey Topic', CLOSEST, ABOVE),
                        HDim(question, 'Question', CLOSEST, ABOVE),
                        HDim(response, 'Response', DIRECTLY, LEFT),
                        HDim(disabled_status, 'Disabled Status', CLOSEST, LEFT),
                        HDimConst('Measure Type', measure_type),
                        HDimConst('Unit', unit),
                        HDim(lower_ci, 'Lower CI', DIRECTLY, RIGHT),
                        HDim(upper_ci, 'Upper CI', DIRECTLY, RIGHT),
                        HDim(weighted_count, 'Weighted Count', DIRECTLY, BELOW),
                        HDim(sample, 'Sample', DIRECTLY, BELOW),
            ]            
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            trace.store("combined_dataframe", tidy_sheet.topandas())
            savepreviewhtml(tidy_sheet)
        else:
            continue



# +
df = trace.combine_and_trace(datacube_name, "combined_dataframe")
df.rename(columns={'OBS': 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

df = df.replace({'Marker' : {
    '~' : 'indicates a proportion less than 0.1'}})

df['Period'] = df.apply(lambda x: x['Period'].replace('Great Britain, ', '') if 'Great Britain, ' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df['Period'].str.rstrip()


df['Survey Topic'] = df['Survey Topic'].str.split(':').str[1]
df['Survey Topic'] = df['Survey Topic'].str.lstrip()

#hacky fix... 
f1=((df['Survey Topic'] =="Impact on people's life overall") & (df['Question'] =='How worried or unworried are you about the effect that Coronavirus (COVID-19) is having on your life right now?') & (df['Sample'] ==""))
df.loc[f1,'Sample'] = '1199.0'

f2=((df['Survey Topic'] =="Impact on people's life overall") & (df['Question'] =='In which ways is Coronavirus (COVID-19) affecting your life? 2') & (df['Sample'] ==""))
df.loc[f2,'Sample'] = '1017.0'

date_inclusive =  df['Period'].iloc[0]


# -

df = df[['Survey Topic', 'Question', 'Response', 'Disabled Status', 'Value', 'Measure Type', 'Unit', 'Lower CI', 'Upper CI', 'Weighted Count', 'Sample', 'Marker']]


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)

for column in df:
    if column in ("Survey Topic","Question","Response", "Disabled Status"):
        df[column] = df[column].map(lambda x: pathify(x))

notes = """
1. For the purposes of this analysis, a person is considered to have a disability if they have a self-reported long-standing illness, condition or impairment which causes difficulty with day-to-day activities. This definition is consistent with the Equality Act 2010.

2. Respondents were able to choose more than one option. 
"""

# +
out = Path('out')
out.mkdir(exist_ok=True)

datasetTitle = 'Coronavirus and the social impacts on disabled people in Great Britain: ' + date_inclusive + ' (inclusive)'
title = pathify(datasetTitle)

import os

df.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()

df
