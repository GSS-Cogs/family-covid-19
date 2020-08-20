# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------
## ONS Online job advert estimates 

[Landing Page](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/onlinejobadvertestimates)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Online-job-advert-estimates/flowchart.ttl)

----------
### Stage 1. Transform

#### Sheet: Vacancies

        B12:CA12 - Date
        A13:A42 - Industry 
        A43:CA43 - Marker (Inputed Values row across relates to the following note: "Furthermore some weeks have no observation. The missing  values have been imputed using linear interpolation, and have been highlighted." Format as required)
        Add Measure Type Column with value: Adverts
        Add Unit column with value: Count

#### Table Structure

		Date, Industry, Value, Marker, Measure Type, Unit

-------------

### Stage 2. Alignment

#### Sheet: Vacancies by Adzuna Category

		Format 'Date' column as a day. Adverts are a snapshot of that day
		Change 'Maker' columns value to 'Imputed' where necessary and change all NaNs to empty string. Footnote should cover why and how values have been Imputed.
		I'm a bit confused as to why a count of job adverts can have a decimal place but values are coming through as integers. Can we change back to decimal.
		For 'Industry' column change 'All Industries' to All
		Add column 'NUTS1 Region' with value 'United Kingdom'. See next why not using codes

#### Sheet: Vacancies by NUTS1 Region

		they appear to have added another sheet!!!!
		
		Columns: Date, NUTS1 Region, Marker, Measure Type, Unit, Value
		Format 'Date' column as a day. Adverts are a snapshot of that day
		Change 'Maker' columns value to 'Imputed' where necessary and change all NaNs to empty string. Footnote should cover why and how values have been Imputed.
		Keep 'NUTS1 Region' as is, DO NOT use geography codes as their are values we will not be able to get codes for, 'Unmatched' and 'All Countries and Regions'. Can't use 'United Kingdom' instead of 'All Countries and Regions' as it is referring to the countries and regions that have been matched not everything.
		Add column 'Industry' with value 'All'

	Join both tables

#### Dataset Name

		Online job advert estimates

#### Table Structure

		Date, Industry, NUTS1 Region, Marker, Measure Type, Unit, Value

##### Footnotes

		footnotes from both sheets should be added to metadata

--------------

##### DM Notes

		notes

