# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## NHS-E COVID-19 Daily Deaths 

### National Health Service

[Landing Page](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-daily-deaths/)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NHS-E-COVID-19-Daily-Deaths/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		NHS COVID-19 Daily Deaths

#### Table Structure

		Period, ONS Geography Code, NHS Hospital Code, Age, Ethnicity, Pre-existing Condition Status, Pre-existing Condition, Measure Type, Unit, Marker, Value

#### Sheet: COVID19 total deaths by trust

		B17:B235 - NHS England Region - change to ONS Geography Code and change to codes:
			England - E92000001
			London - E12000007
			Midlands - E40000008
			North East and Yorkshire - E40000009
			North West - E12000002
			South East - E40000005
			South West - E32000013
		D17:D235 - Code - change to NHS Hospital Code (Codelist)
		E17:E235 - Name - ignore as we have the code but becomes part of the NHS Hospital Code Codelist
		F16:CG16 - Date - change to Period and format as required
		CI17:CI235 - Awaiting Verification - change Measure Type as below, will have the overall date range in the period column
		CK17:CK235 - Total - will have the overall date range in the period column
		Add Age column with value All
		Add Ethnicity column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with values Deaths Positive Test and Deaths Awaiting Verification
		Add Unit column with value Count

#### Sheet: COVID19 total deaths by region

		B17:B25 - NHS England Region - change to ONS Geography Code and change to codes as explained above
		D16:CE16 - Date - change to Period and format as required
		CI17:CI25 - Awaiting Verification - change Measure Type as below, will have the overall date range in the period column
		CK17:CK25 - Total - will have the overall date range in the period column
		Add NHS Hospital Code column with value All
		Add Age column with value All
		Add Ethnicity column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with values Deaths Positive Test and Deaths Awaiting Verification
		Add Unit column with value Count

#### Sheet: Deaths by Region - no pos test

		B17:B25 - NHS England Region - change to ONS Geography Code and change to codes as explained above
		D16:CE16 - Date - change to Period and format as required
		CI17:CI25 - Awaiting Verification - change Measure Type as below, will have the overall date range in the period column
		CK17:CK25 - Total - will have the overall date range in the period column
		Add NHS Hospital Code column with value All
		Add Age column with value All
		Add Ethnicity column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with values Deaths No Positive test and Deaths Awaiting Verification
		Add Unit column with value Count

#### Sheet: COVID19 total deaths by age

		B17:B24 - Age group - change to Age (Codelist)
		D16:CE16 - Date - change to Period and format as required
		CI17:CI224 - Awaiting Verification - change Measure Type as below, will have the overall date range in the period column
		CK17:CK224 - Total - will have the overall date range in the period column
		Add ONS Geography Code column with value E92000001
		Add NHS Hospital Code column with value All
		Add Ethnicity column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with values Deaths Positive Test and Deaths Awaiting Verification
		Add Unit column with value Count

#### Sheet: COVID19 all deaths by ethnicity

		C5 - Date - change to Period and format as required (will have to figure out what the date range is)
		B17:B40 - Ethnic Group - change to Ethnicity (Codelist)
			Row 22 = White Total 
			Row 27 = Mixed Race Total
			Row 37 = BAME Total
			Row 40 = Not Stated/No match Total
		Add ONS Geography Code column with value E92000001
		Add NHS Hospital Code column with value All
		Add Age column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with values Deaths Positive Test and Percentage and Percentage without Null and not stated
		Add Unit column with values Count and Percent

#### Sheet: COVID19 all deaths by gender

		C5 - Date - change to Period and format as required (will have to figure out what the date range is)
		B17:B24 - Age group - change to Age (Codelist)
		D16:G16 - Gender - change to Sex - Female = F, Male = M, Unknown Gender = U, Total = T
		Add ONS Geography Code column with value E92000001
		Add NHS Hospital Code column with value All
		Add Ethnicity column with value All
		Add Pre-existing Condition Status column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with value Deaths Positive Test
		Add Unit column with value Count

#### Sheet: COVID19 all deaths by condition

		C5 - Date - change to Period and format as required (will have to figure out what the date range is)
		D16:G16 - Pre-existing Condition Status (Codelist)
		B17:B24 - Age Group - change to Age (Codelist)
		Add ONS Geography Code column with value E92000001
		Add NHS Hospital Code column with value All
		Add Ethnicity column with value All
		Add Age column with value All
		Add Pre-existing Condition column with value All
		Add Measure Type column with value Deaths Positive Test
		Add Unit column with value Count		

#### Sheet: COVID19 all deaths condition 2

		B16:B27 - Date Introduced - change to Period ,this should be a date range from the date in the cell to the published date in cell C8
		C16:C27 - Condition - change to Pre-existing Condition (Codelist) 
		D15:H15 - Pre-existing Condition Status (Codelist)
			Count of condition = With Condition
			Count of unknown or not reported for condition = unknown or not reported
			Count of all deaths since condition introduced = Deaths since Condition Introduced
			% of deaths since introduced with condition = Deaths since Condition Introduced
			% of deaths (excluding unknown or not reported) with condition = Deaths excluding unknown or not reported
		Add ONS Geography Code column with value E92000001
		Add NHS Hospital Code column with value All
		Add Ethnicity column with value All
		Add Age column with value All
		Add Pre-existing Condition Status column with value Yes
		Add Measure Type column with values Deaths Positive Test 
		Add Unit column with values Count and Percent	

##### Footnotes

		Hopefully this is in already in the metadata
		Note: interpretation of the figures should take into account the fact that totals by date of death, particularly for recent prior days, are likely to be updated in future releases. For example as deaths are confirmed as testing positive for Covid-19, as more post-mortem tests are processed and data from them are validated. Any changes are made clear in the daily files.

#### DM Notes

Data likely to change from 14 May 2020, hopefully this will already be explained in the metadata

