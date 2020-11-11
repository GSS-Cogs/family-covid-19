#!/usr/bin/env python
# coding: utf-8
# %%
#SG-Coronavirus-Covid-19-additional-data-about-adult-care-homes-in-Scotland

# %%
from gssutils import *
import pandas as pd
import json
import string
import re


# %%

def right(s, amount):
    return s[-amount:]

def left(s, amount):
    return s[:amount]

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def decimal(s):
    try:
        float(s)
        if float(s) >= 1:
            return False
        else:
            return True
    except ValueError:
        return True

def cellCont(cell):
    return re.findall(r"'([^']*)'", str(cell))[0]

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]

def excelRange(bag):
    xvalues = []
    yvalues = []
    for cell in bag:
        coordinate = cellLoc(cell)
        xvalues.append(''.join([i for i in coordinate if not i.isdigit()]))
        yvalues.append(int(''.join([i for i in coordinate if i.isdigit()])))
    high = 0
    low = 0
    for i in xvalues:
        if col2num(i) >= high:
            high = col2num(i)
        if low == 0:
            low = col2num(i)
        elif col2num(i) < low:
            low = col2num(i)
        highx = colnum_string(high)
        lowx = colnum_string(low)
    highy = str(max(yvalues))
    lowy = str(min(yvalues))

    return '{' + lowx + lowy + '-' + highx + highy + '}'

def dicti(tabName, tabTitle, tabColumns):
    columnInfo = {}

    for i in tabColumns:
        underI = i.replace(' ', '_')
        columnInfo[i] = getattr(getattr(trace, underI), 'var')

    dicti = {'name' : tabName,
             'title' : tabTitle,
             'columns' : columnInfo}

    return dicti

def dictiComment(tabName, tabTitle, tabColumns):
    columnInfo = {}

    for i in tabColumns:
        underI = i.replace(' ', '_')
        columnInfo[i] = re.findall('"([^"]*)"', str(getattr(getattr(trace, underI), 'comments')))

    dicti = {'name' : tabName,
             'columns' : columnInfo}

    return dicti


# %%
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

info = json.load(open('info.json'))

req = Request(info["landingPage"], headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
plaintext = html.decode('utf8')
soup = BeautifulSoup(plaintext)
for a in soup.select('.no-icon'):
    if 'Coronavirus (Covid-19): Testing for COVID-19 in adult care homes in Scotland' in a.get_text():
        dataURL = "https://www.gov.scot" + a['href']

with open('info.json', 'r+') as info:
    data = json.load(info)
    data["dataURL"] = dataURL
    info.seek(0)
    json.dump(data, info, indent=4)
    info.truncate()

scraper = Scraper(seed='info.json')
scraper.distributions[0].title = "Coronavirus (Covid-19): additional data about adult care homes in Scotland"
scraper


# %%

distribution = scraper.distributions[0]
display(distribution)


# %%


trace = TransformTrace()

tidied_sheets = {}

tabs = { tab: tab for tab in distribution.as_databaker() }

datasetTitle = scraper.distributions[0].title
link = distribution.downloadURL

dictiList = []

with open('info.json') as info:
    data = info.read()

infoData = json.loads(data)

infoData['transform']['transformStage'] = {}

for tab in tabs:
    if tab.name.lower().startswith('table 1'):

        columns = ['Period','NHS Board', 'People Tested','Measure Type','Unit']
        trace.start(datasetTitle, tab, columns, link)

        remove = tab.filter(contains_string('Source:')).expand(DOWN).expand(RIGHT)

        cell = tab.filter('NHS Board')

        board = cell.fill(DOWN).is_not_blank() - remove
        trace.NHS_Board('Values found in range: {}', var = excelRange(board))

        period = cell.fill(RIGHT).is_not_blank() - remove
        trace.Period('Values found in range: {}', var = excelRange(period))

        measure = cell.shift(1, 1).expand(RIGHT).is_not_blank()

        tested = cell.shift(1, 2).expand(RIGHT).is_not_blank()
        trace.People_Tested('Values found in range: {}', var = excelRange(tested))

        trace.Measure_Type('Hard Coded as: {}', var = 'Count')

        trace.Unit('Hard Coded as: {}', var = 'Person')

        tabTitle = tab.filter(contains_string('Table '))

        dictiList.append(dicti(tab.name, cellCont(tabTitle), columns))

        observations = board.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', CLOSEST, LEFT),
                HDim(board, 'NHS Board', DIRECTLY, LEFT),
                HDim(measure, 'Measure', CLOSEST, LEFT),
                HDim(tested, 'People Tested', DIRECTLY, ABOVE), #Needs a better header
                HDimConst('Measure Type', 'Count'),
                HDimConst('Unit', 'Person')
            ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)

        trace.store(pathify(tab.name), tidy_sheet.topandas())



