# # ONS Deaths involving COVID-19 in the care sector, England and Wales 

from gssutils import *
import datetime
import json 
import logging
import re


# +
#### Add transformation script here #### 

scraper = Scraper(seed="info.json") 
tabs = scraper.distribution(latest=True).as_databaker()
source_sheet = scraper.distribution(latest=True).downloadURL
print("Using source data", source_sheet)
scraper 
# -

# ## Geography
#
# Using a cmd api for this (should probably be the open geography portal) plus some overides to save having to hard code a billion things.

# +
import requests

class Geography(object):
    """
    We're going to 'borrow' a json representation of the admin hierarchy to do
    some basic lookups of area codes.
    """

    def __init__(self, url, overrides={}):
        self.url = url
        r = requests.get(self.url)
        if r.status_code != 200:
            raise Exception("Failed to get geography codes off cmd, status code {},from url {}" \
                           .format(r.status_code, self.url))
        self.json = r.json()
        
        # Where the same label is used for two codes, we use an overrides dict to pass in 
        # specific choices
        self.overrides = overrides
        
    def __call__(self, label):
        
        if label in self.overrides.keys():
            return self.overrides[label]
        else:
            found = []
            for item in self.json["items"]:
                if item["label"].lower().strip() == label.lower().strip():
                    found.append(item["code"])
            assert len(found) == 1, f"There is not exactly one code for {label} on {self.url}." \
                            f" Instead we got: {','.join(found)}"
            return found[0]
                
region_overrides = {
     'England and Wales': 'K04000001',
     'England': 'E92000001',
     'Wales': 'E05001035',
     'East': 'E12000006'
}
get_regions = Geography("https://api.beta.ons.gov.uk/v1/code-lists/regions/editions/2017/codes", 
                        overrides=region_overrides)

local_authority_overrides = {
     'England and Wales': 'K04000001',
     'England': 'E92000001',
     'Wales': 'E05001035'
}
get_local_authorities = Geography("https://api.beta.ons.gov.uk/v1/code-lists/local-authority/editions/2016/codes", 
                                overrides=local_authority_overrides)


# -

# ## Helpers

# +

def tabs_from_named(tabs, wanted):
    """Given all labs and a list of tab names wanted, return the ones we want, raise if they're not here"""
    wanted = [wanted] if not isinstance(wanted, list) else wanted
    wanted_tabs = [x for x in tabs if x.name.strip() in wanted]
    assert len(wanted_tabs) == len(wanted), \
        f"Could not find tab name {','.join(wanted)} in tabs {','.join([x.name for x in tabs])}"
    return wanted_tabs
 

class is_type(object):
    """Filter to match cell on type of cell.value"""
    
    def __init__(self, type_wanted):
        self.type_wanted = type_wanted
        
    def __call__(self, cell):
        return True if type(cell.value) == self.type_wanted else False

    
def assert_one_of(cells, name_of_selection, expected):
    """Given a list of acceptable values, blow up if we get something else"""
    for cell in cells:
        if cell.value not in expected:
            if cell.value.strip() in expected:
                logging.warning(f"When asserting '{name_of_selection}' we matched cell '{cell}' to expected, but with rogue whitepace detected.")
            else:    
                raise AssertionError(f"When asserting '{name_of_selection}' the cell '{cell}' does not contain a value from {','.join(expected)}")

                
def assert_numeric_or_marker(cells, acceptable_markers):
    """Given a selection of cells, assert their values are all numeric or a marker from the provided list"""
    for cell in cells:
        exc = AssertionError(f"The cell '{cell}' is neither numeric nor contains a marker from the list " \
                    f"'{','.join(acceptable_markers)}'.")
         # cast and catch
        try:
            float(cell.value)
        except ValueError:
            if cell.value not in acceptable_markers:
                raise exc
            return
        except Exception as e:
            raise exc from e

            
