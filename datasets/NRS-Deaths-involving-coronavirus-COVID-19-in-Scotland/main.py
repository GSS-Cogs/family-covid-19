# +
### NRS Deaths involving coronavirus COVID-19 in Scotland
# -
# just try and get it working

all_dat = []
#trace = TransformTrace()

# %run 'NRS COVID Deaths.py' 
all_dat.append(tidy)

# %run 'NRS All Deaths.py' 
all_dat.append(tidy)

# %run 'NRS All Deaths by location.py' 
all_dat.append(tidy)

# +
#datacube_name = "NRS Registered COVID-19 and All Deaths"
#columns=['Period', 'Registered Death Type', 'Council Area', 'NHS Board', 'NRS Age Group', 'Location of Death', 'Sex']
#trace.start(datacube_name, tab, columns, scrape.distributions[0].downloadURL)
# -

print('Date range from NRS All Deaths script: ' + str(date_range) + ' Days')
print('Minimum date from NRS All Deaths script: ' + str(min_date))
date_range_str = 'gregorian-interval/' + str(min_date).replace(' ','T') + '/P' + str(date_range) + 'D'
print('Formatted date range string: ' + date_range_str)

# Replace nans in the Period column with the date range value
all_dat[0]['Period'] = all_dat[0]['Period'].replace(np.nan,date_range_str)
all_dat[1]['Period'] = all_dat[1]['Period'].replace(np.nan,date_range_str)

# Insert some columns so all the tables match up
all_dat[2].insert(0,'Period', date_range_str)
all_dat[2].insert(4,'Deaths by Gender', 'All')
all_dat[2].insert(5,'NRS Age Group', 'All')
all_dat[2] = all_dat[2][['Period', 'Deaths Registered', 'Deaths by Council Area', 'Deaths by NHS Board', 'NRS Age Group', 'Deaths by location', 'Deaths by Gender', 'Measure Type', 'Unit', 'Value']]

print("COVID-19 Deaths *********")
print(list(all_dat[0]))
print("All Deaths *********")
print(list(all_dat[1]))
print("Location Deaths *********")
print(list(all_dat[2]))

# Join all the tables together
joined_dat = pd.concat(all_dat)
joined_dat['Deaths Registered'] = joined_dat['Deaths Registered'].str.replace('-194','-19')
joined_dat['Deaths Registered'].unique()

# Rename some columns
joined_dat = joined_dat.rename(columns={'Deaths by Gender': 'Sex', 'Deaths by Council Area': 'Council Area',
                                       'Deaths by NHS Board': 'NHS Board', 'Deaths by location': 'Location of Death',
                                       'Deaths Registered': 'Registered Death Type'})

# Pull the mapping files into DataFrames
geogsHB = pd.read_csv('../../Reference/scottish-health-board-mapping.csv') 
geogsCA = pd.read_csv('../../Reference/scottish-council-areas-mapping.csv') 
sexMap = pd.read_csv('../../Reference/sex-mapping.csv') 

# Map the Geography codes
joined_dat['NHS Board'] = joined_dat['NHS Board'].map(geogsHB.set_index('Category')['Code'])
joined_dat['Council Area'] = joined_dat['Council Area'].map(geogsCA.set_index('Category')['Code'])

# Map the Sex codes
joined_dat['Sex'] = joined_dat['Sex'].str.strip()
joined_dat['Sex'] = joined_dat['Sex'].map(sexMap.set_index('Category')['Code'])

for c in joined_dat.columns:
    if (c != 'Period') & (c != 'Measure Type') & (c != 'Sex') &(c != 'Unit') & (c != 'Value') :
        joined_dat[c] = joined_dat[c].map(lambda x: pathify(x))

# +
del joined_dat['Measure Type']
del joined_dat['Unit']

joined_dat['Value'] = pd.to_numeric(joined_dat['Value'], downcast='integer')
# -

# Output the data to CSV
out = Path('out')
out.mkdir(exist_ok=True)
joined_dat.drop_duplicates().to_csv(out / 'observations.csv', index = False)

joined_dat.head(60)

# +
scrape.dataset.family = 'covid-19'

# Output CSV-W metadata (validation, transform and DSD).
# Output dataset metadata separately for now.

import os
from urllib.parse import urljoin

dataset_path = pathify(os.environ.get('JOB_NAME', 'gss_data/covid-19/' + Path(os.getcwd()).name))
scrape.set_base_uri('http://gss-data.org.uk')
scrape.set_dataset_id(dataset_path)
scrape.dataset.title = 'NRS Deaths involving COVID-19 in Scotland'
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / 'observations.csv')
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scrape._base_uri, f'data/{scrape._dataset_id}'))
csvw_transform.write(out / 'observations.csv-metadata.json')
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scrape.generate_trig())

# +
#help(scrape)
# -








