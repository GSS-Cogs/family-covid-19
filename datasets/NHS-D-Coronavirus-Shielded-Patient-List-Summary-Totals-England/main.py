# # NHS-D Coronavirus Shielded Patient List Summary Totals, England 

from gssutils import * 
import json 
from urllib.parse import urljoin
import os


# ## Helpers

# +

def tabs_from_named(tabs, wanted):
    """Given all labs and a list of tab names wanted, return the ones we want, raise if they're not here"""
    wanted = [wanted] if not isinstance(wanted, list) else wanted
    wanted_tabs = [x for x in tabs if x.name.strip() in wanted]
    assert len(wanted_tabs) == len(wanted), \
        f"Could not find tab name {','.join(wanted)} in tabs {','.join([x.name for x in tabs])}"
    return wanted_tabs

def pivot_and_store_breakdowns(df, scraper, store_as, trace):
    """Pivot the Age, Gender, Disease Group, ALL breadkdowns and store via the tracer"""
    dims_to_pivot = df["Breakdown Field"].unique().tolist()
    
    for dim in dims_to_pivot:

        columns=['Period', 'Area', 'Age', 'Gender', 'Disease Group', 'Measure Type', 'Unit of measure', "Unit multiplier", "Value"]
        trace.start(scraper.distributions[0].title, "sub slice for breakdown field '{}'".format(dim), columns, 
                    scraper.distributions[0].downloadURL)

        trace.multi(["Age", "Gender", "Disease_Group"], "Pivot the Breakdown Field and Values columns to make Age and Gender dimensions")
        dft = df[df["Breakdown Field"] == dim]
        for add_dim in dims_to_pivot:
            if add_dim == dim and dim != "ALL":
                dft[dim] = df["Breakdown Value"]
                trace.multi([dim.replace(" ", "_") ], f"Set '{dim}' to the breakdown value.")
            else:
                # Trace multi, so we can set against a variable
                # Dont trace ALL, as we're dropping it in a sec
                if add_dim != "ALL":
                    trace.multi([add_dim.replace(" ", "_") ], "Set value to all.")
                dft[add_dim.replace(" ", "_") ] = "All"
        trace.store(store_as, dft)
    
def make_standard_changes(df, trace):
    """Some standard changes that apply to both datasets"""
    
    trace.add_column("Measure Type")
    trace.Measure_Type("Set to 'Count'.")
    df["Measure Type"] = "Count"

    trace.add_column("Unit")
    trace.Unit("Set to 'Patients'.")
    df["Unit"] = "Patients"
    
    # Period
    # to day/{year}-{month}-{day}
    trace.Period("Format period as single day URI.")
    df["Period"] = df["Period"].map(lambda x: "day/"+x.replace("/", "-"))

    return df


from rdflib import Graph
import rdflib as rd
import numpy as np

def mapPlaceNamesWithCodes(placeNames):
    try:
        g = Graph()
        g.parse("../../Reference/reference-geography.ttl", format="ttl")
        
        c = placeNames.columns[0]
        las = pd.DataFrame(placeNames[c].unique())
        laslist = list(placeNames[c].unique())
        las.rename(columns={0 : 'Category'}, inplace=True)
        las['Code'] = ''
        for la in laslist:
            q = (f"SELECT ?s ?p ?o WHERE  {{ ?s ?p '{la.strip()}' . ?s <http://www.w3.org/2000/01/rdf-schema#label> ?o . }}")
            try:
                qres = g.query(q)
                for row in qres:
                    las['Code'][las['Category'] == la.strip()] = row[2].strip()
                    break
            except Exception as e:
                print("No Match!: " + str(e))
                return placeNames[c]
        placeNames[c] = placeNames[c].map(las.set_index('Category')['Code'])
        return placeNames[c]
    except Exception as e:
        print('Main Error: ' + str(e))
        return placeNames[c]


# -

