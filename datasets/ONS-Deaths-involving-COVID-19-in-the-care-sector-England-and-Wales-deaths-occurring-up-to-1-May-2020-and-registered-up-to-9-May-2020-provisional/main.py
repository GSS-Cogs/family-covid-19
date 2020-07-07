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
print("Using source data", scraper.distribution(latest=True).downloadURL)
scraper 


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
        
def create_tidy(cs, tab_name):
    """Wrap some standard operations to avoid repeating ourselves"""
    df = cs.topandas().fillna("")

    # rename stuff
    df = df.rename(columns={"OBS":"Value", "DATAMARKER":"Marker"})
        
    # Markers, measures and output
    df = apply_measures(df, tab_name)
    df = apply_markers(df, tab_name)

    return df

def get_title_and_comments(tab):
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
    
    return title, footnotes


def find_source_cell(tab):
    """what is says"""
    return tab.excel_ref('A').filter(lambda x: str(x.value).startswith("Source:")).assert_one()
    
def get_unwanted(tab):
    """return anything level with or below the source cell"""
    return find_source_cell(tab).expand(DOWN).expand(RIGHT)

# TODO
def apply_measures(df, tab_name):
    """Given a dataframe and the source tab name, add the correct measure types"""
    return df

# TODO
def apply_markers(df, tab_name):
    """Given a dataframe and the source tab name, add the correct marker codes"""
    return df


# -

# ## Transform: Table 1

