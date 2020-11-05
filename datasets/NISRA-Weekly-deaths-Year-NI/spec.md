# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Development](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

-----

## NISRA Weekly deaths, Year  NI 

### Northern Ireland Statistics and Research Agency

-------

[Landing Page](https://www.nisra.gov.uk/statistics/ni-summary-statistics/coronavirus-covid-19-statistics)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NISRA-Weekly-deaths-Year-NI/flowchart.ttl)

--------

### 1. Scrape and Transform

#### Sheet: Weekly Deaths_2020 - Deaths registered each week in Northern Ireland 2020

		A - Registration Week
		B - Week Ending (Friday)
		C4:I4 - Registered Death Type (Codelist)
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column

##### Table Structure

		Registration Week, Week Ending, Registered Death Type, Measure Type, Unit, Marker, Value

#### Sheet: Weekly Deaths_Age by Gender - Deaths registered each week in Northern Ireland 2020

		A - Gender
		B - Age (Codelist)
		C3:V3 - Week Number
		C4:V4 - Week Ending (Friday) - C3:4 to be given just the year or a date range
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Gender, Age, Week Number, Week Ending, Measure Type, Unit, Marker, Value

#### Sheet: Weekly_Deaths_by_LGD - Deaths registered in Northern Ireland by Local Government District (LGD)

		A - Registration Week
		B - Week Ending (Friday)
		C4:N4 - Local Government District (Codelist or Geography code)
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Registration Week, Week Ending, Local Government District, Measure Type, Unit, Marker, Value

#### Sheet: Covid-19_Deaths_age by Gender - Covid-19 Deaths registered each week in Northern Ireland, age by Gender

		A - Gender
		B - Age (Codelist)
		C3:L3 - Week Number
		C4:L4 - Week Ending (Friday) - C3:4 to be given just the year or a date range
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Gender, Age, Week Number, Week Ending, Measure Type, Unit, Marker, Value

#### Sheet: Covid-19_Deaths_by_LGD - Covid-19 Deaths registered in Northern Ireland by Local Government District (LGD)

		A - Registration Week
		B - Week Ending (Friday)
		C4:N4 - Local Government District (Codelist or Geography code)
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Registration Week, Week Ending, Local Government District, Measure Type, Unit, Marker, Value

#### Sheet: Covid-19_Reg Date & POD - Covid-19 Deaths registered in Northern Ireland by Place of Death

		A - Week of Death
		B - Week Ending (Friday)
		C3:H3 - Place of Death (Codelist)
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Week of Death, Week Ending, Place of Death, Measure Type, Unit, Marker, Value

#### Sheet: Covid-19 by Week of Death - Covid-19 Death Occurrences by week of death in Northern Ireland 

		A - Week of Death
		B - Week Ending (Friday)
		C3:H3 - COVID-19 Deaths (Codelist)
		Measure Type = Deaths
		Unit - Count and Cumulative Count
		Put Provisional in Marker column
		
##### Table Structure

		Week of Death, Week Ending, COVID-19 Deaths, Measure Type, Unit, Marker, Value
		
#### Sheet: Covid-19 Occurrence Date & POD - Covid-19 Death Occurrences in Northern Ireland by week of death and Place of Death

		A - Week of Death
		B - Week Ending (Friday)
		C3:H3 - Place of Death (Codelist)
		Measure Type = Deaths
		Unit - Count
		Put Provisional in Marker column
		
##### Table Structure

		Week of Death, Week Ending, Place of Death, Measure Type, Unit, Marker, Value

#### Sheet: Covid-19 Date of Death & POD - Covid-19 Death Occurrences by date and Place of Death in Northern Ireland

		A - Date
		B3:H3 - Place of Death (Codelist)
		Measure Type = Deaths
		Unit - Count and Cumulative Count
		Put Provisional in Marker column
		
##### Table Structure

		Date, Place of Death, Measure Type, Unit, Marker, Value
				
--------

### 2. Harmonise

### Dataset One - Registrations

#### Sheet: Table 1

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	Remove superscripts from 'Measurement' column values, rename 'Death Measurement Type' (codelist/pathify)
	Set 'Value' column to 0 where 'Marker' column = '-'
	Replace NaNs in 'Marker' column with empty string

	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Place of death' column with value 'total'
	Add 'Cause of death' column with value 'all'

#### Sheet: Table 2

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Set 'Year to date' cell with range from Sat 4st Jan 2020 to max date in 'Week Ending' column
	Gender: Male = T, Female = M, All = T, Total = T, Unknown = U
	Age: codelist/pathify
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code

	Add 'Place of death' column with value 'total'
	Add 'Cause of death' column with value 'all'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 3

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography codes, set Total to Northern Ireland code
	
	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Place of death' column with value 'total'
	Add 'Cause of death' column with value 'all'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 4

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography codes	
	Remove superscripts from 'Place of death' column values

	Add 'Age' column with value 'all'
	Add 'Gender' column with valuecovid-19-related 'T'
	Add 'Cause of death' column with value 'all'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 5

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Set 'Year to date' cell with range from Sat 4st Jan 2020 to max date in 'Week Ending' column
	Rename column 'OBS' to 'Value'
	Gender: Male = T, Female = M, All = T, Total = T, Unknown = U
	Age: codelist/pathify

	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Place of death' column with value 'total'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 6

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Set 'Area' column to ONS Geography codes, set Total to Northern Ireland code
	Rename column 'OBS' to 'Value'
	
	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Place of death' column with value 'total'
	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 7

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	'Place of death': Remove superscripts (codelist/pathify)

	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 8

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Set 'Area' column to ONS Geography codes, set Total to Northern Ireland code
	Rename column 'OBS' to 'Value'

	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Place of death' column with value 'care-home'
	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered in Week'

#### Sheet: Table 9

	Ignore Cumulative Total
	Set Period to day interval
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	'Place of death':(codelist/pathify)

	Add 'Age' column with value 'all'
	Add 'Gender' column with value 'T'
	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Death Measurement Type' column with value 'Total Number of Deaths Registered on Day'
	
#### Table Structure

	Period, Death Measurement Type, Area, Gender, Age, Place of death, Cause of death, DataMarker, Value
	

#### JOIN Tables 1 to 9

	Rename 'Week Ending' columns as 'Period'
	Add 'Marker' columns where needed and rename 'Datamarker' columns to Marker
	Remove 'Average Count' data for now as we still can't have multiple measures
	Remove Measure Type and Unit column as these will be defined in info.json

	info.json
		Measure Type: count	
		Unit: deaths

	Scraper:
		Title: Weekly deaths - Registrations		
		Comment:  Weekly and daily death registrations in Northern Ireland including COVID-19 related deaths
		Description: Weekly and daily death registrations in Northern Ireland including COVID-19 related deaths 
			Care Home deaths includes deaths in care homes only. Care home residents who have died in a different location will not be counted in this table. 
			+ footnotes below
		Family: covid-19
		dataset_id:


### Dataset Two - Occurrences

#### Sheet: Table 10

	Ignore Cumulative Number
	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code

	Add 'Place of death' column with value 'total'
	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Residential setting' column with value 'all'
	
#### Sheet: Table 11

	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	'Place of death': remove superscripts (codelist/pathify)

	Add 'Cause of death' column with value 'covid-19-related'
	Add 'Residential setting' column with value 'all'

#### Sheet: Table 12

	Ignore Cumulative Total
	Set Period to day interval
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	Add 'Place of death' columns with values 'care-home', 'hospital', 'total' as per sheet

	Add 'Residential setting' column with value 'care-home'
	Add 'Cause of death' column with value 'covid-19-related'

#### Sheet: Table 13

	Ignore percentages
	Set week ending to the previous Saturday and format as a gregorian-interval - 7 days
	Rename column 'OBS' to 'Value'
	Set 'Area' column to ONS Geography Northern Ireland code
	'Place of death': remove superscripts (codelist/pathify)

	Add 'Cause of death' column with value 'covid-19-related
	Add 'Residential setting' column with value 'all'

#### Table Structure

	Period, Area, Place of death, Cause of death, Residential setting, DataMarker, Value

#### JOIN Tables 10 to 13

	Rename 'Week Ending' columns as 'Period'
	Add 'Marker' columns where needed and rename 'Datamarker' columns to Marker
	Remove Measure Type and Unit column as these will be defined in info.json or a dict , which is passed to the CSVMapping class.

	info.json
		Measure Type: count	
		Unit: deaths

	Scraper:
		Title: Weekly deaths - Occurrences
		Comment: Weekly and daily death occurrences in Northern Ireland including COVID-19 related deaths
		Description: Weekly and daily death occurrences in Northern Ireland including COVID-19 related deaths 
			This data is based on the actual date of death, from those deaths registered by GRO. All data in this table are subject to change, as some deaths will have occurred but haven’t been registered yet.
			Care home residents have been identified where either (a) the death occurred in a care home, or (b) the death occurred elsewhere but the place of usual residence of the deceased was recorded as a care home. It should be noted that the statistics will not capture those cases where a care home resident died in hospital or another location and the usual address recorded on their death certificate is not a care home. 
			+ footnotes below
		Family: covid-19
		dataset_id:

--------------
	
### Footnotes

	To meet user needs, NISRA publish timely but provisional counts of death registrations in Northern Ireland in our Weekly Deaths provisional dataset. Weekly totals are presented alongside a 5-year, weekly average as well as the minimum and maximum number of deaths for the same week over the last five years. To allow time for registration and processing, these figures are published 7 days after the week ends.
	Because of the coronavirus (COVID-19) pandemic, from 3rd April 2020, our weekly deaths release has been supplemented with the numbers of respiratory deaths (respiratory deaths include any death where Pneumonia, Bronchitis, Bronchiolitis or Influenza was mentioned anywhere on the death certificate); and deaths relating to COVID-19 (that is, where COVID-19 or suspected COVID-19 was mentioned anywhere on the death certificate, including in combination with other health conditions). The figures are presented by age group and sex.
	
	Find latest report here:
	https://www.nisra.gov.uk/publications/weekly-deaths

	Weekly published data are provisional.
	The majority of deaths are registered within five days in Northern Ireland.
	Respiratory deaths include any death where terms directly relating to respiratory causes were mentioned anywhere on the death certificate (this includes Covid-19 deaths). 
	This is not directly comparable to the ONS figures relating to ‘deaths where the underlying cause was respiratory disease’.
	Covid-19 deaths include any death where Coronavirus or Covid-19 (suspected or confirmed) was mentioned anywhere on the death certificate.
	Data are assigned to LGD based on usual residence of the deceased, as provided by the informant. Usual residence can include a care home. Where the deceased was not usually resident in Northern Ireland, their death has been mapped to the place of death.
	The 'Other' category in Place of death includes deaths at a residential address which was not the usual address of the deceased and all other places.

-----------

### DM Notes

	Have requested information from BAs about when the start of the week begins and what do the dashes mean. Until we have an answer for this leave the 'Marker' and the 'Value' columns they are and do not publish.

	BAs have confirmed that the start of the week is on a Saturday