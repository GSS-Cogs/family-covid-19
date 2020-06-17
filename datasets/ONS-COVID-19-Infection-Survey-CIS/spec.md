# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## ONS Coronavirus  COVID-19  Infection Survey 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/datasets/coronaviruscovid19infectionsurveydata)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Coronavirus-COVID-19-Infection-Survey/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		Coronavirus (COVID-19) Infection Survey

#### Table Structure

		Period, ONS Geography Code, Survey Criteria, Age, Sex, Working Location, CI Lower, CI Upper, Measure Type, Unit, Value

#### Sheet: 1

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with value Count, Average Count, Average Percentage as appropriate.
		Add Unit column with value Person or Percent as appropriate.
		A7:A10 - Survey Criteria 
			'Number of individuals included in this analysis (unweighted)' - 'Total Individuals in Analysis (unweighted)'
			'Estimated average % of the population that had COVID-19 (weighted)' - ' Estimated Total COVID-19 Cases (weighted)'
			'Estimated average number of people in England who had COVID-19 (weighted)' - 'Estimated Total COVID-19 Cases (weighted)'
		C7:C10 - CI Lower
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D10 - CI Upper
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.
		
#### Sheet: 2

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with value Average Count, Percentage as appropriate.
		Add Unit column with value Person or Percent as appropriate.
		A7:A8 - Survey Criteria 
			'New infections per 100 people followed for 1 week, known as the incidence rate ' - 'Incidence Rate (weighted)'
			'Estimated average number of people in England who were newly infected with COVID-19 per week ' - 'Estimated Infections Per Week (weighted)'
		C7:C8 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 3

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with value Count, Percentage as appropriate.
		Add Unit column with value Person or Percent as appropriate.
		A7:A8 - Survey Criteria 
			'Individuals included in antibody analysis' - 'Individuals Included in Antibody Analysis (unweighted)'
			'Percentage of individuals testing positive for antibodies' - 'Estimated Individuals Testing Positive for Antibodies (unweighted)'
		C7:C8 - CI Lower
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 4

		A7:A12 - Period
			Remove everything after, and including, the colon but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with value Average Count, Percentage as appropriate.
		Add Unit column with value Person or Percent as appropriate.
		B5:C5 - Survey Criteria 
			'Number testing positive for COVID-19' - 'Estimated Tested Positive for COVID-19 (weighted)'
			'% testing positive for COVID-19' - 'Estimated Tested Positive for COVID-19 (weighted)'
		D7:D10 - CI Lower
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.
		E7:E10 - CI Upper
			Replace blank values with N/A
			Multiply percentage values by 100 due to Excel formatting quirk.
		Ignore blank and '-' values in observations as they are non-values. They are just there so that 95% confidence interval column relates correctly.

#### Sheet: 5

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		A7:A11 Age 
			70 and above - 70+
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		B5 - Survey Criteria 
			'% testing positive for COVID-19' - 'Estimated Tested Positive for COVID-19 (weighted)'
		C7:C11 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D11 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 6

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		A7:A8 Sex 
		Add Working Location column with value 'Any'
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		B5 - Survey Criteria 
			'% testing positive for COVID-19' - 'Estimated Tested Positive for COVID-19 (weighted)'
		C7:C8 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 7

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		A7:A8 - Survey Criteria 
			'Individuals working in patient-facing healthcare or resident-facing social care roles' - 'Estimated Individuals Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)'
			'Individuals not working in patient-facing healthcare or resident-facing social care roles' - 'Estimated Individuals not Working in Patient-Facing Healthcare or Resident-Facing Social Care Roles Testing Positive COVID-19 (unweighted)'
		C7:C8 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 8

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		A7:A8 - Survey Criteria 
			'Individuals reporting any symptoms on the day of the test' - 'Estimated Individuals Testing Positive for COVID-19 Reporting Symptons on Day of Test (unweighted)'
			'Individuals not reporting any symptoms on the day of the test' - 'Estimated Individuals Testing Positive for COVID-19 Not Reporting Symptons on Day of Test (unweighted)'
		C7:C8 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 9

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		Add Working Location column with value 'Any'
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		A7:A8 - Survey Criteria 
			'Individuals reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test' - 'Estimated Individuals Testing Positive for COVID-19 reporting a cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)'
			'Individuals reporting no cough or fever or loss of taste/smell on the day of the test' - 'Estimated Individuals Testing Positive for COVID-19 reporting no cough, and/or fever, and/or loss of taste/smell on the day of the test (unweighted)
		C7:C8 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D8 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

#### Sheet: 10

		A4 - Period
			Period given for full tab, remove 'between ' but leave rest unformatted for later harmonisation.
		Add ONS Geography Column with value 'E92000001'
		Add Age column with Value 'All'
		Add Sex column with value 'All'
		A7:A10 Working Location
		Add Measure Type column with Percentage
		Add Unit column with value Percent 
		B5 - Survey Criteria 
			'% testing positive for COVID-19' - 'Estimated Tested Positive for COVID-19 (weighted)'
		C7:C10 - CI Lower
			Multiply percentage values by 100 due to Excel formatting quirk.
		D7:D10 - CI Upper
			Multiply percentage values by 100 due to Excel formatting quirk.

##### DM Notes

		In column 'Working Location' the value 'Any' includes Non-applicable eg Children and non-workers.