# %%


#infoData['transform']['transformStage'] = dictiList


# %%

all_tabs = []
postTransNotes = []

pd.set_option('display.float_format', lambda x: '%.2f' % x)

for tab in tabs:
    if tab.name.lower().startswith('table 1'):

        name = tab.name

        tableName = pathify(name)

        df = trace.combine_and_trace(datasetTitle, tableName).fillna('')

        df = df.reset_index(drop=True)

        df = df[['Period', 'NHS Board', 'Measure', 'People Tested', 'OBS', 'Measure Type', 'Unit']]
        trace.add_column('Measure')
        trace.add_column('OBS')

        postTransNotes.append(dictiComment(name, tableName, list(df.columns)))

        all_tabs.append(df)



# %%
infoData['transform']['Post Transform Changes'] = postTransNotes


# %%


notes = """
Please Note: Due to a change in the reporting cycle, there are overlaps between the tables covering 29th June - 5th July, 3rd July - 9th July and 10th July - 16th July. As such these cannot be compared directly.
15th July Based on return of 966 of Scotland's 1,080 adult care homes
22nd June Based on return of 987 of Scotland's 1,080 adult care homes
29th June Based on return of 1,006 of Scotland's 1,080 adult care homes
3rd July Based on return of 1,003 of Scotland's 1,080 adult care homes
10th July Based on return of 1,007 of Scotland's 1,080 adult care homes
17th July Based on return of 1,012 of Scotland's 1,080 adult care homes
24th July Based on return of 1,011 of Scotland's 1,080 care homes 
31st July Based on return of 1,007 of Scotland's 1,080 care homes 
7th August Based on return of 1,006 of Scotland's 1,080 care homes 
14th August Based on return of 1,006 of Scotland's 1,080 care homes 
"""

infoData['transform']['Stage One Notes'] = notes

with open('infoStageOne.json', 'w') as info:
        info.write(json.dumps(infoData, indent=4).replace('null', '"Not Applicable"'))


# %%
trace.output()


# %%
all_tabs[0]['Sector'] = 'All'

# %%
all_tabs[0] = all_tabs[0][['Period', 'NHS Board', 'Measure', 'People Tested', 'Measure Type', 'Unit', 'OBS']]

# %%
# Pull the mapping files into DataFrames
geogsHB = pd.read_csv('../../Reference/scottish-health-board-mapping.csv') 
geogsCA = pd.read_csv('../../Reference/scottish-council-areas-mapping.csv') 

# %%
all_tabs[0]['NHS Board'][all_tabs[0]['NHS Board'] == 'SCOTLAND'] = 'Scotland'

# %%
# Map the Geography codes
all_tabs[0]['NHS Board'] = all_tabs[0]['NHS Board'].map(geogsHB.set_index('Category')['Code'])

# %%
joined_dat1 = all_tabs[0]
#joined_dat1.head()

# %%
#ssl = ['¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹','¹⁰']

joined_dat1['Period'] = [x[:-2] for x in joined_dat1['Period']]
joined_dat1['Period'] = joined_dat1['Period'].str.strip()
#joined_dat1.head()

# %%
#joined_dat1['Period'].unique()

# %%
joined_dat1 = joined_dat1.rename(columns = {'OBS' : 'Value', 'Measure': 'Test Outcome'})
#joined_dat1.head(5)

# %%
joined_dat1['People Tested'] = joined_dat1['People Tested'].apply(pathify) 
joined_dat1['Test Outcome'] = joined_dat1['Test Outcome'].apply(pathify) 

# %%
#joined_dat1['Measure'].unique()

