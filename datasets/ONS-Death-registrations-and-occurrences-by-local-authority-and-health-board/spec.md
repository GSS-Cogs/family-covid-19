# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## ONS Death registrations and occurrences by local authority and health board 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/causesofdeath/datasets/deathregistrationsandoccurrencesbylocalauthorityandhealthboard/2020)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Death-registrations-and-occurrences-by-local-authority-and-health-board/flowchart.ttl)

----------
#### No stage 1 as I jumped straight to Stage 2
#### KEEP THE 2 DATASETS SEPARATE

### Stage 2. Alignment

#### Sheet: Registrations - All Data

		Period
			Week number -> Week, formatted as 'week/{year}-W{wk}'
		Geography
			Keep column 'Area Code'
			Remove columns 'Geography type' and Area name'
		Dimensions
			'Cause of death' (codelist)
			'Place of death' (codelist)
		Value
			'Number of deaths' -> 'Value'
		Measure Type = Deaths
		Unit = Count

		Scraper
			Title = Death Registrations by Local Authority and Health Board
			Description = These figures represent death occurrences and registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release:\n https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/latest
			Comment = Provisional counts of the number of deaths registered in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.
			Family = covid-19
			CSV filename: registrations-observations.csv
			Dataset Path: add to end of normal path: - '/registrations'

#### Table Structure

		Week, Area Code, Cause of death, Place of death, Value

#### Sheet: Occurrences - All Data

		Period
			Week number -> Week, formatted as 'week/{year}-W{wk}'
		Geography
			Keep column 'Area Code'
			Remove columns 'Geography type' and Area name'
		Dimensions
			'Cause of death' (codelist)
			'Place of death' (codelist)
		Value
			'Number of deaths' -> 'Value'
		Measure Type = Deaths
		Unit = Count

		Scraper
			Title = Death Occurrences by Local Authority and Health Board
			Description = These figures represent death occurrences and registrations, there can be a delay between the date a death occurred and the date a death was registered. More information can be found in our impact of registration delays release:\n https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/impactofregistrationdelaysonmortalitystatisticsinenglandandwales/latest
			Comment = Provisional counts of the number of death occurrences in England and Wales, including deaths involving the coronavirus (COVID-19), by local authority, health board and place of death in the latest weeks for which data are available.
			Family = covid-19
			CSV filename: occurrences-observations.csv
			Dataset Path: add to end of normal path: - '/occurrences'

#### Table Structure

		Week, Area Code, Cause of death, Place of death, Value

#### Info.json

		File has been set up with column definitions, 
		'Cause of death' and 'Place of death' dimensions have been set up to reference:
			http://gss-data.org.uk/data/gss_data/covid-19/ons-death-registrations-and-occurrences-by-local-authority-and-health-board/
		rather than have individual code lists for each dataset
-------------

##### Footnotes

		footnotes

##### DM Notes

		notes