def assert_continuous_sequence(cells, direction):
    """Given a bag of cells, assert they form a continuous sequence without gaps"""
    assert direction in [UP, DOWN, LEFT, RIGHT], "You need to supply a direction for assert_continuous_sequence"
    all_x = [cell.x for cell in cells]
    all_y = [cell.y for cell in cells]
    
    # Vertical sequence
    if direction in [UP, DOWN]:
        all_y = [cell.y for cell in cells]
        for cell in cells:
            if cell.y+1 not in all_y and cell.y-1 not in all_y:
                raise AssertionError(f"There is a gap in your sequential vetical selection near {cell}")
                
    # Horizontal sequence
    if direction in [LEFT, RIGHT]:
        all_x = [cell.x for cell in cells]
        for cell in cells:
            if cell.x+1 not in all_x and cell.x-1 not in all_x:
                raise AssertionError(f"There is a gap in your sequential horizontal selection near {cell}")


def create_tidy(cs, tab_name, trace):
    """Wrap some standard operations to avoid repeating ourselves"""
    df = cs.topandas().fillna("")

    # rename stuff
    df = df.rename(columns={"OBS":"Value", "DATAMARKER":"Marker"})
        
    # Markers, measures and output
    df = apply_measures(df, tab_name, trace)
    df = apply_markers(df, tab_name, trace)

    return df


def get_title_and_footnotes(tab):
    """
    Given one tab, get the tab name (minus the comment annotations) and a list of comments
    """
    title_cell = tab.excel_ref('A2')
    assert len(title_cell.value) > 10, f"Cell A2 on tab '{tab.name}' does not appear to hold the title"
    
    # Strip the footnotes
    title_cell_split = title_cell.value.strip().split(",")
    footnotes = {}
    title = None
    is_d = re.compile("\d{1}")
    for i in range(len(title_cell_split)-1, 0, -1):
        if is_d.match(title_cell_split[i]):
            footnotes[title_cell_split[i]] = ""
        else:
            title = ",".join(title_cell_split[:i])
            
    # TODO, why am I needing to set this manually?
    if len(footnotes) > 0:
        footnotes["1"] = ""
            
    potential_footnotes = find_source_cell(tab).expand(DOWN).is_not_blank()
    for no in footnotes.keys():
        footnote_text_cell = [x for x in potential_footnotes if x.value.strip().startswith(no)]
        assert len(footnote_text_cell) == 1, f"Could not find a distinct foodnote for annotation {no}"
        footnotes[no] = footnote_text_cell[0].value
    
    return title, footnotes


def find_source_cell(tab):
    """what is says"""
    try:
        # in case of multi-table sheets
        s = tab.excel_ref('A').filter(lambda x: str(x.value).startswith("Source:")).by_index(-1)
    except xypath.XYPathError:
        s = tab.excel_ref('A').filter(lambda x: str(x.value).startswith("Source:")).by_index(1)
    except:
        raise
    return s


def get_unwanted(tab):
    """return anything level with or below the source cell"""
    return find_source_cell(tab).expand(DOWN).expand(RIGHT)


# TODO
def apply_measures(df, tab_name, trace):
    """Given a dataframe and the source tab name, add the correct measure types"""

    # Was expecting some variety, probably doesnt need its own function
    um = 1
    trace.add_column("Unit Multiplier")
    trace.Unit_Multiplier("Set unit multiplier to {}.", var=str(um))
    
    m = "Count"
    df["Measure Type"] = m
    trace.add_column("Measure Type")
    trace.Measure_Type("Set Measure Type to {}.", var=m)    
        
    u = "People"
    df["Unit of Measure"] = u
    trace.add_column("Unit of Measure")
    trace.Unit_of_Measure("Set Unit of Measure to {}.", var=u) 
        
    return df


# TODO
def apply_markers(df, tab_name, trace):
    """Given a dataframe and the source tab name, add our version of the data markers"""
    
    if "Marker" not in df.columns.values:
        return df
    
    markers = {
        ":": "no-data-availible"
    }
    df["Marker"] = df["Marker"].map(lambda x: markers.get(x, ""))
    trace.Marker("Converting data markers with the lookup: {}", var=json.dumps(markers))
    return df


def excelRange(bag):
    min_x = min([cell.x for cell in bag])
    max_x = max([cell.x for cell in bag])
    min_y = min([cell.y for cell in bag])
    max_y = max([cell.y for cell in bag])
    top_left_cell = xypath.contrib.excel.excel_location(bag.filter(lambda x: x.x == min_x and x.y == min_y))
    bottom_right_cell = xypath.contrib.excel.excel_location(bag.filter(lambda x: x.x == max_x and x.y == max_y))
    return f"{top_left_cell}:{bottom_right_cell}"
    
    
