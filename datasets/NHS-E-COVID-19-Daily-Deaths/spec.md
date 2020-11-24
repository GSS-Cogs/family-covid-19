# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## NHS-E COVID-19 Daily Deaths 

### National Health Service

[Landing Page](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/)

#### File

	COVID 19 total announced deaths 18 November 2020

#### Sheet: Tab1 Deaths by region

	Column B: NHS Region - map to regions, see DM notes
	Row 16: Date of Death, reformat to day/{yyyy-mm-dd}
		Ignore the first date column 'Up to 1-mar-20' (See DM notes below) 
		Date for total column should be formatted to a gregorian-interval from the first day until the last
	Add Column:
		'Age Band' with value 'total'
		'COVID-19 Test Result' with value 'Positive test result':'positive-test-result'
		'NHS Trust' with value 'total'
	Measure Type: deaths
	Unit: count

#### Sheet: Tab2 Deaths no pos test

	Column B: NHS Region - map to regions, see DM notes
	Row 16: Date of Death, reformat to day/{yyyy-mm-dd}
		Ignore the first date column 'Up to 1-mar-20' (See DM notes below) 
		Date for total column should be formatted to a gregorian-interval from the first day until the last
	Add Column:
		'Age Band' with value 'total'
		'COVID-19 Test Result' with value 'No positive test but mentioned on death certificate':'no-positive-test-mentioned-on-death-certificate'
		'NHS Trust' with value 'total'
	Measure Type: deaths
	Unit: count

#### Sheet: Tab3 Deaths by age

	Column B: Age Bands
	Row 16: Date of Death, reformat to day/{yyyy-mm-dd}
		Ignore the first date column 'Up to 1-mar-20' (See DM notes below)
		Date for total column should be formatted to a gregorian-interval/ from the first day until the last
	Add Column:
		'NHS Region' with value 'E92000001'
		'COVID-19 Test Result' with value 'Positive test result':'positive-test-result'
		'NHS Trust' with value 'total'
	Measure Type: deaths
	Unit: count
					
#### Sheet: Tab4 Deaths by trust

	Column B: NHS Region - map to regions, see DM notes
	Column C: Code, rename --> NHS Trust (Use code column and create codelist with code as Notation and Name (column E) as the Label)
	Row 16: Date of Death, reformat to day/{yyyy-mm-dd}
		Ignore the first date column 'Up to 1-mar-20' (See DM notes below)
		Date for total column should be formatted to a Gregorian-interval from the first day until the last
	Add Column:
		'COVID-19 Test Result' with value 'Positive test result':'positive-test-result'
		'Age Band' with value 'total'
	Measure Type: deaths
	Unit: count		

#### Join all 4 sheets

	
#### Table Structure

	Date, NHS Region, NHS Trust, Age Band, COVID-19 Test Result, Value





## THESE SHEETS APPEARED IN THE FILE WHEN THE SPEC WAS INITIALLY DONE BUT HAVE BEEN REMOVED SINCE.

#### Sheet: COVID19 all deaths by ethnicity

#### Sheet: COVID19 all deaths by gender

#### Sheet: COVID19 all deaths by condition		

#### Sheet: COVID19 all deaths condition 2

##### Footnotes

		Hopefully 

#### DM Notes

	First column of dates states 'Up to  01-Mar-20' cannot find when the start date should be. Have asked BAs if they can investigate. Going to assume 1 Jan 2020 for the time being.
	18th Nov 2020. 
	Lots of the NHS trust names do not a ONS Geography code so will have to create codelist based on codes in Tab4
	Spoke to Dave (DM) agreed that we can ignore the 'up to 1 Mar 20' data as they are all zeros and unless something major happens like a huge re-evaluation NHS deaths then they will always be zero. And if things change then the format of the data tables will probably change as well so the spec will need revisiting.

	Age Band:
		pathify values and change 80+ to 80plus

	NHS Trust
		Pathify values
		
	Region ONS Geography Codes:
		England - E92000001
		London - E12000007
		Midlands - E40000008
		North East and Yorkshire - E40000009
		North West - E12000002
		South East - E40000005
		South West - E32000013

