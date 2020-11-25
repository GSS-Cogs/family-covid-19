# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## NRS Births, deaths, and other vital events 

[Landing Page](https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/general-publications/births-deaths-and-other-vital-events-quarterly-figures)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NRS-Births-deaths-and-other-vital-events/flowchart.ttl)

----------
#### Consists of 6 zipped csv files for the latest Quarter. The first one gives details for births, deaths and marriages for all of Scotland  by quarter. The second does the same but with population estimates by Admin area but only for the latest quarter. The third gives deaths by age and sex by admin area. The forth gives deaths by cause for all of Scotland. The fifth gives deaths by sex, age and cause for all of Scotland. The sixth gives deaths by sex, caused NHS board got all of Scotland. 
---------
#### Sheet: quarter-2-20-tables_Q1_.csv

	Rename Sex column to Sex
	Measurement 
		Rename 'Vital Event' but it only contains the value in row 3: 
			Live births, Stillbirths, Perinatal deaths, Neonatal deaths, Infant deaths, Deaths - all ages, Marriages, Civil Partnerships
	Set and '-' values to 0

#### Dataset one - Births, Stillbirths etc.

	Live births
		Vital Event, 	Sex, 	Parent Marital Status,		Measure Type,				Unit
		Live births,	T,	married,		count,				births
		Live births,	F,	married,		count,				births
		Live births,	M,	married,		count,				births
		Live births,	T,	married,		rate-per-1000-population,				births
		Live births,	T,	unmarried,		count,				births

		Ignore 'males per 1,000 females' as it can be derived from the data
		Ignore 'TO unmarried parents % of live births' as it can be derived from the data

	Stillbirths
		Vital Event,	Sex,	Parent Status,	Measure Type,			Unit
		Stillbirths,	T,	all,	count			deaths
		Stillbirths,	T,	all,	rate-per-1000-live-and-still-births			deaths

	Perinatal deaths
		Vital Event,	Sex,	Parent Status,	Measure Type,		Unit
		Perinatal deaths,	T,	all,	count		deaths
		Perinatal deaths,	T,	all,	rate-per-1000-live-and-still-births		deaths

	Perinatal deaths
		Vital Event,	Sex,	Parent Status,	Measure Type,		Unit
		Perinatal deaths,	T,	all,	count,		deaths
		Perinatal deaths,	T,	all,	rate-per-1000-live-and-still-births,		deaths

	Neonatal deaths
		Vital Event,	Sex,	Parent Status,	Measure Type,			Unit
		Neonatal deaths,	T,	all,	count,			deaths
		Neonatal deaths,	T,	all,	rate-per-1000-live-births,			deaths

	Infant deaths
		Vital Event,	Sex,	Parent Status,	Measure Type,			Unit
		Infant deaths,	T,	all,	count,			deaths
		Infant deaths,	T,	all,	rate-per-1000-live-births,			deaths

	Scraper:
		Title: Births, deaths, and other vital events, Quarterly figures - Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths  
		Comment: Quarterly figures for Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths  
		Description: 
			Quarterly figures for Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths  
			About this data
			https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-about.pdf
		Family: covid-19

	Table Structure
		Period, Vital Event, Sex, Parent Marital Status, Area (See below)
		
#### Dataset two - Deaths, Marriages, Civil Partnerships

	Deaths - all ages
		Vital Event,	Sex,	Measure Type,			Unit
		deaths - all ages,	T,	count,			deaths
		deaths - all ages,	F,	count,			deaths
		deaths - all ages,	M,	count,			deaths
		deaths - all ages,	T,	rate-per-1000-population,			deaths

	Marriages
		Vital Event,	Sex,	Measure Type,			Unit
		all marriages,	T,	count,			marriages
		all marriages,	T,	rate-per-1000-population,			marriages
		opposite sex marriages,	T,	count,			marriages
		same sex marriages,	T,	count,			marriages

	Civil Partnerships
		Vital Event,	Sex,	Measure Type,			Unit
		Civil Partnerships,	M,	count,			civil-partnerships
		Civil Partnerships,	F,	count,			civil-partnerships

	Scraper:
		Title: Births, deaths, and other vital events, Quarterly figures - Deaths, Marriages & Civil Partnerships  
		Comment: Quarterly figures for Deaths, Marriages & Civil Partnerships 
		Description:
			Quarterly figures for Deaths, Marriages & Civil Partnerships
			About this data
			https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-			about.pdf
		Family: covid-19	

	Measures:
		Measure Type: count, rate-per-1000-population
		Unit: deaths, marriages, civil-partnerships

	Table Structure
		Period, Vital Event, Sex, Area (see below)

