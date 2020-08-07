# -*- coding: utf-8 -*-
# # ONS Personal and economic well-being in Great Britain 

from gssutils import * 
import json 
import pandas as pd
import datetime
import dateutil.parser


# ## Helpers

# +

def tabs_from_named(tabs, wanted):
    """Given all labs and a list of tab names wanted, return the ones we want, raise if they're not here"""
    wanted = [wanted] if not isinstance(wanted, list) else wanted
    wanted_tabs = [x for x in tabs if x.name.strip() in wanted]
    assert len(wanted_tabs) == len(wanted), \
        f"Could not find tab name {','.join(wanted)} in tabs {','.join([x.name for x in tabs])}"
    return wanted_tabs

def format_period(time_str):
    """
    turns day & month, eg 12th June 2020 into 6-12-2020
    /id/gregorian-interval/{dateTime}/{duration}
    """
    try:
        time_str = time_str.replace("th", "").replace("rd", "").replace("–", "-")
        start = " ".join(time_str.split(" ")[:2]) + " 2020"
        end = " ".join(time_str.split(" ")[-2:]) + " 2020"
        
        start_as_dtime = dateutil.parser.parse(start)
        end_as_dtime = dateutil.parser.parse(end)
        duration = end_as_dtime - start_as_dtime

        interval = "gregorian-interval/" + start_as_dtime.strftime('%Y-%m-%dT00:00:00') + "/" + str(duration.days) + "D"
        return interval
    except Exception as e:
        raise Exception("The value {} failed.".format(time_str)) from e
        
def assert_one_of(cells, name_of_selection, expected):
    """Given a list of acceptable values, blow up if we get something else"""
    for cell in cells:
        if cell.value not in expected:
            if cell.value.strip() in expected:
                logging.warning(f"When asserting '{name_of_selection}' we matched cell '{cell}' to expected, but with rogue whitepace detected.")
            else:    
                raise AssertionError(f"When asserting '{name_of_selection}' the cell '{cell}' does not contain a value from {','.join(expected)}")
        


# +

scraper = Scraper(seed="info.json") 
scraper 
# -

dist = scraper.distribution(latest=True)
tabs = dist.as_databaker()
dist


# +
# NOTE - the above 'downloadURL' is the source data we're transforming here.
# -

# # Personal Well Being
#
# Personal well being is split across two tabs:
# * tab1 - the first 4 tables as the observations
# * tab2 - 4 tables providing the upper and lower vi calues for those 4 tables.
#
# We're going to extract both tabs then inner join the CI values onto the main obervations table.
#
# * TODO - still need to get the lower tables on this tab.
# * TODO - need to extract the footnotes for each table.
# * TODO - current overriding "Mean Average Estimate" to "Mean Average" in all cases, need to capture that nuance somehow without wrecking the cube.

# +

# Personal Well Being
# i.e the tope 4 tables from the first two tabs
    
def extract(tab_name, take_ci):
    """
    Extraction code for a named tab (one of the first two tabs)
    If take_ci is true also extract the CI header row, otherwise the structures (and therefore the code) is identical.
    """
    
    for tab in tabs_from_named(tabs, tab_name):

        sub_tabs = []
        for wellbeing_measure in ["Life satisfaction in Great Britain", "Worthwhile in Great Britain", "Happiness in Great Britain", "Anxiety in Great Britain"]:

            measure_of_wellbeing = tab.excel_ref('A').filter(starts_with(wellbeing_measure)).assert_one()

            # 'Mean Average' is a cell lower on one of the tabs.
            try:
                anchor = measure_of_wellbeing.shift(1,2).filter(contains_string("Mean Average")).assert_one()
            except AssertionError:
                anchor = measure_of_wellbeing.shift(1,3).filter(contains_string("Mean Average")).assert_one()
                
            rating = anchor.expand(RIGHT).is_not_blank()
            score = rating.shift(DOWN).is_not_blank() | anchor

            unwanted = anchor.shift(LEFT).fill(DOWN).filter(starts_with("Source:")).by_index(1).assert_one().expand(RIGHT).expand(DOWN)

            period = anchor.shift(LEFT).fill(DOWN).is_not_blank() - unwanted

            if take_ci:
                ci = anchor.shift(0, 2).expand(RIGHT).is_not_blank()
                assert_one_of(ci, "ci", ["Lower Interval", "Upper Interval"])
                
            if take_ci:
                observations = period.waffle(ci)
            else:
                observations = period.waffle(score)
                
            dimensions = [
                HDim(period, "Period", DIRECTLY, LEFT),
                HDim(rating, "Rating", CLOSEST, LEFT, cellvalueoverride={"Mean Average Estimate": "Mean Average"}),
                HDim(score, "Score", CLOSEST, LEFT,cellvalueoverride={"Mean Average Estimate": "Mean Average"}),
                HDimConst("Measure of Wellbeing", [x.value for x in measure_of_wellbeing][0])
            ]
            
            if take_ci:
                dimensions.append(HDim(ci, "CI", DIRECTLY, ABOVE))
            
            cs = ConversionSegment(observations, dimensions)
            sub_tabs.append(cs.topandas())
        
        df = pd.concat(sub_tabs)
    
        # period
        df["Period"] = df["Period"].map(lambda x: x.split("(")[1].split(")")[0])
        df["Period"] = df["Period"].astype(str).apply(format_period)

        # wellbeing measure
        for wb in df["Measure of Wellbeing"].unique().tolist():
            assert "in Great Britain" in wb, "Aborting, expecting the phrase 'in Great Britain' in all values of column" \
                            " 'Measure of Wellbeing', instead got: {}.".format(wb)

        df["Measure of Wellbeing"] = df["Measure of Wellbeing"].map(lambda x: x.split("in Great Britain")[0].strip())
        
        return df

# Extract the tabs
obs_df = extract(["Overall population"], False)
print("DF length before joins:", len(obs_df))
ci_df = extract(["Personal well-being QMI"], True)

# Add a hacky composite key to each row of the dfs, discount the CI and OBS columnsfrom this
for df in [obs_df, ci_df]:
    df["ckey"] = ""
    for col in df.columns.values:
        if col != "CI" and col != "OBS":
            df["ckey"] = df["ckey"]+df[col]

# Split ci_df into upper and lower dataframers
lower_ci_df = ci_df[ci_df["CI"] == "Lower Interval"]
upper_ci_df = ci_df[ci_df["CI"] == "Upper Interval"]


# JOIN LOWER CI

df = pd.merge(obs_df,lower_ci_df,on='ckey')
# Rename stuff, drop columns we have two copies of
rename_dict = {"OBS_y": "Lower CI", "OBS_x": "OBS"}
drop_me = []
for col in df.columns.values.tolist():
    if not col.startswith("OBS") and col != "ckey":
        if col.endswith("_x"):
            rename_dict.update({col: col.replace("_x", "")})
        else:
            drop_me.append(col)

# drop unwaned and do renaming
df = df.drop(drop_me, axis=1)
df = df.rename(columns=rename_dict)

# JOIN UPPER CI

df = pd.merge(df,upper_ci_df,on='ckey')
# Rename stuff, drop columns we have two copies of
rename_dict = {"OBS_y": "Upper CI", "OBS_x": "Value"}
drop_me = []
for col in df.columns.values.tolist():
    if not col.startswith("OBS") and col != "Lower CI":
        if col.endswith("_x"):
            rename_dict.update({col: col.replace("_x", "")})
        else:
            drop_me.append(col)

# drop unwaned and do renaming
df = df.drop(drop_me, axis=1)
df = df.rename(columns=rename_dict)
print("DF length after joins:", len(df))
      
df
# -

