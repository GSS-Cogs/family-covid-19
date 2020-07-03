# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## WG Attendance at local authority settings during the coronavirus  COVID-19  pandemic 


[Landing Page](https://gov.wales/attendance-local-authority-settings-during-coronavirus-covid-19-pandemic)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?wg-attendance-at-local-authority-settings-during-the-coronavirus-covid-19-pandemic/flowchart.ttl)

------

### Stage 1: Transform

#### Sheet: Table1_Eng

		A - Date
		B - Settings
		C - Percentage of Settings
		D - Children
		E - Percentage of Children
		F - Vulnerable Children
		G - Percentage of Vulnerable Children
		H - Staff
		I - Percentage of Staff

#### Sheet: Table2_Eng

		A - Week Beginning
		B - Week Ending
		C - Settings
		D - Percentage of Settings
		E - Children
		F - Percentage of Children
		G - Vulnerable Children
		H - Percentage of Vulnerable Children
		I - Staff
		J - Percentage of Staff

---------

### Stage 2: Alignment

#### Sheet: Table1_Eng

		Date to be renamed Period
		Column in range B4:I4 to be flattened with column name: Local Authority Settings

#### Sheet: Table2_Eng

		Week Beginning and Week Ending to be formatted into one column renamed Period
		Column in range C4:J4 to be flattened with column name: Local Authority Settings

#### Table Joins

		Both tables to be joined and output with name: 
			Attendance at local authority settings during the coronavirus COVID-19 pandemic.csv

#### Table Structure

		Period, Local Authority Settings, Measure Type, Unit, Value, Marker

##### DM Notes

		Vamshi had already completed the transform before a spec had been written so this is a post-spec