# ## NOTE
#
# The scrapers not working and we need to access 2 different datasURLS, to get around that we're going to generate an info.json+downloadURL for each on the fly.

# ## Scraper: Coronavirus Shielded Patient List Summary Totals, Local Authority, England
#     (Coronavirus Shielded Patient List, England - Open Data with CMO DG - LA - 2020-08-20)

# +
with open("info.json", "r") as f:
    data = json.load(f)
    data["dataURL"] = "https://files.digital.nhs.uk/63/0A6FF2/Coronavirus%20Shielded%20Patient%20List%2C%20England%20-%20Open%20Data%20with%20CMO%20DG%20-%20LA%20-%202020-08-20.csv"
with open("temp.json", "w") as f:
    json.dump(data, f)

LA_TITLE = "Coronavirus Shielded Patient List Summary Totals, Local Authority, England"
scraper = Scraper(seed="temp.json") 
scraper.distributions[0].title = LA_TITLE
source_sheet = scraper.distribution(latest=True).downloadURL
print("Using source data", source_sheet)
scraper 
# -

# ## Transform: Coronavirus Shielded Patient List Summary Totals, Local Authority, England

# +

trace = TransformTrace()
df = scraper.distribution(latest=True).as_pandas()
    
columns=['Period', 'Area', 'Age', 'Gender', 'Disease Group']
trace.start(scraper.distributions[0].title, "", columns, scraper.distributions[0].downloadURL)
    
pivot_and_store_breakdowns(df, scraper, LA_TITLE, trace)
df = trace.combine_and_trace(LA_TITLE, LA_TITLE)

# Drop the "All" column and the unwanted columns
trace.ALL("Remove unwanted columns, get rid of column 'LA Name' as we have the codes")
df = df.drop(["ALL", "Breakdown Field", "Breakdown Value", "LA Name", "Disease_Group"], axis=1)
    
# Rename columns
df = df.rename(columns={"LA Code": "Geography Code", "Extract Date" : "Period", "Patient Count": "Value"})
trace.multi(["Area", "Period", "Value"], "Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively")
    
# Measures etc
df = make_standard_changes(df, trace)

# Add missing geo codes
lookup = {
    "ENG": "E92000001"
}
df["Geography Code"] = df["Geography Code"].map(lambda x: lookup.get(x, x))
df['Disease Group'] = df['Disease Group'].fillna('All')
df['Geography Type']='Local Authority'

tidy_1 =df[['Period', 'Geography Code', 'Geography Type', 'Disease Group', 'Gender', 'Age', 'Measure Type', 'Unit', 'Value']]
# -

# ## Scrape: Coronavirus Shielded Patient List Summary Totals, CCG, England

# +
with open("info.json", "r") as f:
    data = json.load(f)
    #data["dataURL"] = "https://files.digital.nhs.uk/BA/B409A2/Coronavirus%20Shielded%20Patient%20List%2C%20England%20-%20Open%20Data%20-%20CCG%20-%202020-07-01.csv"
    data["dataURL"] = "https://files.digital.nhs.uk/96/1D4DE5/Coronavirus%20Shielded%20Patient%20List%2C%20England%20-%20Open%20Data%20with%20CMO%20DG%20-%20CCG%20-%202020-08-20.csv"
with open("temp.json", "w") as f:
    json.dump(data, f)

CCG_TITLE = "Coronavirus Shielded Patient List Summary Totals, CCG, England"
scraper = Scraper(seed="temp.json") 
scraper.distributions[0].title = CCG_TITLE
source_sheet = scraper.distribution(latest=True).downloadURL
print("Using source data", source_sheet)
scraper 
# -

# ## Transform: Coronavirus Shielded Patient List Summary Totals, CCG, England

# +

trace = TransformTrace()
df = scraper.distribution(latest=True).as_pandas()
    
columns=['Period', 'Area', 'Age', 'Gender']
trace.start(scraper.distributions[0].title, "", columns, scraper.distributions[0].downloadURL)
    
