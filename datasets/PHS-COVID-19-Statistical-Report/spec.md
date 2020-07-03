# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/index.html)

------

## PHS COVID-19 Statistical Report 
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

------

## PHS COVID-19 Statistical Report 

[Landing Page Council Areas](https://www.opendata.nhs.scot/dataset/b318bddf-a4dc-4262-971f-0ba329e09b87/resource/e8454cf0-1152-4bcb-b9da-4343f625dfef/download/total_cases_by_la_04062020.csv)

[Landing Page Cumulative Cases](https://www.opendata.nhs.scot/dataset/b318bddf-a4dc-4262-971f-0ba329e09b87/resource/287fc645-4352-4477-9c8c-55bc054b7e76/download/daily_cumulative_counts_04062020.csv)

[Landing Page Healthboard Cases](https://www.opendata.nhs.scot/dataset/b318bddf-a4dc-4262-971f-0ba329e09b87/resource/7fad90e5-6f19-455b-bc07-694a22f8d5dc/download/total_cases_by_hb_04062020.csv)

#### Open Data available at:

[Open Data Platform](https://www.opendata.nhs.scot/dataset/covid-19-in-scotland)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?PHS-COVID-19-Statistical-Report/flowchart.ttl)

--------

### 1. Transform

#### Open Data source needs to be investigated to see what is available
#### Has been split into 3 datasets with 3 different json files 	

1. Council Area Cases

	Sheet: total_cases_by_la_{date}

		A - CA (Council Area)
		B - Total Cases

2. Cumulative Cases

	Sheet: daily_cumulative_counts_{date}	

		A - Date
		B - DailyCases
		C - CumulativeCases
		D - Deaths
		E - DeathsQF


3. Healthboard Cases

	Sheet: total_cases_by_hb_{date}

		A - HB (Health Board)
		B - Total Cases
			
--------

### 2. Alignment

-----

##### Footnotes

		footnotes