---------------------------------------------------------

#### Sheet: quarter-2-20-tables_Q2_.csv

	HAVE COUNCIL AREA ONS GEOGRAPHIES CODES BEEN USED FOR THE COUNCIL AREAS AND HEALTH BOARD GEOGRAPHIES CODES BEEN USED FOR THE HEALTH BOARDS??????
	Measurement 
		Rename 'Vital Event' but it only contains the value in row 3: 
			Live births, Stillbirths, Perinatal deaths, Neonatal deaths, Deaths - all ages, Marriages, Civil Partnerships
	Set and '-' values to 0

#### Process as per datasets 1 & 2 above but separate out Estimated Population figures

	Process Live births, Stillbirths, Perinatal deaths, Neonatal deaths and Infant deaths as per dataset 1 (in first file) above and join. You will have to add an Area and Parent Marital Status column to dataset 1 and give it the code for Scotland
	Process Deaths - all ages, marriages and Civil Partnerships as per dataset 2 (in first file) above and join. You will have to add an Area column to dataset 2 and give it the code for Scotland
	Separate out Estimated Population and output as individual dataset, see next stage:

#### Dataset three - Estimated Population

	Remove Measurement column as no longer needed
	Rename Sex column to Sex

	Table Structure
		Period, Area, Sex, Marker, Values

	Measures
		Measure Type: people
		Unit: count
		
	Scraper:
		Title: Births, deaths, and other vital events, Quarterly figures - Estimated Population by Sex and Council Area 
		Comment: Quarterly figures for estimated population by sex and Council Area
		Description:
			Quarterly figures for estimated population by sex and Council Area
			About this data
			https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-			about.pdf
		Family: covid-19	
	
----------------------------------------------------------

### THE NEXT 4 FILES ARE JOINED AS ONE DATASETS AS THEY ARE ALL RELATED TO DEATH. THE DEATH FIGURES FROM THE FIRST FILE HAVE BEEN LEFT IN DATASET 2 TO GIVE OVERALL STATS FOR MARRIAGES, DEATHS ETC.

#### Sheet: quarter-2-20-tables_Q3_.csv

#### Dataset four - Deaths by Sex, Age, Cause of Death and Admin area

	HAVE COUNCIL AREA ONS GEOGRAPHY CODES BEEN USED FOR THE COUNCIL AREAS AND HEALTH BOARD GEOGRAPHY CODES BEEN USED FOR THE HEALTH BOARDS??????
	Rename Gender column to Sex
	Remove Measurement column as it will be the measure Type so defined in the info,json file.	
	Set and '-' values to 0
	'All ages' to be changed to 'all'
	Add column 'Cause of Death' with value 'all'

	Table Structure
		Period, Area, Age, Sex, Cause of Death, Values	

	Measures:
		Measure Type: deaths
		unit: count

	Scraper:
		Title: Births, deaths, and other vital events, Quarterly figures - Deaths by Age, Sex, Cause of Death and Administrative Area
		Comment: Quarterly figures for Deaths by Age, Sex, Cause of Death and Administrative Area
		Description:
			Quarterly figures for estimated population by sex and Council Area
			About this data
			https://www.nrscotland.gov.uk/files//statistics/births-marriages-deaths-quarterly/quarterly-pub-			about.pdf
		Family: covid-19	

#### Sheet: quarter-2-20-tables_Q4_.csv

