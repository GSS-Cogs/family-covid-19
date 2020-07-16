# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------
## PHE COVID-19  number of outbreaks in care homes – management information 

[Landing Page](https://www.gov.uk/government/statistical-data-sets/covid-19-number-of-outbreaks-in-care-homes-management-information#history)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?PHE-COVID-19-number-of-outbreaks-in-care-homes-–-management-information/flowchart.ttl)

----------
### Stage 1. Transform

#### Sheet: 1 & 2

		Week Commencing
		Region
		Categorised by
		Area Code
		All outbreaks	
		Number of care homes	
		Percentage of care homes that have reported an outbreak

#### Sheet: 3 & 4

		Week Commencing
		Region
		Categorised by
		Area Code
		All outbreaks	
		Number of care homes	
		
		"Government Office Region": remove column

-------------
### Stage 2. Harmonise

#### Tables joined up into one dataset in stage 1

		"Region": remove column
		"Categorised by": change name to "Care Home Region"
		
		The values for the following 2 columns are based on the overall time period rather than individual weeks
		"All Outbreaks": remove column and make it part of overall data with values
			"Period": (Max-Date - Min-Date)
			"Area Code": as per RGN09CD column
			"Care Home Region": value as per sheet name
			"Measure Type": Outbreaks of COVID-19
			"Unit": Count
		"Percentage of care homes that have reported an outbreak": remove column and make part of overall data with values:
			"Period": (Max-Date - Min-Date)
			"Area Code": as per RGN09CD column
			"Care Home Region": value as per input sheet name
			"Measure Type": Outbreaks of COVID-19
			"Unit": Percent

----------
#### Table Structure

		Period, Care Home Region, Area code, Number of care homes, Measure Type, Marker, Unit, Value

--------------
##### Footnotes

		footnotes

##### DM Notes

		notes

