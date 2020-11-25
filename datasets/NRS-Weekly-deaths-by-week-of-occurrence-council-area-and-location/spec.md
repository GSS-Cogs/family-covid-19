# COGS Dataset Specification

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## NRS Weekly deaths by week of occurrence, council area and location

[Landing Page](https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/general-publications/weekly-and-monthly-data-on-births-and-deaths/deaths-involving-coronavirus-covid-19-in-scotland/related-statistics)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NRS-Weekly-deaths-by-week-of-occurrence-council-area-and-location/flowchart.ttl)

#### NOTE: ONLY FIRST DATASET ON LANDING PAGE HAS BEEN TRANSFORMED AS MATCHES THE MAIN TITLE. ALTHOUGH THE OTHER DATASETS WOULD BE QUITE INTERESTING TO HAVE ON PMD4


#### Sheet: Weekly deaths by week of occurrence, council area and location

	Week of Occurrence: format as week/{year}-{week} - week/2020-01
	Remove column Period
	Area has already been converted to ONS Geography codes but ensure the codes are for Council areas
	Cause of Death: codelist and pathify
	Location of Death: have added back into the final column sort as it was not there. Codelist and pathify

	Measures:
		Measure Type: deaths
		Unit: count

	Scraper:
		dataset_id: should be correct as is
		Title: should be correct as is
		Comment: Weekly Covid-19 and Non-Covid-19 deaths by week of occurrence, council area and location
		Description:
			Weekly Covid-19 and Non-Covid-19 deaths by week of occurrence, council area and location
			This data is from user requests for ad-hoc analysis related to COVID-19 deaths data. As these data may be useful for others, we are making them available to download for any users of our data.
		Family: covid-19

#### Table Structure

		Week of Occurrence, Area, Location of Death, Cause of Death, Value
		
##### Footnotes

		footnotes

##### DM Notes

		notes

