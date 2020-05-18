# COGS Dataset Specification

[Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## Universal Credit declarations (claims) and advances: management information

### Department for Work and Pensions

[Landing Page](https://www.gov.uk/government/collections/universal-credit-statistics)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?DWP-Universal-Credit-declarations-claims-and-advances-management-information/flowchart.ttl)


### Dataset One

#### Output Dataset Name:
	DWP Universal Credit Declarations and Advances - Management Information

#### Table Structure
	Period, Universal Credit Stage, Measure Type, Unit, Marker, Value

#### Sheet: 1

	C7:BP7 - Date - Change name to Period and format as required

	B12:B13 - Universal Credit Stage
	
		Households making a Universal Credit declaration - Declaration
		Individuals making a Universal Credit declaration - Declaration

	Add Measure Type column with values Households and Individuals
	
	Add Unit column with values Count

#### Sheet: 2

	C7:BP7 - Date - Change name to Period and format as required

	B12:B17 - Universal Credit Stage
	
		New Claim/ Benefit Transfer - Advance New Claim or Benefit Transfer
		Budgeting - Advance Budgeting
		Change of Circumstances - Advance Change of Circumstances  
		Total - Advance Total

	Add Measure Type column with values Advances
	
	Add Unit column with values Count


##### Footnotes
	Text from the Notes sheet needs to be added to the metadata as it makes statements about 
	suitability and comparability. 

	The Definitions sheets would also be helpful or explanations
		