# %%
del joined_dat1['Measure Type']
del joined_dat1['Unit']

joined_dat1['Value'] = pd.to_numeric(joined_dat1['Value'], downcast='integer')

# %%
dtes = joined_dat1['Period'].str.split("-", n = 1, expand = True)
dtes[1] = dtes[1].str.strip()
dtes[0] = dtes[0].str.strip()

# Get the year from the second date and attach it to the first date!!!!!
dtes2 = dtes[1].str.split(" ", n = 2, expand = True)
dtes[2] = dtes2[2]
dtes[0] = dtes[0] + ' ' + dtes[2]
del dtes2
del dtes[2]
dtes[2] = pd.to_datetime(dtes[0])
dtes[3] = pd.to_datetime(dtes[1])

dtes[4] = (dtes[3]-dtes[2]).astype('timedelta64[D]')
# Only getting 6 days back but assuming it is 7 to represent a full week
dtes[4] = (dtes[4] + 1).astype(int).astype(str)
dtes[5] = 'gregorian-interval/'
dtes[6] = 'T00:00:00/P'
dtes[7] = 'D'
dtes[8] = (dtes[5] + dtes[2].dt.strftime('%Y-%m-%dT%H:%M:%S') + '/P' + dtes[4] + dtes[7])#.replace('/P0 ', '/P')

#dtes
joined_dat1['Period'] = dtes[8]
joined_dat1['Value'] = joined_dat1['Value'].astype(int)

# %%
# Output the data to CSV
csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat1.drop_duplicates().to_csv(out / csvName, index = False)

# %%
scraper.dataset.family = 'covid-19'
scraper.dataset.description = 'SG Coronavirus COVID-19 additional data about adult care homes in Scotland - Suspected COVID-19 Cases.\n ' + notes
scraper.dataset.comment = 'Testing for COVID-19 in adult care homes in Scotland: split by care homes with confirmed COVID-19 and without confirmed COVID-19, presented by NHS Health Board'
scraper.dataset.title = 'Testing for COVID-19 in adult care homes in Scotland'

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name)) 
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(dataset_path)

csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

# %%
scraper = Scraper(seed="info.json")   
scraper.distributions[0].title = "SG-Coronavirus-Covid-19-additional-data-about-adult-care-homes-in-Scotland"
scraper 

# %%

distribution = scraper.distributions[1]
datasetTitle = scraper.distributions[0].title
link = distribution.downloadURL

# %%
tabs = { tab: tab for tab in distribution.as_databaker() }

# %%
for tab in tabs:
    if tab.name.lower().startswith('data'):
        weeks = tab.excel_ref('C12').fill(DOWN).expand(DOWN).is_not_blank()
        death = tab.excel_ref('C12').fill(RIGHT).expand(RIGHT).is_not_blank()
        dat = tab.excel_ref('C12').fill(DOWN).fill(RIGHT).is_not_blank()

        # Set the dimensions
        Dimensions = [
            HDim(weeks,'Week', DIRECTLY, LEFT),
            HDim(death,'Cause of Death', CLOSEST, RIGHT),
            ]
        c2 = ConversionSegment(dat, Dimensions, processTIMEUNIT=True)        
        c2 = c2.topandas()


        

# %%
from datetime import datetime

c2 = c2.rename(columns={'OBS':'Value'})
c2 = c2[['Week','Cause of Death','Value']]
df = pd.DataFrame(c2['Week'].str.split(' ',1).tolist(),columns = ['Start','End'])
c2['Week'] = df['Start']
del df
c2 = c2[c2['Cause of Death'] != "Confirmed COVID-19 as % of all deaths"]
c2 = c2[c2['Cause of Death'] != "Suspected COVID-19 as % of all deaths"]
c2 = c2[c2['Cause of Death'] != "Other causes as % of all deaths"]


# %%
c2['Week'] = c2['Week'].astype(str) + '20' 
c2['Week'] =  pd.to_datetime(c2['Week'], format='%d/%m/%Y')
c2['Week'] = 'gregorian-interval/' + c2['Week'].astype(str) + 'T00:00:00/P7D'
c2['Value'] = pd.to_numeric(c2['Value'], downcast='integer')
c2.head(60)

# %%

# %%
