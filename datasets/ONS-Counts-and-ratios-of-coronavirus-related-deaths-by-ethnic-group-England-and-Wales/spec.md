# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## ONS Counts and ratios of coronavirus-related deaths by ethnic group, England and Wales 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/countsandratiosofcoronavirusrelateddeathsbyethnicgroupenglandandwales)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Counts-and-ratios-of-coronavirus-related-deaths-by-ethnic-group-England-and-Wales/flowchart.ttl)


------

### Stage 1: Transform

#### Sheet: Table 1

		A - Ethnicity
		B - Sex
		C - Ageband
		D - Counts of Coronavirus-related deaths
		
#### Sheet: Table 2

		A - Ethnicity
		B - Sex
		C - Ageband
		D - Ratio of Coronavirus-related deaths to non Coronavirus-related
		

---------

### Stage 2: Alignment

#### Sheet: Table1_Eng

		Counts of Coronavirus-related deaths is the Value column with Count put in Measure Type and Deaths in Unit columns	

#### Sheet: Table2_Eng

		Ratio of Coronavirus-related deaths to non Coronavirus-related is the Value column with Ratio put in Measure Type and Deaths in Unit columns
		

#### Table Joins

		Both tables to be joined and output with name: 
			ons-counts-and-ratios-of-coronavirus-related-deaths-by-ethnic-group-england-and-wales.csv

#### Table Structure

		Ethnicity, Sex, Age band, Value, Measure Type, Unit

##### DM Notes

		Transform had already been completed before a spec had been written so this is a post-spec
