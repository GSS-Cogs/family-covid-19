# # ONS Online price changes for high-demand products 

# +
from gssutils import * 
import json
import string
import warnings
import pandas as pd
import json
import numpy as np

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def cellLoc(cell):
    return right(str(cell), len(str(cell)) - 2).split(" ", 1)[0]

def cellCont(cell):
    return re.findall(r"'([^']*)'", cell)[0]

def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

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

month_look_up = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
                  'Jul':'07','Aug':'08','Sep':'09', 'Oct':'10','Nov':'11', 'Dec':'12'}

def date_time (date):
    if len(date)  == 10:
        return 'gregorian-interval/' + date + 'T00:00:00/P7D'
    elif len(date) == 6:
        month = month_look_up[right(date,3)]
        return 'gregorian-interval/2020-' + month + '-' + left(date,2) + 'T00:00:00/P7D'
    else:
        return date



# -

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage)  
distribution = scraper.distributions[0]

datasetTitle = 'Online price changes for high-demand products'
tabs = { tab: tab for tab in distribution.as_databaker() }
trace = TransformTrace()
df = pd.DataFrame()

# +
tab = next(t for t in tabs.values() if t.name.startswith('Online Price Change of HDP'))

columns=["Week", "Date", "Products", 'Marker', "Measure Type", "Unit"]
trace.start(datasetTitle, tab, columns, scraper.distributions[0].downloadURL)

remove_perentage_data = tab.filter(contains_string('percentage change weekly')).expand(RIGHT).expand(DOWN)

week = tab.filter(contains_string('Antibacterial hand wipes')).shift(-2,1).expand(DOWN).is_not_blank() - remove_perentage_data
trace.Week('Week date given at cell range: {}', var = excelRange(week))

date = tab.filter(contains_string('Antibacterial hand wipes')).shift(-1,1).expand(DOWN).is_not_blank() - remove_perentage_data
trace.Date('Date given at cell range: {}', var = excelRange(date)) 

products = tab.filter(contains_string('Antibacterial hand wipes')).expand(RIGHT).is_not_blank() - remove_perentage_data
trace.Products('Products given at cell range: {}', var = excelRange(products))

observations = date.waffle(products)
measure_type = 'Price Indice Change'
trace.Measure_Type('Hardcoded value as: Price Indice Change')
unit = 'Percent'
trace.Unit('Hardcoded value as: Percent')

dimensions = [
    HDim(week, 'Week', DIRECTLY, LEFT),
    HDim(date, 'Period', DIRECTLY, LEFT),
    HDim(products, 'Products', DIRECTLY, ABOVE),
    HDimConst('Measure Type', measure_type),
    HDimConst('Unit', unit),
    ]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
trace.with_preview(tidy_sheet)
#savepreviewhtml(tidy_sheet) 
trace.store("df", tidy_sheet.topandas())


# +
df = trace.combine_and_trace(datasetTitle, "df")
df.rename(columns={'OBS' : 'Value'}, inplace=True)
trace.add_column("Value")
trace.Value("Rename databaker columns OBS to Value")

trace.Date("Formating to gregorian-interval/YYY-MM-DDT00:00:00/P7D")
df['Period'] =  df["Period"].apply(date_time)

tidy = df[['Week', 'Period', 'Products', 'Value', 'Measure Type', 'Unit']]

# -


trace.Week("Remove any prefixed whitespace from all values in column and pathify")
trace.Products("Remove any prefixed whitespace from all values in column and pathify")
trace.Measure_Type("Remove any prefixed whitespace from all values in column and pathify")
trace.Unit("Remove any prefixed whitespace from all values in column and pathify")
for column in tidy:
    if column in ('Week', 'Products', 'Measure Type', 'Unit'):
        tidy[column] = tidy[column].str.lstrip()
        tidy[column] = tidy[column].str.rstrip()
        tidy[column] = tidy[column].map(lambda x: pathify(x))

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'observations.csv', index = False)

tidy


