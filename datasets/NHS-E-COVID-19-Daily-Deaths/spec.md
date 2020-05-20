# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## NHS-E COVID-19 Daily Deaths 

### National Health Service

[Landing Page](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NHS-E-COVID-19-Daily-Deaths/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		name

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: COVID19 total deaths by trust

		B17:B235 - NHS England Region - ignore not needed, should be able to derive from hierarchies in the future
		D17:D235 - Code - change to NHS Hospital Code (Codelist)
		E17:E235 - Name - ignore as we have the code but becomes part of the NHS Hospital Code Codelist
		F16:CG16 - Date - change to Period and format as required
		CI17:CI235 - Awaiting Verification - will have the overall date range in the period column
		CK17:CK235 - Total - will have the overall date range in the period column
		Add Measure Type column with value Deaths
		Add Unit column with value Count

#### Sheet: 2

		spec

##### Footnotes

		footnotes

