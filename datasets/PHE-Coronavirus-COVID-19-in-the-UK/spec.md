# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/index.html)

## PHE Coronavirus  COVID-19  in the UK 

### Public Health England

[Landing Page](https://coronavirus.data.gov.uk/?_ga=2.156389567.589199403.1589439040-1962094972.1582617556)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?phe-coronavirus-covid-19-in-the-uk/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		PHE Coronavirus COVID-19 Cases & Deaths in the UK

#### Table Structure

		Period, ONS Geography Code, Area Type, Reported Case Type, Measure Type, Unit, Marker, Value

#### Filename: coronavirus-cases_latest.csv (Also available as JSON)

#### Sheet: coronavirus-cases_latest

		A - Area name - We have the code so do not this column
		B - Area code - change to ONS Geography Code
		C - Area Type (Codelist)
		D - Specimen Date - change to Period and format as required
		E1:K1 - Reported Case Type	
		Add Measure Type column with values Cases and Rate
		Add Unit column with value Count

#### Filename: coronavirus-deaths_latest.csv (Also available as JSON)

#### Sheet: coronavirus-deaths_latest

		A - Area name - We have the code so do not this column
		B - Area code - change to ONS Geography Code
		C - Area Type (Codelist)
		D - Reporting Date - change to Period and format as required
		E1:F1 - Reported Case Type	
		Add Measure Type column with values Deaths
		Add Unit column with value Count

##### Footnotes
		Periods for Cases are Specimen Data.
		Periods for Deaths are Reporting Date.
		Deaths and lab-confirmed case counts and rates for England and subnational areas are provided by Public Health England. All data for the rest of the UK are provided by the Department of Health and Social Care based on data from the devolved administrations. Maps include Ordnance Survey data © Crown copyright and database right 2020 and Office for National Statistics data © Crown copyright and database right 2020. See the About the data page (link at top of this page) for details. The England total excludes 392 lab-confirmed cases that are not yet in the automated reporting system. These are included in the total number of lab-confirmed UK cases.

