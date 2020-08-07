# # NHS-D Coronavirus Shielded Patient List Summary Totals, England 

from gssutils import * 
import json 


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
    """Pivot the Age, Gender, ALL breadkdowns and store via the tracer"""
    dims_to_pivot = df["Breakdown Field"].unique().tolist()
    for dim in dims_to_pivot:

        columns=['Period', 'Area', 'Age', 'Gender', 'Measure Type', 'Unit of measure', "Unit multiplier", "Value"]
        trace.start(scraper.distributions[0].title, "sub slice for breakdown field '{}'".format(dim), columns, 
                    scraper.distributions[0].downloadURL)

        trace.multi(["Age", "Gender"], "Pivot the Breakdown Field and Values columns to make Age and Gender dimensions")
        dft = df[df["Breakdown Field"] == dim]
        for add_dim in dims_to_pivot:
            if add_dim == dim and dim != "ALL":
                dft[dim] = df["Breakdown Value"]
                trace.multi([dim], f"Set '{dim}' to the breakdown value.")
            else:
                # Trace multi, so we can set against a variable
                # Dont trace ALL, as we're dropping it in a sec
                if add_dim != "ALL":
                    trace.multi([add_dim], "Set value to all.")
                dft[add_dim] = "All"
        trace.store(store_as, dft)
    
def make_standard_changes(df, trace):
    """Some standard changes that apply to both datasets"""
    
    trace.add_column("Measure Type")
    trace.Measure_Type("Set to 'Count'.")
    df["Measure Type"] = "Count"

    trace.add_column("Unit")
    trace.Unit("Set to 'People'.")
    df["Unit"] = "People"
    
    # Period
    # to day/{year}-{month}-{day}
    trace.Period("Format period as single day URI.")
    df["Period"] = df["Period"].map(lambda x: "day/"+x.replace("/", "-"))

    return df


# -

# ## NOTE
#
# The scrapers not working and we need to access 2 different datasURLS, to get around that we're going to generate an info.json+downloadURL for each on the fly.

# ## Scraper: Coronavirus Shielded Patient List Summary Totals, Local Authority, England

# +
with open("info.json", "r") as f:
    data = json.load(f)
    data["dataURL"] = "https://files.digital.nhs.uk/BD/8E87D5/Coronavirus%20Shielded%20Patient%20List%2C%20England%20-%20Open%20Data%20-%20LA%20-%202020-07-01.csv"
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
    
columns=['Period', 'Area', 'Age', 'Gender']
trace.start(scraper.distributions[0].title, "", columns, scraper.distributions[0].downloadURL)
    
pivot_and_store_breakdowns(df, scraper, LA_TITLE, trace)
df = trace.combine_and_trace(LA_TITLE, LA_TITLE)

# Drop the "All" column and the unwanted columns
trace.ALL("Remove unwanted columns, get rid of column 'LA Name' as we have the codes")
df = df.drop(["ALL", "Breakdown Field", "Breakdown Value", "LA Name"], axis=1)
    
# Rename columns
df = df.rename(columns={"LA Code": "Area", "Extract Date": "Period", "Patient Count": "Value"})
trace.multi(["Area", "Period", "Value"], "Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively")
    
# Measures etc
df = make_standard_changes(df, trace)

# Add missing geo codes
lookup = {
    "ENG": "E92000001"
}
df["Area"] = df["Area"].map(lambda x: lookup.get(x, x))
    
out = Path('out')
out.mkdir(exist_ok=True)
df.to_csv(out / f"{pathify(LA_TITLE)}.csv", index=False)

# -

df['Area'].unique()
#df.head(60)

# ## Scrape: Coronavirus Shielded Patient List Summary Totals, CCG, England

# +
with open("info.json", "r") as f:
    data = json.load(f)
    data["dataURL"] = "https://files.digital.nhs.uk/BA/B409A2/Coronavirus%20Shielded%20Patient%20List%2C%20England%20-%20Open%20Data%20-%20CCG%20-%202020-07-01.csv"
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
trace.ALL("Remove unwanted columns, get rid of column 'CCG Name' as we have the codes")
df = df.drop(["ALL", "Breakdown Field", "Breakdown Value", "CCG Name"], axis=1)
    
# Rename columns
df = df.rename(columns={"CCG Code": "Area", "Extract Date": "Period", "Patient Count": "Value"})
trace.multi(["Area", "Period", "Value"], "Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively")
    
# Measures etc
df = make_standard_changes(df, trace)

out = Path('out')
out.mkdir(exist_ok=True)
df.to_csv(out / f"{pathify(CCG_TITLE)}.csv", index=False)
# -

trace.output()

df.head(60)

df['Age'].unique()

df.columns




