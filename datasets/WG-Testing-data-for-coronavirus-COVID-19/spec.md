# COGS Dataset Specification

[Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

## Testing data for coronavirus (COVID-19)

### Welsh Government

[Landing Page](https://gov.wales/testing-data-coronavirus-covid-19-12-may-2020)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?WG-Testing-data-for-coronavirus-COVID-19/flowchart.ttl)

[Development](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

### Dataset One

#### Output Dataset Name:
	WG Testing data for Coronavirus - COVID-19 

#### Table Structure
	Period, Test Outcome, Critical Worker Category, Emergency Services Worker, Test Location, Marker, Measure Type, Unit, Value 

#### Sheet: Completed_tests

	A - Date - Change name to Period and format as required

	B:C - Test Outcome
	
		Cumulative individuals tested - Total
		Cumulative positive cases - Positive

	Add Test Location column with value All

	Add Critical Worker Category column with value All

	Add Emergency Services Worker column with value All
		
	Add Measure Type Column with value People

	Add Unit column with value Cumulative Count

#### Sheet: Critical_workers_category

	B7:M7 - Date - Change name to Period and format as required
	
	B8:M8 - Test Outcome (Codelist)
	
		Cumulative positive cases - Positive
		Cumulative negative cases - Negative
		Cumulative number of test - Total
		
	A9:A17 - Critical Worker Category (Codelist)

	Add Emergency Services Worker column with value All

	Add Test Location column with value All

	Add Measure Type Column with value People

	Add Unit column with value Cumulative Count

#### Sheet: Critical_workers_detail

	C9:E9 - Date - Change name to Period and format as required

	C10:E10 - Test Outcome (Codelist)
	
		Cumulative positive cases - Positive
		Cumulative negative cases - Negative
		Cumulative number of test - Total

	A11:A30 - Critical Worker Category (Codelist)

	B11:B30 - Emergency Services Worker (Codelist)

	Add Test Location column with value All

	Add Measure Type Column with value People

	Add Unit column with value Cumulative Count

#### Sheet: Location_tests

	B7:Q7 - Date - Change name to Period and format as required

	B8:Q8 - Test Outcome (Codelist)

		Cumulative tests completed - Total
		% results within 1 day - Results within 1 Day
		% results within 3 days - Results within 3 Days


	A9:A11 - Test Location
		Tested in hospital - Hospital
		Tested ar coronavirus testing unit - Coronavirus Testing Unit
		Testing as drive-through centres - Drive-through Centres

	Add Critical Worker Category column with value All

	Add Emergency Services Worker column with value All

	Add Measure Type Column with value Tests

	Add Unit column with value Count		

##### Footnotes
	Add to Metadata:
		Data presented is the cumulative total correct at the date stated
		The column Emergency Services Worker is a legacy category. Numbers may decline over time as data entry improves
		