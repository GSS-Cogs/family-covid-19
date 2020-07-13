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

#### Sheet: Weekly Deaths_Age by Sex - Deaths registered each week in Northern Ireland 2020

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

#### Sheet: Covid-19_Deaths_age by sex - Covid-19 Deaths registered each week in Northern Ireland, age by sex

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

#### Dataset Outputs:

		d1. NISRA Weekly Registered COVID-19 and All Deaths
		
			Reformat NaN values in marker column to Empty sting
			Map Local Government District column to mapping CSV
			Map Sex column to sex_mapping.csv
			Reformat year to date values (year/2020) with overall range date
			Remove any superscript values from end of string in columns (eg, 1, 2, 3, P)
			Replace any Nan value sin Value column with 0 and check a reason why has been put in Marker column
			
		d2. dataset output Two

#### Sheet: Table 1

		Column Addition/Removal/Rename/Reformat
			Add Sex column with value T
			Add NISRA Age Band column with value All
			Remove column Registration Week
			Rename column Week Ending to Period
			Add column Local Government District with value All
			Add Location of Death column with value All
			
		Join to Dataset:
			d1

#### Sheet: Table 2

		Column Addition/Removal/Rename/Reformat
			Add column Registered Death Type with value All Registered Deaths
			Remove column Week number
			Rename column Week Ending to Period
			Reformat year to date values with overall range date
			Rename Gender column to Sex and reformat with M, F, T, U
			Add column Local Government District with value All	
			Add Location of Death column with value All
		
		Join to Dataset:
			d1
		
#### Sheet: Table 3

		Column Addition/Removal/Rename/Reformat
			Add Sex column with value T
			Add NISRA Age Band column with value All
			Add column Registered Death Type with value All Registered Deaths
			Remove column Registration Week
			Rename column Week Ending to Period
			Add Location of Death column with value All
		
		Join to Dataset:
			d1

#### Sheet: Table 4

		Column Addition/Removal/Rename/Reformat
			Add column Registered Death Type with value COVID-19 Registered Deaths
			Add column Local Government District with value All
			Remove column Week number
			Rename column Week Ending to Period
			Add Location of Death column with value All
		
		Join to Dataset:
			d1

#### Sheet: Table 5

		Column Addition/Removal/Rename/Reformat
			Add column Registered Death Type with value COVID-19 Registered Deaths
			Add Sex column with value T
			Add NISRA Age Band column with value All
			Remove column Registration Week
			Rename column Week Ending to Period
			Add Location of Death column with value All
		
		Join to Dataset:
			d1

#### Sheet: Table  6

		Column Addition/Removal/Rename/Reformat
			Add column Registered Death Type with value COVID-19 Registered Deaths
			Add Sex column with value T
			Add NISRA Age Band column with value All
			Remove column Week of Death
			Rename column Week Ending to Period
			Rename Place of Death column to Location of Death (Just to match up with other COVID-19 datasets)
		
		Join to Dataset:
			d1
		

#### Sheet: Table 7

		Column Addition/Removal/Rename/Reformat
			Add column Registered Death Type with value COVID-19 Registered Deaths
			Add Sex column with value T
			Add NISRA Age Band column with value All
			Remove column Registration Week
			Rename column Week Ending to Period
			Add Location of Death column with value All
		
		Join to Dataset:
			d1
		
		
#### Sheet: Table 8

		Column Addition/Removal/Rename/Reformat
			Remove column Week of Death
			Rename column Place elf Death as Location of Death
		
		Join to Dataset:
			d2
		
#### Sheet: Table 9

		Column Addition/Removal/Rename/Reformat
			Add a column
		
		Join to Dataset:
			d2
		
#### Sheet: Table 10

		Column Addition/Removal/Rename/Reformat
			Add a column
		
		Join to Dataset:
			d2

#### Sheet: Table 11

		Column Addition/Removal/Rename/Reformat
			Add a column
		
		Join to Dataset:
			d2

-----

##### Footnotes

		footnotes

