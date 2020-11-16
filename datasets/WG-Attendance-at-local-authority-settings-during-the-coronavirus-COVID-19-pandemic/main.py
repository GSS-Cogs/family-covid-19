#!/usr/bin/env python
# coding: utf-8

# In[10]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# # WG Attendance at local authority settings during the coronavirus  COVID-19  pandemic

from gssutils import *
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from lxml import html

info = json.load(open('info.json'))

req = Request(info["landingPage"], headers={'User-Agent': 'Mozilla/5.0'})
flat = urlopen(req).read()
plaintext = flat.decode('utf8')
tree = html.fromstring(plaintext)
link = tree.xpath('//*[@id="series--content"]/div[1]/div/div/ul/li/div/div[1]/a')[0].attrib['href']
dataReq = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
dataFlat = urlopen(dataReq).read()
dataPlaintext = dataFlat.decode('utf8')
dataTree = html.fromstring(dataPlaintext)

dataLink = dataTree.xpath('/html/body/div[2]/div/main/div/section/div[2]/div/article/section/div[4]/div/div[1]/div[3]/div/div/div/div/div/div/div/div/div[1]/h3/a')
dataURL = dataLink[0].attrib['href']

with open('info.json', 'r+') as info:
    data = json.load(info)
    data["dataURL"] = dataURL
    info.seek(0)
    json.dump(data, info, indent=4)
    info.truncate()


# In[11]:


scrape = Scraper(seed="info.json")
scrape.distributions[0].title = "Attendance at local authority settings during the coronavirus (COVID-19) pandemic"
scrape


# In[12]:


scrape.distributions = [x for x in scrape.distributions]

dist = scrape.distributions[0]
display(dist)


# In[13]:


tabs = { tab.name: tab for tab in dist.as_databaker() if tab.name.startswith('Table')}
list(tabs)


# In[14]:


tidied_sheets = {}

for name, tab in tabs.items():

    if 'Table1_Eng' in name:

        remove = tab.filter(contains_string('Source:')).expand(DOWN).expand(RIGHT)

        cell = tab.filter('Week beginning')

        week_beginning = cell.fill(DOWN).is_not_blank() - remove

        week_ending = week_beginning.shift(RIGHT)

        measurement = cell.shift(2, 0).expand(RIGHT).is_not_blank()

        observations = week_ending.fill(RIGHT).is_not_blank()

        dimensions = [
        HDim(week_beginning, 'Week Beginning', DIRECTLY, LEFT),
        HDim(week_ending, 'Week Ending', DIRECTLY, LEFT),
        HDim(measurement, 'Measurement', DIRECTLY, ABOVE),
        HDim(measurement, 'Measure Type', DIRECTLY, ABOVE),
        HDim(measurement, 'Unit', DIRECTLY, ABOVE),
        ]

        #Measurement is used for meature tpye and unit here as I'm going
        #to be using the measurement to determine each and this is the easier way

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets[name] = tidy_sheet.topandas()

tidy_sheet.topandas()


# In[15]:


formatted_tables = {}

for name in tidied_sheets:

    if name == 'Table1_Eng':

        df = tidied_sheets['Table1_Eng']

        #df['Week Ending'] = df.apply(lambda x: 'gregorian-interval/' + str(parse(x['Week Ending']).date() - timedelta(days=6)) +'T00:00:00/P7D', axis = 1)

        df = df.replace({'Measurement' : {
                'Number of LAs that provided data (a)' : 'Number of LAs that provided data',
                'Total number of pupils on roll at the LAs that provided data (b)' : 'Total number of pupils on roll at the LAs that provided data'},
                         'Measure Type' : {
                'Number of LAs that provided data (a)' : 'Local Authority',
                'Number of pupils that did attend at least one session during the week' : 'Person',
                'Number of pupils that were invited to attend at least one session during the week' : 'Person',
                'Number of schools closed' : 'School',
                'Number of schools open' : 'School',
                'Percentage of all pupils on roll that did attend at least one session during the week' : 'Percentage',
                'Percentage of pupils who were invited to attend that did attend at least one session during the week' : 'Percentage',
                'Total number of pupils on roll at the LAs that provided data (b)' : 'Person'},
                         'Unit' : {
                'Number of LAs that provided data (a)' : 'Count',
                'Number of pupils that did attend at least one session during the week' : 'Count',
                'Number of pupils that were invited to attend at least one session during the week' : 'Count',
                'Number of schools closed' : 'Count',
                'Number of schools open' : 'Count',
                'Percentage of all pupils on roll that did attend at least one session during the week' : 'Percent',
                'Percentage of pupils who were invited to attend that did attend at least one session during the week' : 'Percent',
                'Total number of pupils on roll at the LAs that provided data (b)' : 'Count'}})

        df = df.rename(columns={'OBS':'Value'})

        formatted_tables[name] = df


# In[16]:


df = pd.concat(formatted_tables.values(), ignore_index=True)

df


# In[17]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[18]:


tidy = df[['Week Beginning', 'Week Ending', 'Measurement', 'Value', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)

