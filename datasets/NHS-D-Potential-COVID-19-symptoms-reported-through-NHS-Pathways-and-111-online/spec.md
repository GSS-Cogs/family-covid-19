# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/index.html)

## NHS-D Potential COVID-19 symptoms reported through NHS Pathways and 111 online 

### National Health Service

[Landing Page](https://digital.nhs.uk/data-and-information/publications/statistical/mi-potential-covid-19-symptoms-reported-through-nhs-pathways-and-111-online)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/specflowcharts.html?nhs-d-potential-covid-19-symptoms-reported-through-nhs-pathways-and-111-online/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		NHS Potential COVID-19 Symptoms reported through NHS Pathways and 111 Online

#### Table Structure

		Period, Site Type, Sex, Age, ONS Geography Code, Measure Type, Unit, Marker, Value

#### Filename: 111 Online Covid-19 data_CCG mapped.csv

#### Sheet: 111 Online Covid-19 data_CCG ma

		A - SiteType - change to Site Type (Codelist) (111, 999)
		B - CallDate - Change to Period and format as required
		C - Gender - change to Sex (Male = M, Female = F, Unknown = U)
		D - AgeBand - Change to Age (Codelist)
		E - CCGCode - Change to ONS Geography Code
		F - CCGName - Ignore as we have the Geography codes
		G - April20 mappedCCGCode - Ignore as some of these geographies are not available on the portal
		H - April20 mappedCCGName - Ignore 
		I - TriageCount - These are the Observations (Obvs)
		Add Measure Type column with value Triage
		Add Unit column with value Count 

#### Filename: NHS Pathway Covid-19 data CCG mapped.csv

#### Sheet: NHS Pathway Covid-19 data CCG

		A - JourneyDate - Change to Period and format as required
		B - Gender - change to Sex (Male = M, Female = F, Unknown = U)
		C - AgeBand - Change to Age (Codelist)
		D - CCGCode - Change to ONS Geography Code 
		E - CCGName - Ignore as we have the Geography codes
		F - April20 mappedCCGCode - Ignore as some of these geographies are not available on the portal
		G - April20 mappedCCGName - Ignore 
		H - Total - These are the Observations (Obvs)
		Add Site Type column with value 111 Online
		Add Measure Type column with value Online Assessments
		Add Unit column with value Count 

##### Footnotes

		
		Extra files have been created with lots of Metadata, need to decide how we can handle this.

#### DM Notes

	Some of the mapped Geography codes are missing from the portal, they cooer to be aggregated, merged or renamed NHS Trusts. Emailed Matt Jinman on 20/05/2020 with a list of 75 codes asking if they can be added.