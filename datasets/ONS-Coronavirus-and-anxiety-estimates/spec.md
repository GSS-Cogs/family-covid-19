# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## ONS Coronavirus and anxiety estimates 

### Office for National Statistics

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/datasets/coronavirusandanxietyestimates)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Coronavirus-and-anxiety-estimates/flowchart.ttl)

### Stage 1: Alignment

#### Sheet: Loneliness, Sex, Marital Status, Felling safe, Work affected, Disability

		Tables have already been joined in stage 1

#### Output Table

		Format the dates as Gregorian-intervals
		Create column "Opinions and Lifestyle Survey" with value "OPN Lite #" (1-7), values taken from the 'Period' column
		Column 'Breakdown Category' will have to be split out
		Add 'Loneliness' column with values 'Never', 'Hardly ever' etc. Set rows from other sheets to 'All'
		Add 'Sex' column with values 'M' and 'F'. Set rows from other sheets to 'T'
		Add 'Marital Status' column with values 'Single', Widowed' etc. Set rows from other sheets to 'All'
		Add 'Feeling Safe' column with values 'Very Safe', 'Safe' etc. Set rows from other sheets to 'All'
		Add 'Work Affected' column with values ''Not, My work is being affected', 'My work is being affected'. Set rows from other sheets to 'All'
		Add 'Disability' column with values 'Non-disabled', 'Disabled' etc. Set rows from other sheets to 'All'
		Remove 'Breakdown Category' column
		Set 'Measure Type' column to value 'Anxiety'
		Set 'Unit' column to value 'Rating Scale'

		Keep Sample size out of data for now but if needed format as above but:
		'Measure Type' = 'Count'
		'Unit' = 'Sample Size'
	
#### Output Dataset Name:

		Coronavirus and Anxiety Estimates - GB - average ratings

#### Table

		Period, Loneliness, Sex, Marital Status, Feeling Safe, Work Affected, Disability, Measure Type, Unit, Value

##### Footnotes

		To be added to metadata:
		Statistics in this release have been taken from five waves of the Opinions and Lifestyle Survey (OPN), a monthly omnibus survey. In response to the coronavirus (COVID-19) pandemic, we have adapted the OPN to become a weekly survey used to collect data on the impact of the coronavirus on day-to-day life in Great Britain.
		Question: Respondents were asked “Overall, how anxious did you feel yesterday?” and answered on a scale of 0 to 10, where 0 is “not at all” and 10 is “completely”.
		Comparisons must be made with caution as these estimates are provided from a sample survey. As such, confidence intervals are produced to present the sampling variability which should be taken into account when assessing change, as true differences may not exist. 

#### DM Notes

	co-efficient of variation (CV) has not been considered as it is colour coded and would need manual processing for each new release. Added note to Github card and informed BAs