class format_time(object):
    """
    Appliable class for formatting dates based on the style used
    """
    
    def __init__(self, time_style):
        allowed = { 
            "specific_day": self._specific_day
        }
        assert time_style in allowed.keys(), f"There is no handling for the time style {time_style}"
        self.date_style = allowed[time_style] 
        
    def _specific_day(self, cell_val):
        # from: 28/12/2019
        # to:  gregorian/{year}-{month}-{day}
        return ">>>>"+str(cell_val)
    
    def __call__(self, cell_val):
        return self.date_style(cell_val)
    
trace = TransformTrace()
footnotes_dict = {}
comments = {}
# -
# ## Transform: Table 1

for tab in tabs_from_named(tabs, "Table 1"):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Marker', 'Period', 'Cause of death', 'Source', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        # Start with the date title cell
        date_cell = tab.excel_ref('A').filter("Date").assert_one() 

        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))
        assert_continuous_sequence(period, UP)
        trace.Period("{} Got period as datatime types in column A", var=excelRange(period))

        # Cause of death
        cause_of_death = date_cell.fill(RIGHT).is_not_blank()
        accepted_causes = ["Deaths involving COVID-19", "All deaths", "2019 Comparison"]
        assert_one_of(cause_of_death, "cause_of_death", accepted_causes)
        trace.Cause_of_death("{} Selected category items as 'Deaths involving COVID-19, 'All deaths'"
                        "2019 Comparison", var=excelRange(cause_of_death))

        # Area and Source
        # NOTE - same thing, we'll split the source bit into an attribute in post
        source = date_cell.shift(UP).fill(RIGHT).is_not_blank()
        accepted_source = ["England and Wales (ONS data)", "England (ONS data)", 
                               "England (CQC data)", "Wales (ONS data)", "Wales (CIW data)"]
        assert_one_of(source, "source", accepted_source)
        msg = "Selected source items as '{}'. Please note - we'll be splitting these into an area " \
               " dimension and a seperate 'Source' attribute in post.".format(accepted_source)
        trace.Source("{} " + msg, var=excelRange(source))
        
        # observations
        obs = cause_of_death.waffle(period)
        
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(cause_of_death, "Cause of death", DIRECTLY, ABOVE),
            HDim(source, "Source", CLOSEST, LEFT)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        df["Period"] = df["Period"].apply(format_time("specific_day"))
        
        # Split source and area
        df["Area"] = df["Source"].map(lambda x: x.split("(")[0].strip())
        for x in df["Area"].unique():
            assert x in ['England and Wales', 'England', 'Wales'], f"'{x}' is not an expected Area"
            
        df["Source"] = df["Source"].map(lambda x: x.split("(")[1].strip(")"))
        for x in df["Source"].unique():
            assert x in ['ONS data', 'CQC data', 'CIW data'], f"{x} is not an expected Source"
        trace.multi(["Source", "Area"], "Split the cells extracted as 'Source' into seperate " \
                   "Source and Area columns")
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube from tab '{tab.name}'.") from e

# ## Transform: Table 2

for tab in tabs_from_named(tabs, "Table 2"):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Sex', 'Age', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        # Start with the first persons cell
        first_persons_cell = tab.excel_ref('B').filter("Persons").assert_one()

        # Sex
        sex = first_persons_cell.expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Persons", "Male", "Female"])
        trace.Sex("{} Get dimension 'Sex', with values 'Persons', 'Male' and 'Female'", var=excelRange(sex))
        
        # Area
        area = first_persons_cell.shift(UP).shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(area, "area", ["England and Wales", "England", "Wales"])
        trace.Area("{} Get dimension 'Area' with values 'England and Wales', "
                    "'England' and 'Wales'", var=excelRange(area))
        
        # Age
        age = tab.excel_ref('A').filter('All ages').expand(DOWN).is_not_blank() - get_unwanted(tab)
        assert_one_of(age, "Age", ["All ages", "0-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"])
        trace.Age("{} Get age dimension from column A, as number range plus 'All ages'", var=excelRange(age))
       
        # observations
        obs = first_persons_cell.shift(DOWN).expand(DOWN).expand(RIGHT).is_not_blank() \
                .is_not_whitespace() - get_unwanted(tab)
        assert_numeric_or_marker(obs, [":"])
    
        dimensions = [
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(area, "Area", CLOSEST, LEFT)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)

    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e

