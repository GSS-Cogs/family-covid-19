# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

------

## WG Notifications of deaths of residents related to COVID-19 in adult care homes 

[Landing Page](https://gov.wales/notifications-deaths-residents-related-covid-19-adult-care-homes)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?WG-Notifications-of-deaths-of-residents-related-to-COVID-19-in-adult-care-homes/flowchart.ttl)

--------

### 1. Transform

#### Sheet: Table_1 Notifications of Service User Deaths received from Adult Care Homes

		B3:D3 - Notification Date Range
		A4:A6 - Care Provided
		Measure Type column = Deaths
		Unit column value = Count
		9 Observations

##### Table Structure
		Notification Date Range, Care Provided, Measure Type, Unit, Marker, Value

#### Sheet: Table_2 Notifications of deaths of adult care home residents with confirmed or suspected COVID-19 by location of death

		A1 - Notification Date Range
		A3:A10 - Location of Death
		Add Measure Type column with value Deaths
		Add Unit column with value Count
		8 Observations

##### Table Structure
		Notification Date Range, Location of Death, Measure Type, Unit, Marker, Value

#### Sheet: Table_3 Notifications of deaths of residents from adult care homes by date of notification and cause

		A6:A371 - Notification Day
		B3:D3 - Notification Year 
		B4:H5 - Cause of Death (Codelist)
		Add Measure Type column with value Deaths
		Add Unit column with value Count
		Remove data for 2020 that is in the future (Obvs)
		2562 Observations with future data 1412 without 

##### Table Structure
		Notification Day, Notification Year, Cause of Death, Measure Type, Unit, Marker, Value

#### Sheet: Table_4 Notifications of deaths of adult care home residents with confirmed or suspected covid-19 by location of death and date of notification

		A5:A80 - Notification Date
		B4:I4 - Location of Death (Codelist)
		Add Measure Type column with value Deaths
		Add Unit column with value Count
		This table is for Deaths with Confirmed or Suspected COVID-19 (Cause)
		608 Observations

##### Table Structure
		Notification Date, Location of Death, Measure Type, Unit, Marker, Value

#### Sheet: Table_5 Notifications of deaths of adult care home residents by location of death and date of notification

		A5:A80 - Notification Date
		B4:I4 - Location of Death (Codelist)
		Add Measure Type column with value Deaths
		Add Unit column with value Count
		This table is for all Deaths (Cause)
		608 Observations
		
##### Table Structure
		Notification Date, Location of Death, Measure Type, Unit, Marker, Value
		
#### Sheet: Table_6 Number of notifications of deaths of adult care home residents involving COVID-19 (both confirmed and suspected) occurring in care homes, by Local Authority and day of notification

		A4:A26 - Area Code
		B4:B26 - Local Authority
		C3:BZ3 - Notification Date
		Add Measure Type column with value Deaths
		Add Unit column with value Count
		This table is for Deaths in Care Homes (Location) where the person had Confirmed or Suspected COVID-19 (Cause)
		1748 Observations

##### Table Structure
		Area Code, Local Authority, Notification Date, Measure Type, Unit, Marker, Value

#### Sheet: Table_7 Number of notifications of deaths of adult care home residents involving COVID-19 (both confirmed and suspected) occurring in any location, by Local Authority and day of notification

		A4:A26 - Area Code
		B4:B26 - Local Authority
		C3:BZ3 - Notification Date
		Add Measure Type column with value Deaths
		Add Unit column with value Count	
		This table is for Deaths in all locations (Location) where the person had Confirmed or Suspected COVID-19 (Cause)	
		1748 Observations

##### Table Structure
		Area Code, Local Authority, Notification Date, Measure Type, Unit, Marker, Value

#### Sheet: Table_8 Number of notifications of deaths of adult care home residents by Local Authority and day of notification

		A4:A26 - Area Code
		B4:B26 - Local Authority
		C3:BZ3 - Notification Date
		Add Measure Type column with value Deaths
		Add Unit column with value Count	
		This table is for Deaths in all locations (Location) and for all cause of deaths (Cause)	
		1748 Observations

##### Table Structure
		Area Code, Local Authority, Notification Date, Measure Type, Unit, Marker, Value

#### Sheet: Table_9 Number of notifications of deaths of adult care home residents occurring in care homes by Local Authority and day of notification

		A4:A26 - Area Code
		B4:B26 - Local Authority
		C3:BZ3 - Notification Date
		Add Measure Type column with value Deaths
		Add Unit column with value Count	
		This table is for Deaths in Care Homes (Location) and for all cause of deaths (Cause)	
		1748 Observations

##### Table Structure
		Area Code, Local Authority, Notification Date, Measure Type, Unit, Marker, Value
	
##### Footnotes

		N/A

--------------------------

### 2. Alignment 

#### Dataset Outputs:

		d1. dataset output One
		d2. dataset output Two
		d3. Dataset output Three

#### Sheet: Table_1

		Column Additions/Renames/Deletions
			Period column Gregorian-interval period as stated in column headings
			Add column Location of Death with value All
			Add Cause of Death with value All
			Add column Local Authority with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Care Provided --> Location of Death, Cause of Death, Local Authority
			
		Join to Dataset:
			d1

#### Sheet: Table_2

		Column Additions/Renames/Deletions
			Period column Gregorian-interval period as stated in title (A1)
			Add column Cause of Death with value COVID-19
			Add column Care Provided with value All
			Add column Local Authority with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Location of Death --> Care Provided, Cause of Death, Local Authority
			
		Join to Dataset:
			d1

#### Sheet: Table_3

		Column Additions/Renames/Deletions
			Period column, join up Year with day to give Gregorian-Day interval
			Add column Location of Death with value All
			Add column Care Provided with value All
			Add column Local Authority with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 
			Change "All deaths Total" to "All", "Covid Total" to "COVID-19", "Non-Covid Total" to "Other"
			Change "Suspected" to "Suspected COVID-19", "Confirmed" to "Confirmed COVID-19"

		Period, Cause of Death --> Location of Death, Care Provided, Local Authority
			
		Join to Dataset:
			d1

#### Sheet: Table_4 

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Care Provided with value All
			Add column Cause of Death with value COVID-19
			Add column Local Authority with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Location of Death --> Care Provided, Cause of Death, Local Authority
			
		Join to Dataset:
			d1

#### Sheet: Table_5

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Care Provided with value All
			Add column Cause of Death with value All
			Add column Local Authority with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Location of Death --> Care Provided, Cause of Death, Local Authority
			
		Join to Dataset:
			d1
		
#### Sheet: Table_6 

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Location of Death with value Care Home
			Add column Care Provided with value All
			Add column Cause of Death with value COVID-19
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Local Authority --> Location of Death, Care Provided, Cause of Death
			
		Join to Dataset:
			d1

#### Sheet: Table_7 

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Location of Death with value All
			Add column Care Provided with value All
			Add column Cause of Death with value COVID-19
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Local Authority --> Location of Death, Care Provided, Cause of Death
			
		Join to Dataset:
			d1

#### Sheet: Table_8

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Location of Death with value All
			Add column Care Provided with value All
			Add column Cause of Death with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Local Authority --> Location of Death, Care Provided, Cause of Death
			
		Join to Dataset:
			d1

#### Sheet: Table_9

		Column Additions/Renames/Deletions
			Period column Gregorian-day interval
			Add column Location of Death with value Care Home
			Add column Care Provided with value All
			Add column Cause of Death with value All
			Add column Measure Type with value Deaths
			Add column Unit with value Count 

		Period, Local Authority --> Location of Death, Care Provided, Cause of Death
			
		Join to Dataset:
			d1

#### DM Notes

		Check if metadata mentions that the COVID-19 cases are both confirmed and suspected

