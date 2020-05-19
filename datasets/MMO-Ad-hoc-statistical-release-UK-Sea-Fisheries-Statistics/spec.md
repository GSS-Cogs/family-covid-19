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
		Add Measure Type column with values GBP Thousands, Weight and Annual Percentage Change
		Add Unit column with values GBP, Tonnes, Percent
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column

#### Sheet: Table 2 - Activity (value, volume landed and number of trips) of the UK fishing fleet by country and admin port

		D6:E6 - Year - change to Period and format as required
		B:C - Country & Admin Port - change to ONS Geography Code and change values to 9 digit codes
			Ignore Unknown rows for now as we currently do not have a Geography code for it
		Add Vessel Length column with value All
		Add Species Group column with value All
		F, J, N Change has latest Year in Period column
		Add Measure Type column with values GBP Thousands, Weight and Annual Percentage Change
		Add Unit column with values GBP, Tonnes, Trips
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
		Add Measure Type column with values GBP Thousands, Weight and Annual Percentage Change
		Add Unit column with values GBP, Tonnes, Percent
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
		Add Measure Type column with values GBP Thousands, Weight and Annual Percentage Change
		Add Unit column with values GBP, Tonnes, Percent
		Any values of .. to be replaced with 0 and "Figure less than 1" put in Marker column
		
##### Footnotes

		Please note this release contains provisional data and therefore may not provide a complete picture of recent fishing activity.
		A high volume landing of mackerel by an English vessel has missing data. Therefore, to give a more realistic estimate, the value for this landing has been imputed based on March 2019 mackerel prices


**DM Notes**

Intro													
														
The MMO publishes national statistics on fishing activity across the UK on a monthly basis with a two month lag: 
https://www.gov.uk/government/collections/monthly-uk-sea-fisheries-statistics.

In response to COVID-19, the MMO will be publishing an additional ad hoc statistical release with more timely figures on fishing activity data. This will be published monthly while coronavirus continues to have a large impact on the fishing industry.

In publishing more timely data we are accepting a reduction in data quality as the picture of fishing activity may not be complete while data is still being processed. This release is therefore not badged as national statistics, reflecting the temporary nature of the recurring publication and the reduced data quality when compared to our regular monthly national statistics. 

We welcome feedback on this publication. Please submit your comments here: https://forms.gle/Qoaty1byCddJYryb9.
												

**Glossary**	
	
Demersal: Species of demersal fish inhabit the bottom of the ocean. Key demersal species fished by the UK fleet include cod, haddock and whiting. 
	
Pelagic: Pelagic fish inhabit the water column (not near the sea bed or shore). The two main pelagic species fished by the UK fleet are mackerel and herring. 
	
Shellfish: Shellfish include various species of molluscs (e.g. scallops, whelks) and crustaceans (e.g. crabs and nephrops).
	
Number of trips: The number of distinct trips (out from port and back to port) where fish were landed taken by a given group of vessels in a given time frame. The same vessel will account for multiple trips.
	
Admin port: Vessels are registered with specific ports. This is not necessarily where they land all their catches but gives an indication of where vessels are based around the UK and its nations.
	
Value: In this publication the value in £000's is reported. This is the value fishers received for their landings at first sale as recorded on sales notes from Registered Buyers and Sellers of fish.
	
Quantity: The quantity in tonnes in reported. This is the live weight of fish caught and landed by fishers. 