# ## Transform: Tables 3 & 4

# +
cube3n4_title = "Number of deaths, age standardised and age specific mortality rates, by sex"
for tab in tabs_from_named(tabs, ["Table 3", "Table 4"]):

    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Sex', 'Age', "Rate", {"Lower 95% CI": "Lower_CI"}, {"Lower 95% CI": "Upper_CI"}, 
                 'Area', 'Category']
        trace.start(cube3n4_title, tab, columns, source_sheet)
        
        first_death_cells = tab.excel_ref('B').filter("Number of deaths")
        assert len(first_death_cells) == 4, "Aborting, there should be exactly 4 'Number of deaths' cells"
    
        ignore_for_obs = \
            first_death_cells.expand(RIGHT) | \
            first_death_cells.shift(UP).expand(RIGHT) | \
            first_death_cells.shift(UP).shift(UP).expand(RIGHT)                                 
        
        # Sex
        sex = first_death_cells.by_index(1).shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Person", "Male", "Female"])
        trace.Sex("{} Get dimension 'Sex', with values 'Persons', 'Male', 'Females'.", var=excelRange(sex))
        
        # Attributes to pivot later
        attributes = first_death_cells.by_index(1).expand(RIGHT).is_not_blank()

        category = tab.excel_ref('A').filter(starts_with("Number of deaths"))
        assert len(category) == 4, "We are expecting 4 categories beginner 'Numbers of deaths' in column A"
        trace.Category("{} Get dimension 'category' as things starting 'Number of deaths..' from column A."
                       , var=excelRange(category))
        
        # need to use a specific line for closest to avoid equally valid lookups
        area = first_death_cells.by_index(1).shift(UP).shift(UP)
        trace.Area("{} Area is either 'England' or 'Wales'.", var=excelRange(area))
        
        # Obs should be anything outisde of column A that's not selected elsewhere
        obs = first_death_cells.expand(DOWN).expand(RIGHT).is_not_blank() - ignore_for_obs
        assert_numeric_or_marker(obs, [":"])
              
        obs_in_b = obs.filter(lambda x: x.x == 1)
        age = tab.excel_ref('A1').waffle(obs_in_b)
        trace.Age("{} Dimension 'Age' is from column A", var=excelRange(age))
        
        dimensions = [
            HDim(sex, "Sex", CLOSEST, LEFT),
            HDim(attributes, "TEMP_FOR_ATTRIBUTES", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(area, "Area", CLOSEST, ABOVE),
            HDim(category, "Category", CLOSEST, ABOVE)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Make a hacky composite key
        df["Composite"] = ""
        for col in ["Sex", "Age", "Area", "Category"]:
            df["Composite"] = df["Composite"] + df[col]
        
        # Use that composite key to match attributes to obs
        trace.multi(["Rate", "Lower_CI", "Upper_CI"], "Flatten the observations, pulling these" 
                    "values into their own appropriate attribute column")
        for attribute in ["Rate", "Lower 95% CI", "Upper 95% CI"]:
            df[attribute] = ""
            for _, row in df[df["TEMP_FOR_ATTRIBUTES"] == attribute].iterrows():
                df[attribute][df["Composite"] == row["Composite"]] = row["Value"]

        # sort out messy categories
        df["Category"] = df["Category"].map(lambda x: x.split(",")[0])
        should_be = [
                'Number of deaths',
                'Number of deaths of non-care home residents due to COVID-19',
                'Number of deaths of care home residents from all causes',
                'Number of deaths of non-care home residents from all causes'
        ]
        for item in df["Category"].unique().tolist():
            assert item in should_be, "Unexpected category. '{}' not in '{}'." \
                            .format(item, json.dummps(should_be))
        trace.Category("Shortened categories to remove repeated (and super long) date info."
                      " Took everything to the left of the first comma")
                
        # Tidy up temporary nonsence
        df = df.drop(["Composite", "TEMP_FOR_ATTRIBUTES"], axis=1)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        trace.store(cube3n4_title, df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube3n4_title}' from tab '{tab.name}'.") from e
        
df = trace.combine_and_trace(cube3n4_title, cube3n4_title)
df.to_csv(f"{pathify(cube3n4_title)}.csv", index=False)
# -

# ## Transform: Table 5, 6

# +
cube5n6_title = "Number of deaths of care home residents by place of death"
for tab in tabs_from_named(tabs, ["Table 5", "Table 6"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Area', 'Place of death']
        trace.start(cube5n6_title, tab, columns, source_sheet)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        trace.Period("{} Period dimension taken as date types from column A plus 'Total'.", \
                    var=excelRange(period))
        
        # Area
        area = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(area, "Area", ["England and Wales", "England", "Wales"])
        trace.Area('{} Area dimension taken as "England and Wales", "England", "Wales"', \
                  var=excelRange(area))
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Care Home", "Hospital", "Elsewhere"])
        trace.Place_of_death('{} the dimension "Place of death" taken as "Care Home", "Hospital",' \
                             '"Elsewhere"', var=excelRange(place_of_death))
        
        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(area, "Area", CLOSEST, LEFT),
            HDim(place_of_death, "Place of death", DIRECTLY, ABOVE),
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
                
        trace.store(cube5n6_title, df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube5n6_title}' from tab '{tab.name}'.") from e
        
df = trace.combine_and_trace(cube5n6_title, cube5n6_title)
df.to_csv(f"{pathify(cube5n6_title)}.csv", index=False)

# -


# ## Transform: Table 7,8

# +
cube7n8_title = "Number of deaths of care home residents notified to the Care Quality Commission"
for tab in tabs_from_named(tabs, ["Table 7", "Table 8"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Place Of Death', 'Area', 'Cause Of Death']
        trace.start(cube7n8_title, tab, columns, source_sheet)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        trace.Period("{} Period dimension taken as date types from column A plus 'Total'.", \
                    var=excelRange(period))
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Care Home", "Hospital", "Elsewhere", "Not Stated"])
        trace.Place_Of_Death('{} the dimension "Place of death" taken as "Care Home", "Hospital", "Elsewhere",' \
                             '"Not Stated"', var=excelRange(place_of_death))
        
        # Cause of death
        cause_of_death = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(cause_of_death, "cause_of_death", ["All deaths", "COVID-19"])
        trace.Cause_Of_Death('{} the dimension "Cause of death" taken as "All deaths", "COVID-19"', \
                            var=excelRange(cause_of_death))

        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        area = "England" if tab.name.strip() == "Table 7" else "Wales"
        trace.Area("Set to 'England for table 7, else 'Wales'.")
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(place_of_death, "Place Of Death", DIRECTLY, ABOVE),
            HDim(cause_of_death, "Cause Of Death", CLOSEST, LEFT),
            HDimConst("Area", area)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        trace.store(cube7n8_title, df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube7n8_title}' from tab '{tab.name}'.") from e
        
df = trace.combine_and_trace(cube7n8_title, cube7n8_title)
df.to_csv(f"{pathify(cube7n8_title)}.csv", index=False)

# -


# ## Transform: Table 9

for tab in tabs_from_named(tabs, ["Table 9"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Place Of Death', 'Area', 'Cause Of Death']
        trace.start(title, tab, columns, source_sheet)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        trace.Period("{} Period dimension taken as date types from column A plus 'Total'.", \
                    var=excelRange(period))
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Home care", "Hospital", "Elsewhere", "Not Stated"])
        trace.Place_Of_Death('{} the dimension "Place of death" taken as "Care Home", "Hospital", "Elsewhere",' \
                             '"Not Stated"', var=excelRange(place_of_death))
        
        # Cause of death
        cause_of_death = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(cause_of_death, "category_of_death", ["All deaths", "COVID-19"])
        trace.Cause_Of_Death('{} the dimension "Cause of death" taken as "All deaths", "COVID-19"', \
                            var=excelRange(cause_of_death))
        
        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
                
        area = "England"
        trace.Area("Hard coded Area to {}", var=area)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(place_of_death, "Place Of Death", DIRECTLY, ABOVE),
            HDim(cause_of_death, "Cause Of Death", CLOSEST, LEFT),
            HDimConst("Area", area)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)

    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Table 10

for tab in tabs_from_named(tabs, ["Table 10"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Value', 'Category', 'Period', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        assert_continuous_sequence(period, UP)
        trace.Period("{} Period dimension taken as date types from column A.", \
                    var=excelRange(period))
        
        # Category
        category = date_cell.fill(RIGHT).is_not_blank()
        assert_one_of(category, "category", ["Care home resident", "Home care service user"])
        trace.Category("{} dimension 'Category' taken as 'Care home resident' and " \
                       "'Home care service user'.", var=excelRange(category))
        
        obs = category.waffle(period)
        assert_numeric_or_marker(obs, [":"])
        
        area = "England"
        trace.Area("Hard coded Area to {}", var=area)
        
        dimensions = [
            HDim(category, "Category", DIRECTLY, ABOVE),
            HDim(period, "Period", DIRECTLY, LEFT),
            HDimConst("Area", area)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Table 11

for tab in tabs_from_named(tabs, ["Table 11"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Cause of death', 'Period', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        first_region = tab.excel_ref("B").filter("East").assert_one()
        
        # Period
        period = first_region.shift(LEFT).fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        assert_continuous_sequence(period, UP)
        trace.Period("{} Period dimension taken as date types from column A.", \
                    var=excelRange(period))
        
        # Area
        area = first_region.expand(RIGHT).is_not_blank()
        assert_one_of(area, "area", ["East", "East Midlands", "London", "North East", "North West", 
                                     "South East", "South West", "West Midlands",
                                     "Yorkshire and the Humber", "Wales"])
        trace.Area("{} Area dimension is left to right starting from East", var=excelRange(area))
        
        # Category of death
        cause_of_death = first_region.shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(cause_of_death, "cause_of_death", ["All deaths", "Deaths involving COVID-19"])
        trace.Cause_of_death('{} "Cause of death" taken as either "All deaths" or "Deaths involving' \
                            ' COVID-19".', var=excelRange(cause_of_death))
        
        obs = period.waffle(area)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(cause_of_death, "Cause of death", CLOSEST, LEFT),
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(area, "Area", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Tables 12 & 13

# +
cube12n13_title = "Number of weekly deaths of care home residents by local authority"
for tab in tabs_from_named(tabs, ["Table 12", "Table 13"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Area', 'Week Number', 'Cause of death']
        trace.start(cube12n13_title, tab, columns, source_sheet)
        
        area_code_header = tab.excel_ref('A').filter("Area Code").assert_one()
        
        week_no = area_code_header.shift(UP).expand(RIGHT).is_not_blank()
        trace.Week_Number("{} Week number taken as left-to-right integers across the " \
                          "top.", var=excelRange(week_no))
        
        area = area_code_header.fill(DOWN).regex("[A-Z]{1}\d{8}")
        assert_continuous_sequence(area, UP)
        trace.Area("{} Area code taken as the continusous sequence of codes from column" \
                   " A.", var=excelRange(area))
        
        period = area_code_header.fill(RIGHT).is_not_blank()
        assert_continuous_sequence(period, RIGHT)
        trace.Period("{} Period taken as continuous honizontal sequence of dates across " \
                     " the top.", var=excelRange(period))
        
        obs = area.shift(RIGHT).waffle(period - tab.excel_ref('B'))
        assert_numeric_or_marker(obs, [":"])
        
        cause_of_death = "Deaths involving COVID-19" if tab.name.strip() == "Table 15" else "All deaths"
        trace.Cause_of_death("Based on tab name, value set to {}.", \
                                   var=cause_of_death)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", DIRECTLY, ABOVE),
            HDimConst("Cause of death", cause_of_death)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        trace.store(cube12n13_title, df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube12n13_title}' from tab '{tab.name}'.") from e
        
df = trace.combine_and_trace(cube12n13_title, cube12n13_title)
df.to_csv(f"{pathify(cube12n13_title)}.csv", index=False)

# -


# ## Tables 14 & 15

# +
cube14n15_title = "Number of weekly deaths of care home residents by local authority"
for tab in tabs_from_named(tabs, ["Table 14", "Table 15"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Area', 'Week Number', 'Cause of death']
        trace.start(cube14n15_title, tab, columns, source_sheet)
        
        # We're gonna anchor to the first instance of "England" in column A
        # that's a bit flimsy so we'll double confirm it
        big_england = tab.excel_ref('A').filter("England").assert_one()
        big_england2 = tab.excel_ref('A').is_not_blank().by_index(3)
        assert big_england == big_england2, "England needs to be the first area in column A, got" \
                                " '{}'.".format(big_england2.value)

        week_no = big_england.shift(UP).shift(UP).expand(RIGHT)
        trace.Week_Number("{} Week number taken as left-to-right integers across the " \
                          "top.", var=excelRange(week_no))
        
        area = big_england.expand(DOWN) - get_unwanted(tab)
        assert_continuous_sequence(area, UP)
        trace.Area("{} Area is taken from column A, below 'England' minus footnotes.", \
                  var=excelRange(area))
        
        period = big_england.shift(UP).fill(RIGHT).is_not_blank()
        assert_continuous_sequence(period, RIGHT)
        trace.Period("{} 'Period' dimension taken as continuous sequence of dates" \
                     " across the top", var=excelRange(period))
        
        obs = area.shift(RIGHT).waffle(period - tab.excel_ref('B'))
        assert_numeric_or_marker(obs, [":"])
        
        cause_of_death = "Deaths involving COVID-19" if tab.name.strip() == "Table 15" else "All deaths"
        trace.Cause_of_death("Based on tab name, value set to {}.", \
                                   var=cause_of_death)
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", DIRECTLY, ABOVE),
            HDimConst("Cause of death", cause_of_death)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Make a note about stupid geography
        if tab.name not in comments.keys():
            comments[tab.name] = []
        comments[tab.name].append("Cant codify geography for this. Needs investigating but they seem to be" \
                              " inventing geographies by ramming some places together randomly. " \
                               "eg 'Bournemouth, Christchurch and Poole'.")
        
        # Where the period is "Grand Total" set the week no to "All"
        assert "Grand total" in df["Period"].unique(), "The label 'Grand total' is expected and required"
        df["Week Number"][df["Period"] == "Grand total"] = "All"
        
        trace.store(cube14n15_title, df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube14n15_title}' from tab '{tab.name}'.") from e
        
df = trace.combine_and_trace(cube14n15_title, cube14n15_title)
df.to_csv(f"{pathify(cube14n15_title)}.csv", index=False)

# -


# ## Table 16

for tab in tabs_from_named(tabs, ["Table 16"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Period', 'Area', 'Week Number', 'Cause of death']
        trace.start(title, tab, columns, source_sheet)
        
        area_code_header = tab.excel_ref('A').filter("Area Code")
        
        area = area_code_header.fill(DOWN).regex("[A-Z]{1}\d{8}")
        assert_continuous_sequence(area, UP)
        trace.Area("{} Area code taken as the continuous sequence of codes from column" \
                " A.", var=excelRange(area))
        
        cause_of_death = area_code_header.shift(RIGHT).fill(RIGHT).is_not_blank()
        assert_continuous_sequence(cause_of_death, RIGHT)
        assert_one_of(cause_of_death, "cause_of_death", ["All deaths", "COVID-19"])
        trace.Cause_of_death('{} dimension "Cause of death" taken as "All deaths", "COVID-19"', \
                             var=excelRange(cause_of_death))

        period = area_code_header.shift(UP).fill(RIGHT).is_not_blank()
        trace.Period("{} Period taken as continuous horizontal sequence of dates across " \
                     " the top.", var=excelRange(period))
        
        week_no = area_code_header.shift(UP).shift(UP).expand(RIGHT).is_not_blank()
        trace.Week_Number("{} Week number taken as horizontal sequence of integers across the " \
                          "top.", var=excelRange(week_no))
        
        obs = area.waffle(cause_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", CLOSEST, LEFT),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", CLOSEST, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Table 17


for tab in tabs_from_named(tabs, ["Table 17"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Leading cause', 'Sex', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        leading_cause_code_header = tab.excel_ref('A').filter("Leading cause code").assert_one()
        
        # Area
        area = leading_cause_code_header.shift(UP).fill(RIGHT).is_not_blank()
        assert_one_of(area, "area", ["England and Wales", "England", "Wales"])
        trace.Area('{} Area code from row near top as "England and Wales", "England" or ' \
                    '"Wales".', var=excelRange(area))
        
        # Sex
        sex = leading_cause_code_header.shift(RIGHT).shift(RIGHT).expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Persons", "Males", "Females"])
        trace.Sex('{} dimension "Sex" taken from horizontal as "Persons", "Males" or "Females".', \
                  var=excelRange(sex))
        
        # Leading cause
        leading_cause = leading_cause_code_header.fill(DOWN).is_not_blank() - get_unwanted(tab)
        assert_continuous_sequence(leading_cause, UP)
        trace.Leading_cause("{} dimension 'Leading cause' taken as the CODES from column A", \
                           var=excelRange(leading_cause))
        
        obs = leading_cause.waffle(sex)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(leading_cause, "Leading cause", DIRECTLY, LEFT),
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDim(area, "Area", CLOSEST, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


for tab in tabs_from_named(tabs, ["Table 18"]):
    
    try:
        title, footnotes = get_title_and_footnotes(tab)
        footnotes_dict[tab.name] = footnotes
        
        columns=['Sex', 'Age Group', 'Pre-existing Condition', 'Area']
        trace.start(title, tab, columns, source_sheet)
        
        condition_header = tab.excel_ref('A').filter("Main pre-existing condition").assert_one()
            
        # Pre-existing condition
        condition = condition_header.fill(DOWN).is_not_blank() - get_unwanted(tab)
        assert_continuous_sequence(leading_cause, UP)
        trace.Pre_existing_Condition("{} dimension 'Pre-existing condition' taken " \
                                    " from column A", var=excelRange(condition))
        
        # Sex
        sex = condition_header.fill(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["All persons", "Males", "Females"])
        trace.Sex('{} dimension "Sex" taken from horizontal as "All persons", "Males", "Females"', \
                 var=excelRange(sex))
        
        # Age group
        age_group = condition_header.shift(DOWN).expand(RIGHT).is_not_blank() \
            | tab.excel_ref('B').filter("All persons").assert_one()
        trace.Age_Group('{} dimension "Age Group" taken from horizontal, plus the "All persons"' \
                       " entry from column B (as otherwise it would be blank).", var=excelRange(age_group))
        
        # Area
        assert "England and Wales" in tab.excel_ref("A2").value, "Expecting 'England and Wales' in cell A2"
        area = "England and Wales"
        trace.Area("Hard coding area to 'England and Wales'")
        
        obs = condition.waffle(age_group)
        
        dimensions = [
            HDim(sex, "Sex", CLOSEST, LEFT),
            HDim(age_group, "Age Group", DIRECTLY, ABOVE),
            HDim(condition, "Pre-existing Condition", DIRECTLY, LEFT),
            HDimConst("Area", area)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name, trace)
        
        # Codeify area column
        df["Area"] = df["Area"].apply(get_regions)
        trace.Area("Converted all area labels to 9 digit ONS codes.")
        
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Finish
#
# Output the tracing stuff, then wrangle it into markdown for the spec.

# +
trace.output()

# use the tracer to write some simple markdown for spec (because I'm lazy)
lines = ["----------### Stage 1. Transform", ""]
for title, details in trace._create_output_dict().items():
    for cube_title, cubes in details.items():   # ['sourced_from', 'id', 'tab', 'column_actions']
        lines.append("#### " + cube_title)
        lines.append("") 
        for cube in cubes:
            lines.append("#### Sheet: " + cube["tab"])
            lines.append("")
            for column in cube["column_actions"]:
                lines.append("{}".format(column["column_label"]))
                for comment in [",".join(list(x.values())) for x in column["actions"]]:
                    lines.append(comment)
                lines.append("")
            lines.append("")
            lines.append("#### Table structure")
            lines.append(", ".join([x["column_label"] for x in cube["column_actions"]]))
            lines.append("")
            lines.append("#### Footnotes")
            if cube["tab"] in footnotes_dict.keys():
                for note in list(footnotes_dict[cube["tab"]].values()):
                    lines.append(note)
            if cube["tab"] in comments:
                lines.append("")
                lines.append("#### DE notes")
                for comment in comments[cube["tab"]]:
                    lines.append(comment)
            lines.append("")
        lines.append("-----")

for l in lines:
    print(l)
# -

