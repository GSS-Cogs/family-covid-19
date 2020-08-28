# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## ONS Which occupations have the highest potential exposure to the coronavirus COVID-19

[Landing Page](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Which-occupations-have-the-highest-potential-exposure-to-the-coronavirus-COVID-19/flowchart.ttl)

### Stage 1. Transform

#### Sheet: Occupations and exposure

        A4:A362 - UK SOC 2010 Code
        B4:B362 - Occupation title 
        C3,D3 - Measure Types (Proximity to others, Exposure to disease) 
        E4:E362 - Total in employment (Attribute)
        F4:F362 - Median hourly pay (£) (Attribute)
        G4:G362 - Percentage of the workforce that are female(%) (Attribute)
        H4:H362 - Percentage of the workforce that are aged 55+ (%) (Attribute)
        I4:I362 - Percentage of the workforce that are BAME (%) (Attribute)
        Add Unit column with value: standardised to a scale

#### Table Structure

		UK SOC 2010 Code, Occupation title, Total in employment, Median hourly pay (£), Percentage of the workforce that are female, Percentage of the workforce that are aged 55+, Percentage of the workforce that are BAME, Measure type, Unit, Value


##### Notes 
    The observations are those values that fall below the two Measure types (Proximity to others, Exposure to disease)
    These are measured using a standardised scale;
    
    The standardised exposure to disease or infections measure is defined by:
    0 – Never
    25 – Once a year or more but not every month
    50 – Once a month or more but not every week
    75 – Once a week or more but not every day
    100 – Every day
    please follow link for more information. 
        https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11

#### Sheet: Total_workforce_population

        A4 - Occupation title 
        B3:D3 - Workforce category
        Add Measure type column with value: Percentage
        Add Unit column with value: Percent

#### Table Structure
    Occupation title, Workforce category, Measure type, Unit, Value


### Stage 2. Harmonise

#### Sheet: Occupations and exposure

		Convert column 'UK SOC 2010 Code' to an Integer
		Change name of 'Measure Type' column to 'Working Condition Category' (will have problems with duplicate rows otherwise)
		Change the following column names
			'Occupation title' --> 'Occupation'
			'Median hourly pay (£)' --> 'Median hourly pay'
			'Percentage of the workforce that are female' --> 'Percentage Workforce Female'
			'Percentage of the workforce that are aged 55+' --> 'Percentage Workforce Aged 55plus'
			'Percentage of the workforce that are BAME' --> 'Percentage Workforce BAME'
		Create new 'Measure Type' column with values:
				Proximity to others = Proximity
				Exposure to Disease = Exposure
		Change 'Unit' column value to 'Standardised Scale'

		If not already in the metadata add link to report/methodology:
		https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11
		Also add the footnotes to the metadata


#### Table Structure

		UK SOC 2010 Code, Occupation, Total in employment, Median hourly pay, Percentage Workforce Female, Percentage Workforce Aged 55plus, Percentage Workforce BAME, Working Condition Category, Measure type, Unit, Value

#### Output Dataset Name

		Which occupations have the highest potential exposure to the coronavirus COVID-19


#### Sheet: Total workforce population

		Remove column 'Occupation Title'
		Change 'Workforce Category' values to:
			'Percentage of the workforce that are female(%)' --> 'Females'
			'Percentage of the workforce that are aged 55+ (%)' --> 'Aged 55plus'
			'Percentage of the workforce that are BAME (%)' --> 'BAME'

		If not already in the metadata add link to report/methodology:
		https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11

#### Table Structure

		Workforce Category, Measure Type, Unit, Value

#### Output Dataset Name

		Which occupations have the highest potential exposure to the coronavirus COVID-19 - Total Workforce Population

##### Footnotes

		footnotes

--------------

##### DM Notes

		Will have to check to see if the Occupation data is already available as an ontology that can be referenced rather than create out own
		Could have flattened everything but then everything would be from different distributions and it looks better as it is.

