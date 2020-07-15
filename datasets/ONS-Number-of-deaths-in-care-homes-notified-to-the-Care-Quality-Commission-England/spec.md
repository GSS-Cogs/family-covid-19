<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## ONS Number of deaths in care homes notified to the Care Quality Commission, England 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/numberofdeathsincarehomesnotifiedtothecarequalitycommissionengland)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Number-of-deaths-in-care-homes-notified-to-the-Care-Quality-Commission-England/flowchart.ttl)

----------### Stage 1. Transform

#### Sheet: Table 1

		A4:A89 - Date of Notification 
        B3:C3 - Place of Occurrence (Codelist)
        Add Death Causes Column with value: Involving COVID-19
        Add Local Authority Column with value: England
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count
        

#### Table Structure

		Date of notification, Place of Occurrence, Death Causes, Local Authority, Measure Type, Unit, Marker, Value

#### Sheet: Table 2

		B3:CH3 - Date of Notification 
        A4:A153 - Local Authority 
        Add Death Causes Column with value: Involving COVID-19
        Add Place of Occurrence Column with value: Care homes
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count

#### Table Structure

		Date of notification, Place of Occurrence, Death Causes, Local Authority, Measure Type, Unit, Marker, Value

#### Sheet: Table 3

		B3:CH3 - Date of Notification 
        A4:A153 - Local Authority 
        Add Death Causes Column with value: All causes
        Add Place of Occurrence Column with value: Care homes
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count

#### Table Structure

		Date of notification, Place of Occurrence, Death Causes, Local Authority, Measure Type, Unit, Marker, Value

#### Sheet: Table 4

		B4:M4 - Week Ending 
        A5, A11 - Death Causes (Codelist)
        A6:A9, A12:A15 - Place of Occurrence (Codelist)
        Add Local Authority Column with value: England
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count

#### Table Structure

		Week Ending, Place of Occurrence, Death Causes, Local Authority, Measure Type, Unit, Marker, Value

#####  Notes 
    Tables can easily be harmonised and outputted as one cube once the formating of Date of Notification and Week Ending is correct. 

-------------### Stage 2. Harmonise

#### Sheet: 1 - Table 1, 2, 3 and 4 to join in one cube.

		Date of Notification to include week ending and daily 
		Location to add value of ONS Geography code England and codelist for Local Authority locations 
		Place of Occurence add value of Care Home, Hospital, Elsewhere, Not Stated
		Death Causes with values for COVID-19 and All causes
		Add Measure Type, Unit as Count, Marker, Value as Deaths
		Add metadata as an Attribute:
		Data provided by Care Quality Commission., Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 3 Jul 2020, and may be an underestimate due to notification delays., Figures are for persons who were resident and died in a care home., Figures don't include 10 April 2020 as the first full week of data for deaths involving COVID-19 began on 11 April 2020.
		

#### Table Structure

		Date of Notification, Location, Place of Occurence, Death Causes, Measure Type, Unit, Marker, Value

##### DM Notes

		Information tab contains comprehensive info data source and general data information - too long to include in description and as an attribute.

<!-- #endregion -->