#### Dataset four - Deaths by Sex, Age, Cause of Death and Admin area

	Period: the average figures for (2015 to 2019) have been ignored, which is good as they can easily be derived from the data
	Create codelist with the ICD 10 Summary code as the Notation and the Cause of Death string and ICD 10 Summary code as the Label, Certain infectious and parasitic diseases (A00-B99),a00-b99 etc. etc. etc. 
	Remove Cause of Death column
	Rename ICD 10 Summary List column as Cause of Death, pathify to match up with codelist
	'all Causes' to be changed to 'all'
	Add column 'Sex' with value 'T'
	Add column 'Age' with value 'all'
	Add column 'Area' with geography code for Scotland
	Set and '-' values to 0
	
	Table Structure
		Period, Area, Age, Sex, Cause of Death, Values	

#### Sheet: quarter-2-20-tables_Q5_.csv

#### Dataset four - Deaths by Sex, Age, Cause of Death and Admin area

	See previous instruction for 'Cause of Death' column
	Add column 'Area' with geography code for Scotland
	Rename Gender column to Sex and 'All' values have already been changed to 'T'
	Set and '-' values to 0
	
	Table Structure
		Period, Area, Age, Sex, Cause of Death, Values	

#### Sheet: quarter-2-20-tables_Q6_.csv

#### Dataset four - Deaths by Sex, Age, Cause of Death and Admin area

	HAVE HEALTH BOARD GEOGRAPHY CODES BEEN USED FOR THE HEALTH BOARDS??????
	See previous instruction for 'Cause of Death' column
	Rename Gender column to Sex and 'All' values have already been changed to 'T'
	Add Age column with value 'all'
	Set and '-' values to 0
	
	Table Structure
		Period, Area, Age, Sex, Cause of Death, Values	

	See age codelist on how to format age values (Y25T29 etc)

-------------------------------------------------------------------------------

## Output datasets

	Dataset 1 - Births, deaths, and other vital events, Quarterly figures - Live births, Stillbirths & Perinatal, Neonatal and Infant Deaths  
	Dataset 2 - Births, deaths, and other vital events, Quarterly figures - Deaths, Marriages & Civil Partnerships 
	Dataset 3 - Births, deaths, and other vital events, Quarterly figures - Estimated Population by Sex and Council Area 
	Dataset 4 - Births, deaths, and other vital events, Quarterly figures - Deaths by Age, Sex, Cause of Death and Administrative Area

## Flow
	Sheet: quarter-2-20-tables.csv
		Live births, Stillbirths, Perinatal deaths, Neonatal deaths, Infant deaths, Deaths - all ages, Marriages, Civil -> Dataset 1
		Deaths, Marriages & Civil Partnerships -> Dataset 2
	Sheet: quarter-2-20-tables.csv
		Live births, Stillbirths, Perinatal deaths, Neonatal deaths, Infant deaths, Deaths - all ages, Marriages, Civil -> Dataset 1
		Deaths, Marriages & Civil Partnerships -> Dataset 2
		Estimated Population -> Dataset 3
	Sheet: quarter-2-20-tables.csv -> Dataset 4
	Sheet: quarter-2-20-tables.csv -> Dataset 4
	Sheet: quarter-2-20-tables.csv -> Dataset 4
	Sheet: quarter-2-20-tables.csv -> Dataset 4

## Codelists

	Vital Events (Live Births, stillbirths, Marriages etc.)
	Cause of Death (ICD 10 Summary code to be Notation and Cause of Death (ICD code) to be Label)
	Age (Less than 4 Months, 15-24, 45-54, all etc.)
	Parent Marital Status (Married, Unmarried)
	

##### Footnotes

		footnotes

##### DM Notes

		Very complicated and messy set of data - I have created the codelists, check to see how to format values
		I have also created a flowchart to try and explain how I have split and joined the data but just message me if you want a clearer explanation.
		If the cube class is not yet working the DE will have to make changes to the info.json dictionary, changing the Measure Type and Unit depending on which dataset is being output
		If multi-measures is not working the DE will have to remove rate-per-1000 data values form the relevant dataset before publishing.

