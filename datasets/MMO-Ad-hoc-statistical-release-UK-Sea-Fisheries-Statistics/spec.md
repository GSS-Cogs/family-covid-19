# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Development](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## MMO Ad hoc statistical release UK Sea Fisheries Statistics 

### Marine Management Organisation

[Landing Page](https://www.gov.uk/government/collections/ad-hoc-statistical-releases-sea-fisheries-statistics)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?MMO-Ad-hoc-statistical-release-UK-Sea-Fisheries-Statistics/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		MMO Ad-Hoc UK Sea Fisheries Statistical Release

#### Table Structure

		Period, ONS Geography Code, Vessel Length, Species Group, Measure Type, Unit, Marker, Value

#### Sheet: Table 1 - Activity (value and volume landed) of the UK fishing fleet by country, vessel length and species group

		D6:E6 - Year - change to Period and format as required
		B8, B21, B34, B47, B60 - UK and Nations - change to ONS Geography Code and use 
			Wales - W08000001
			Scotland - S04000001
			Northern Ireland - N07000001
			England - E92000001
			United Kingdom - K02000001
		C9, C13, C17 - Vessel Length (Codelist)
			u10m total - u10m			(Under 10 Metres)
			10-12m total - 10-12m			(10 to 12 Metres)
			012m total - o12m			(Over 12 Metres)
			Add Total category
		C10:C12 - Species Group (Codelist)
			Demersal
			Pelagic
			Shellfish
			Add All category	
		F, J Change has latest Year in Period column
		Add Measure Type column with values GBP Thousands, Quantity and Annual Percentage Change
		Add Unit column with values GBP, Count, Percent
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column

#### Sheet: Table 2 - Activity (value, volume landed and number of trips) of the UK fishing fleet by country and admin port

		D6:E6 - Year - change to Period and format as required
		B:C - Country & Admin Port - change to ONS Geography Code and change values to 9 digit codes
			Ignore Unknown rows for now as we currently do not have a Geography code for it
		Add Vessel Length column with value All
		Add Species Group column with value All
		F, J, N Change has latest Year in Period column
		Add Measure Type column with values GBP Thousands, Quantity and Annual Percentage Change
		Add Unit column with values GBP, Count, Trips
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column

#### Sheet: Table 3 - Activity (value and volume landed) of the UK fishing fleet by species group and country

		D6:E6 - Year - change to Period and format as required
		B8, C10:C13 - Country - change to ONS Geography Code and change values to 9 digit codes
		B9, B14, B19 - Species Group (Codelist)
			Demersal
			Pelagic
			Shellfish
			Add All category	
		F, J Change has latest Year in Period column
		Add Measure Type column with values GBP Thousands, Quantity and Annual Percentage Change
		Add Unit column with values GBP, Count, Percent
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column

#### Sheet: Table 4 - Activity (value and volume landed) of the UK fishing fleet by country and vessel length

		D6:E6 - Year - change to Period and format as required
		B8, B14, B20, B26, B32 - Country - change to ONS Geography Code and change values to 9 digit codes
		C9:C13 - Vessel Length (Codelist)
			u10m
			10-12m
			12-15m
			15-24m
			o24m	
		F, J Change has latest Year in Period column
		Add Measure Type column with values GBP Thousands, Quantity and Annual Percentage Change
		Add Unit column with values GBP, Count, Percent
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column
		
##### Footnotes

		Please note this release contains provisional data and therefore may not provide a complete picture of recent fishing activity.
		A high volume landing of mackerel by an English vessel has missing data. Therefore, to give a more realistic estimate, the value for this landing has been imputed based on March 2019 mackerel prices


**DM Notes**

Demersal: https://en.wikipedia.org/wiki/Demersal_fish

Pelagic: https://en.wikipedia.org/wiki/Pelagic_fish


