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

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: 2

		spec

----------#### Table Structure

		Period, Measure Type, Unit, Marker, Value

--------------##### Footnotes

		footnotes

##### DM Notes

		notes

<!-- #endregion -->