for tab in tabs_from_named(tabs, "Table 1"):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        # Start with the date title cell
        date_cell = tab.excel_ref('A').filter("Date").assert_one()

        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime))
        assert_continuous_sequence(period, UP)

        # Category
        category = date_cell.fill(RIGHT).is_not_blank()
        assert_one_of(category, "category", ["Deaths involving COVID-19", "All deaths", "2019 Comparison"])

        # Source
        source = date_cell.shift(UP).fill(RIGHT).is_not_blank()
        assert_one_of(source, "source", ["England and Wales (ONS data)", "England (ONS data)", 
                               "England (CQC data)", "Wales (ONS data)", "Wales (CIW data)"])
        # observations
        obs = date_cell.shift(DOWN).shift(RIGHT).expand(DOWN).expand(RIGHT).is_not_blank().is_not_whitespace()
        assert_numeric_or_marker(obs, [":"])
    
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(category, "Category", DIRECTLY, ABOVE),
            HDim(source, "Source", CLOSEST, LEFT),
            HDimConst("Geograpahy", "K0300001")
        ]

        cs = ConversionSegment(obs, dimensions)
        df = cs.topandas().fillna("")

        # rename stuff
        df = df.rename(columns={"OBS":"Value", "DATAMARKER":"Marker"})
        
        # Markers, measures and output
        df = apply_measures(df, tab.name)
        df = apply_markers(df, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e      


# ## Transform: Table 2


for tab in tabs_from_named(tabs, "Table 2"):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        # Start with the first persons cell
        first_persons_cell = tab.excel_ref('B').filter("Persons").assert_one()

        # Sex
        sex = first_persons_cell.expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Persons", "Male", "Female"])
        
        # Geography
        geography = first_persons_cell.shift(UP).shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(geography, "geography", ["England and Wales", "England", "Wales"])
        
        # Age
        age = tab.excel_ref('A').filter('All ages').expand(DOWN).is_not_blank() - get_unwanted(tab)
        assert_one_of(age, "Age", ["All ages", "0-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"])
        
        # observations
        obs = first_persons_cell.shift(DOWN).expand(DOWN).expand(RIGHT).is_not_blank() \
                .is_not_whitespace() - get_unwanted(tab)
        assert_numeric_or_marker(obs, [":"])
    
        dimensions = [
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(geography, "Geography", CLOSEST, LEFT),
        ]

        cs = ConversionSegment(obs, dimensions)
        df = cs.topandas().fillna("")

        # rename stuff
        df = df.rename(columns={"OBS":"Value", "DATAMARKER":"Marker"})
        
        # Markers, measures and output
        df = apply_measures(df, tab.name)
        df = apply_markers(df, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)

    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e

# ## Transform: Tables 3 & 4

# +
cubes34 = []
cubes34_title = "Number of deaths, age standardised and age specific mortality rates, by sex"
for tab in tabs_from_named(tabs, ["Table 3", "Table 4"]):
    
    try:
        first_death_cells = tab.excel_ref('B').filter("Number of deaths")
        assert len(first_death_cells) == 4, "Aborting, there should be exactly 4 'Number of deaths' cells"
    
        ignore_for_obs = \
            first_death_cells.expand(RIGHT) | \
            first_death_cells.shift(UP).expand(RIGHT) | \
            first_death_cells.shift(UP).shift(UP).expand(RIGHT)                                 
        
        # Sex
        sex = first_death_cells.by_index(1).shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Person", "Male", "Female"])
        
        # Attributes to pivot later
        attributes = first_death_cells.by_index(1).expand(RIGHT).is_not_blank()

        category = tab.excel_ref('A').filter(starts_with("Number of deaths"))
        assert len(category) == 4, "We are expecting 4 categories beginner 'Numbers of deaths' in column A"
        
        # need to use a specific line for closest to avoid equally valid lookups
        geography = first_death_cells.by_index(1).shift(UP).shift(UP)
        
        # Obs should be anything outisde of column A that's not selected elsewhere
        obs = first_death_cells.expand(DOWN).expand(RIGHT).is_not_blank() - ignore_for_obs
        assert_numeric_or_marker(obs, [":"])
              
        obs_in_b = obs.filter(lambda x: x.x == 1)
        age = tab.excel_ref('A1').waffle(obs_in_b)
        
        dimensions = [
            HDim(sex, "Sex", CLOSEST, LEFT),
            HDim(attributes, "TEMP_FOR_ATTRIBUTES", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(geography, "Geography", CLOSEST, ABOVE),
            HDim(category, "Category", CLOSEST, ABOVE)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        
        # Make a hacky composite key
        df["Composite"] = ""
        for col in ["Sex", "Age", "Geography", "Category"]:
            df["Composite"] = df["Composite"] + df[col]
        
        # Use that composite key to match attributes to obs
        for attribute in ["Rate", "Lower 95% CI", "Upper 95% CI"]:
            df[attribute] = ""
            for _, row in df[df["TEMP_FOR_ATTRIBUTES"] == attribute].iterrows():
                df[attribute][df["Composite"] == row["Composite"]] = row["Value"]
                
        # Tidy up temporary nonsence
        df = df.drop(["Composite", "TEMP_FOR_ATTRIBUTES"], axis=1)

        cubes34.append(df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cubes34_title}' from tab '{tab.name}'.") from e
        
df = pd.concat(cubes34)
df.to_csv("{}.csv".format(pathify(cubes34_title)), index=False)
# -
# ## Transform: Table 5, 6

# +
cubes56 = []
cubes56_title = "Number of deaths of care home residents by place of death"
for tab in tabs_from_named(tabs, ["Table 5", "Table 6"]):
    
    try:
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        
        # Geography
        geography = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(geography, "geography", ["England and Wales", "England", "Wales"])
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Care Home", "Hospital", "Elsewhere"])
        
        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(geography, "Geography", CLOSEST, LEFT),
            HDim(place_of_death, "Place of death", DIRECTLY, ABOVE),
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        cubes56.append(df)
    
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cubes56_title}' from tab '{tab.name}'.") from e
        
df = pd.concat(cubes56)
df.to_csv("{}.csv".format(pathify(cubes56_title)), index=False)
# -

# ## Transform: Table 7,8

# +
cubes78 = []
cubes78_title = "Number of deaths of care home residents notified to the Care Quality Commission"
for tab in tabs_from_named(tabs, ["Table 7", "Table 8"]):
    
    try:
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Care Home", "Hospital", "Elsewhere", "Not Stated"])
        
        # Cause of death
        category_of_death = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(category_of_death, "category_of_death", ["All deaths", "COVID-19"])
        
        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(place_of_death, "Place of Death", DIRECTLY, ABOVE),
            HDim(category_of_death, "Category Of Death", CLOSEST, LEFT),
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        cubes78.append(df)

    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cubes78_title}' from tab '{tab.name}'.") from e

df = pd.concat(cubes78)
df.to_csv("{}.csv".format(pathify(cubes78_title)), index=False)
# -

# ## Transform: Table 9

for tab in tabs_from_named(tabs, ["Table 9"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        period = period | tab.excel_ref("A").filter("Total").assert_one() # Add the non date total
        assert_continuous_sequence(period, UP)
        
        # Place of death
        place_of_death = date_cell.fill(RIGHT).is_not_whitespace()
        assert_one_of(place_of_death, "place_of_death", ["Home care", "Hospital", "Elsewhere", "Not Stated"])
        
        # Cause of death
        category_of_death = date_cell.shift(UP).expand(RIGHT).is_not_whitespace()
        assert_one_of(category_of_death, "category_of_death", ["All deaths", "COVID-19"])
        
        obs = period.waffle(place_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(place_of_death, "Place of Death", DIRECTLY, ABOVE),
            HDim(category_of_death, "Category Of Death", CLOSEST, LEFT),
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)

    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Table 10

for tab in tabs_from_named(tabs, ["Table 10"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        date_cell = tab.excel_ref("A").filter("Date").assert_one()
        
        # Period
        period = date_cell.fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        assert_continuous_sequence(period, UP)
        
        # Category
        category = date_cell.fill(RIGHT).is_not_blank()
        assert_one_of(category, "category", ["Care home resident", "Home care service user"])
        
        obs = category.waffle(period)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(category, "Category", DIRECTLY, ABOVE),
            HDim(period, "Period", DIRECTLY, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Table 11

for tab in tabs_from_named(tabs, ["Table 11"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        first_region = tab.excel_ref("B").filter("East").assert_one()
        
        # Period
        period = first_region.shift(LEFT).fill(DOWN).filter(is_type(datetime.datetime)) - get_unwanted(tab)
        assert_continuous_sequence(period, UP)
        
        # Area
        area = first_region.expand(RIGHT).is_not_blank()
        assert_one_of(area, "area", ["East", "East Midlands", "London", "North East", "North West", 
                                     "South East", "South West", "West Midlands",
                                     "Yorkshire and the Humber", "Wales"])
        
        # Category of death
        category_of_death = first_region.shift(UP).expand(RIGHT).is_not_blank()
        assert_one_of(category_of_death, "category_of_death", ["All deaths", "Deaths involving COVID-19"])
        
        obs = period.waffle(area)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(category_of_death, "Category of death", CLOSEST, LEFT),
            HDim(period, "Period", DIRECTLY, LEFT),
            HDim(area, "Area", DIRECTLY, ABOVE)
        ]

        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Transform: Tables 12 & 13

# +
cube12n13 = []
cube12n13_title = "Number of weekly deaths of care home residents by local authority"
for tab in tabs_from_named(tabs, ["Table 12", "Table 13"]):
    
    try:
        
        area_code_header = tab.excel_ref('A').filter("Area Code").assert_one()
        
        week_no = area_code_header.shift(UP).expand(RIGHT).is_not_blank()
        
        area = area_code_header.fill(DOWN).regex("[A-Z]{1}\d{8}")
        assert_continuous_sequence(area, UP)
        
        period = area_code_header.fill(RIGHT).is_not_blank()
        assert_continuous_sequence(period, RIGHT)
        
        obs = area.shift(RIGHT).waffle(period - tab.excel_ref('B'))
        assert_numeric_or_marker(obs, [":"])
        
        death_involved_covid = "Yes" if tab.name.strip() == "Table 12" else "No"
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", DIRECTLY, ABOVE),
            HDimConst("Covid-19 Involvement", death_involved_covid)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        cube12n13.append(df)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube12n13}' from tab '{tab.name}'.") from e

df = pd.concat(cube12n13)
df.to_csv("{}.csv".format(pathify(cube12n13_title)), index=False)
# -

# ## Tables 14 & 15

# +
cube14n15 = []
cube14n15_title = "Number of weekly deaths of care home residents by local authority"
for tab in tabs_from_named(tabs, ["Table 14", "Table 15"]):
    
    try:
        
        # We're gonna anchor to the first instance of "England" in column A
        # that's a bit flimsy so we'll double confirm it
        big_england = tab.excel_ref('A').filter("England").assert_one()
        big_england2 = tab.excel_ref('A').is_not_blank().by_index(3)
        assert big_england == big_england2, "England needs to be the first area in column A, got" \
                                " '{}'.".format(big_england2.value)
        
        unwanted_cells = tab.excel_ref('A').filter(lambda x: str(x.value).startswith("Source")) \
                            .assert_one().expand(DOWN).expand(RIGHT)
        
        week_no = big_england.shift(UP).shift(UP).expand(RIGHT)
        
        area = big_england.expand(DOWN) - get_unwanted(tab)
        assert_continuous_sequence(area, UP)
        
        period = big_england.shift(UP).fill(RIGHT).is_not_blank()
        assert_continuous_sequence(period, RIGHT)
        
        obs = area.shift(RIGHT).waffle(period - tab.excel_ref('B'))
        assert_numeric_or_marker(obs, [":"])
        
        death_involved_covid = "Yes" if tab.name.strip() == "Table 15" else "No"
        
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", DIRECTLY, ABOVE),
            HDimConst("Covid-19 Involvement", death_involved_covid)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        
        # Where the period is "Grand Total" set the week no to "All"
        assert "Grand total" in df["Period"].unique(), "The label 'Grand total' is expected and required"
        df["Week Number"][df["Period"] == "Grand total"] = "All"
        
        cube14n15.append(df)
    
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{cube14n15_title}' from tab '{tab.name}'.") from e

df = pd.concat(cube14n15)
df.to_csv("{}.csv".format(pathify(cube14n15_title)), index=False)
# -

# ## Table 16

for tab in tabs_from_named(tabs, ["Table 16"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        area_code_header = tab.excel_ref('A').filter("Area Code")
        
        area = area_code_header.fill(DOWN).regex("[A-Z]{1}\d{8}")
        assert_continuous_sequence(area, UP)
        
        category_of_death = area_code_header.shift(RIGHT).fill(RIGHT).is_not_blank()
        assert_continuous_sequence(category_of_death, RIGHT)
        assert_one_of(category_of_death, "category_of_death", ["All deaths", "COVID-19"])

        period = area_code_header.shift(UP).fill(RIGHT).is_not_blank()
        
        week_no = category_of_death.shift(UP).shift(UP).expand(RIGHT).is_not_blank()
        
        obs = area.waffle(category_of_death)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(period, "Period", CLOSEST, LEFT),
            HDim(area, "Area", DIRECTLY, LEFT),
            HDim(week_no, "Week Number", CLOSEST, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


# ## Table 17


for tab in tabs_from_named(tabs, ["Table 17"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        leading_cause_code_header = tab.excel_ref('A').filter("Leading cause code").assert_one()
        
        # Area
        area = leading_cause_code_header.shift(UP).fill(RIGHT).is_not_blank()
        assert_one_of(area, "area", ["England and Wales", "England", "Wales"])
        
        # Sex
        sex = leading_cause_code_header.shift(RIGHT).shift(RIGHT).expand(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["Persons", "Males", "Females"])
        
        # Leading cause
        leading_cause = leading_cause_code_header.fill(DOWN).is_not_blank() - get_unwanted(tab)
        assert_continuous_sequence(leading_cause, UP)
        
        obs = leading_cause.waffle(sex)
        assert_numeric_or_marker(obs, [":"])
        
        dimensions = [
            HDim(leading_cause, "Leading cause", DIRECTLY, LEFT),
            HDim(sex, "Sex", DIRECTLY, ABOVE),
            HDim(area, "Area", CLOSEST, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e


for tab in tabs_from_named(tabs, ["Table 18"]):
    
    try:
        title, footnotes = get_title_and_comments(tab)
        
        condition_header = tab.excel_ref('A').filter("Main pre-existing condition").assert_one()
            
        # Pre-existing condition
        condition = condition_header.fill(DOWN).is_not_blank() - get_unwanted(tab)
        assert_continuous_sequence(leading_cause, UP)
        
        # Sex
        sex = condition_header.fill(RIGHT).is_not_blank()
        assert_one_of(sex, "sex", ["All persons", "Males", "Females"])
        
        # Age group
        age_group = condition_header.shift(DOWN).expand(RIGHT).is_not_blank() \
            | tab.excel_ref('B').filter("All persons").assert_one()
        
        obs = condition.waffle(age_group)
        
        dimensions = [
            HDim(sex, "Sex", CLOSEST, LEFT),
            HDim(age_group, "Age Group", DIRECTLY, ABOVE),
            HDim(condition, "Pre-existing Condition", DIRECTLY, LEFT)
        ]
        
        cs = ConversionSegment(obs, dimensions)
        df = create_tidy(cs, tab.name)
        df.to_csv("{}.csv".format(pathify(title)), index=False)
        
    except Exception as e:
        raise Exception(f"Problem encountered processing cube '{title}' from tab '{tab.name}'.") from e





