# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## NHS-D Coronavirus Shielded Patient List Summary Totals, England 

[Landing Page](https://digital.nhs.uk/data-and-information/publications/statistical/mi-english-coronavirus-covid-19-shielded-patient-list-summary-totals/latest)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NHS-D-Coronavirus-Shielded-Patient-List-Summary-Totals-England/flowchart.ttl)

----------

### Stage 1. Transform

#### Filename: Coronavirus Shielded Patient List, England - Open Data - CCG, Sheet: Coronavirus Shielded Patient Li

		A - Extract Date
		B - CCG Code
		C - CCG Name
		D - Breakdown Field
		E - Breakdown Value
		F - Patient Count

#### Table Structure

		Extract Date, CCG Code, CCG Name, Breakdown Field, Breakdown Value, Patient Count, Measure Type, Unit, Marker, Value

#### Filename: Coronavirus Shielded Patient List, England - Open Data - LA, Sheet: Coronavirus Shielded Patient Li

		A - Extract Date
		B - LA Code
		C - LA Name
		D - Breakdown Field
		E - Breakdown Value
		F - Patient Count

#### Table Structure

		Extract Date, LA Code, LA Name, Breakdown Field, Breakdown Value, Patient Count, Measure Type, Unit, Marker, Value

-------------

### Stage 2. Harmonise

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: 2

		spec

----------

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

--------------##### Footnotes

		footnotes

##### DM Notes

		notes