pivot_and_store_breakdowns(df, scraper, CCG_TITLE, trace)
df = trace.combine_and_trace(CCG_TITLE, CCG_TITLE)

# Drop the "All" column and the unwanted columns
trace.ALL("Remove unwanted columns, get rid of column 'CCG Code' as we have the codes")
df = df.drop(["ALL", "Breakdown Field", "Breakdown Value", "CCG Code", "Disease_Group"], axis=1)
    
# Rename columns
df = df.rename(columns={"CCG Name": "Geography Code", "Extract Date": "Period", "Patient Count": "Value"})
trace.multi(["Area", "Period", "Value"], "Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively")
    
# Measures etc
df = make_standard_changes(df, trace)
df['Disease Group'] = df['Disease Group'].fillna('All')
df['Geography Type']='Clinical Commissioning Group'

lookup = {
    "ENG": "E92000001"
}
df["Geography Code"] = df["Geography Code"].map(lambda x: lookup.get(x, x))
#CG Name column to be mapped to ONS Geography codes instead
df['Geography Code'] = mapPlaceNamesWithCodes(pd.DataFrame(df['Geography Code']))

tidy_2 =df[['Period', 'Geography Code', 'Geography Type', 'Disease Group', 'Gender', 'Age', 'Measure Type', 'Unit', 'Value']]

# +
joined_data = pd.concat([tidy_1, tidy_2])
joined_data = joined_data.rename(columns={"Gender": "Sex", "Period" : "Extract Date"})

sexcode = {
     'All': 'T',
     'Male': 'M',
     'Female': 'F',
}
joined_data = joined_data.replace({"Sex": sexcode})
agecode = { '70+' : '70plus', '90+' : '90plus'}
joined_data = joined_data.replace({"Age": agecode})
lookup = {"": "E92000001"}
joined_data["Geography Code"] = joined_data["Geography Code"].map(lambda x: lookup.get(x, x))

#Adding data marker * = value between 1 and 7
joined_data['Marker'] = ""
f1=((joined_data['Value'] == '*'))
joined_data.loc[f1,'Marker'] = 'between 1 and 7'
joined_data = joined_data.replace({'Value' : {'*' : ''}})

# -

#Checking things out. 
from IPython.core.display import HTML
for col in joined_data:
    if col not in ['Value']:
        joined_data[col] = joined_data[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(joined_data[col].cat.categories) 

for column in joined_data:
    if column in ('Geography Type', 'Disease Group', 'Marker'):
        joined_data[column] = joined_data[column].str.lstrip()
        joined_data[column] = joined_data[column].str.rstrip()
        joined_data[column] = joined_data[column].map(lambda x: pathify(x))

#Removing columns as they are defined in info.json 
del joined_data['Measure Type']
del joined_data['Unit']
joined_data

# +
#SET UP OUTPUT FOLDER AND OUTPUT DATA TO CSV
csvName = 'observations.csv'
out = Path('out')
out.mkdir(exist_ok=True)
joined_data.drop_duplicates().to_csv(out / csvName, index = False)
scraper.dataset.family = 'covid-19'
scraper.dataset.title = 'Coronavirus Shielded Patient List Summary Totals, England by Clinical Commissioning Group and Local Authority'
#scraper.dataset.comment = notes

# CREATE MAPPING CLASS INSTANCE, SET UP VARIABLES AND WRITE FILES
csvw_transform = CSVWMapping()
csvw_transform.set_csv(out / csvName)
csvw_transform.set_mapping(json.load(open('info.json')))
csvw_transform.set_dataset_uri(urljoin(scraper._base_uri, f'data/{scraper._dataset_id}'))
csvw_transform.write(out / f'{csvName}-metadata.json')
# -

# CREATE AND OUTPUT TRIG FILE
with open(out / f'{csvName}-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

trace.output()





