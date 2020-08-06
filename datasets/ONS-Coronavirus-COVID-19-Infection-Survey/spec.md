# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## ONS Coronavirus COVID-19 Infection Survey

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronaviruscovid19infectionsurveydata)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Coronavirus-COVID-19-Infection-Survey/flowchart.ttl)

-------------

### Stage 2. Alignment

#### Sheet: 1

		Bring Ratios back into the table
			'Unit' column value for ratios should be 'People'
			'Measure Type' column values for ratios should be 'Ratio'
		Rename 'Period' column 'Date' and format as required
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove column 'Survey Measure Type'
		Rename 'OBS' to 'Value' 
	   
		Set up dataset for output and test but comment out for Jenkins until multiple measure datacubes can be processed.
		Dataset Name:
			'Coronavirus COVID-19 Infection Survey - Modelled mid-week Estimates of positive tests'

		Add all footnotes to description. Also add line: Intervals are at 95%
		The modelled numbers are the same as in sheet 2 but this sheet holds extra information

#### Sheet: 2

		Rename 'Period' column 'Date' and format as required
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Rename column 'Survey Measure Type' to 'Modelled Estimate Type'
		Rename 'OBS' to 'Value' 
		Change 'Measure Type' column value 'Percentage' to 'Percentage Rate'
		
		Output as own dataset with name:
			'Coronavirus COVID-19 Infection Survey - Modelled daily rates of the population testing positive in England'
		Add all footnotes to description. Also add line: Intervals are at 95%

#### Sheet: 3

		Format 'Period' column as 14 day Gregorian-interval
		Bring Household data back in
			'Unit' column value for households should be 'Households'
			'Measure Type' column value for households should be 'Sample Count'
		Change 'Measure Type' column value 'Count' to 'Sample Count'
		Rename column 'Survey Measure Type' to 'Modelled Estimate Type'
		Change'Measure Type' column value 'Percentage' to 'Percentage Rate'
		Remove '(modelled)' from 'Modelled Estimate Type' column values
		Rename 'OBS' to 'Value' 
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Overall number of COVID-19 infections by non-overlapping 14 day periods'
		Add all footnotes to description. Also add line: Intervals are at 95%		

#### Sheet: 4
	
		Rename 'period' column as 'Date' and format as required
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Rename column 'Survey Measure Type' to 'Modelled Estimate Type'
		Change 'Measure Type' column with value 'Person per 10000' to 'Percentage Rate'
		Change 'Unit' Column with value 'Person' to 'People'
		Rename 'OBS' to 'Value' 
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Modelled mid-week estimates for number of new infections, England'
		Add all footnotes to description. Also add line: Intervals are at 95%	

#### Sheet: 5

		Rename 'Period' column 'Date' and format as required
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove column 'Survey Measure Type' column
		Rename 'OBS' to 'Value' 
		Change 'Unit' Column with value 'Person' to 'People'
		Remove 'Weighted' column
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Modelled daily incidence rates, England'
		Add all footnotes to description. Also add line: Intervals are at 95%		

#### Sheet: 6

		Format 'Period' column as 14 day Gregorian-interval
		Rename 'OBS' to 'Value'
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Rename column 'Survey Measure Type' to 'Modelled Estimate Type'
		Remove 'Weighted' column

		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Incidence rate and estimated number of new infections for individuals (unweighted) - 2 week periods'
		Add all footnotes to description. Also add line: Intervals are at 95%	

#### Sheet: 7

		Format 'Period' column as 14 day Gregorian-interval
		Rename 'OBS' to 'Value'
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove 'Weighted' column

		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Incidence rate and estimated number of new infections for households (unweighted) - 2 week periods'
		Add all footnotes to description. Also add line: Intervals are at 95%	

#### Sheet: 8

		Extract date from 'Period' column and format as required
		Map 'Region' columns to Geography codes and keep the name 'Region'
		Rename 'OBS' to 'Value'
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove 'Survey Measure Type' column
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Modelled estimated & testing positive by region, England (Mid point of most recent week)'
		Add all footnotes to description. Also add line: Intervals are at 95%	

#### Sheet: 9

		Rename 'Period' column to 'Date' and format as required
		Map 'Region' columns to Geography codes and keep the name 'Region'
		Rename 'OBS' to 'Value'
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove 'Survey Measure Type' column
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Modelled daily average percentage of individuals testing positive by region'
		Add all footnotes to description. Also add line: Intervals are at 95%	

#### Sheet: 10

		Bring ratio values back in to table
		Format 'Period' column to Gregorian-interval
		Map 'Region' columns to Geography codes and keep the name 'Region'
		Rename 'OBS' to 'Value'
		Rename 'Lower CI' to 'Credible Lower Interval'
		Rename 'Upper CI' to 'Credible Upper Interval'
		Remove 'Weighted' column
		Remove 'Survey Measure Type' column
		
		Output as own dataset with name:
		'Coronavirus COVID-19 Infection Survey - Percentage of individuals ever testing positive for antibodies (weighted)'
		Add all footnotes to description. Also add line: Intervals are at 95%	

								
#### Join

		DO NOT PUBLISH THIS DATA TO PMD AT THE MOMENT, IT HAS LOTS OF DIFFERENT UNIT TYPES AND WILL CAUSE PROBLEMS
		JUST GET IT READY FOR PUBLISHING
		All 10 datasets have been kept separate as the data is a bit of a nightmare.

----------

##### DM Notes

		info.json NEEDS UPDATING FOR MAPPING AND CODELIST FILES NEED TO BE CREATED (csv and json)

