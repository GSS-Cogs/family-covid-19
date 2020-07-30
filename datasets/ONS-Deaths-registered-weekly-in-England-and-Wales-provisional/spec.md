<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## # ONS Deaths registered weekly in England and Wales, provisional 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/weeklyprovisionalfiguresondeathsregisteredinenglandandwales)

[Transform Flowchart]

----------### Stage 1. Transform

#### Sheet 01 : Weekly figures 2020

        note this sheet might be easier to transform in sections; 
            - Total Deaths : Rows 9 to 15
            - Death by cause : Rows 17 - 19
            - By age group and Sex : rows 20 - 85
            - Death by region of usual residence : rows 87 - 96 
          
        Standard across all sections:
            C5:AE5 - Week number
            C6:AE6 - Week ended 
    
        Section: Death by region of usual residence : rows 87 - 96 
            B87:B96 - Region 
            Add Death grouped by Column with value: Deaths by region of usual residence
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Death Cause Column with value: unknown
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
         
        Section: By age group and Sex : rows 20 - 85
            B22:B41, B44:B63, B66:B85 - Age group
            B20, B42, B64 - Sex
            Add Region Column with value: England and Wales
            Add Death grouped by Column with value: Deaths by age group
            Add Death Cause Column with value: unknown
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count

        Section: Death by cause : Rows 17 - 19
            B18:B19 - Death Cause 
            Add Region Column with value: England and Wales
            Add Death grouped by Column with value: Deaths by cause
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
            
        Section: Total Deaths : Rows 9 to 15
            A9:A15 - Death grouped by
            A9:A15 - Region (Note region data is at the end of death grouped by data, filter out as required.)
            Add Death Cause Column with value: unknown
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
#### Table Structure

		Week number, Week ended, Sex, Age Group, Region, Weekly registrations or occurrences , Death grouped by, Death cause, Value, Measure Type, Unit

#### Sheet 02: Covid-19 - Weekly registrations and Covid-19 
           
         note each sheet might be easier to transform in sections; 
            - By age group and Sex : rows 8 - 75
            - Deaths by region of usual residence : rows 76 - 86 
          
         Standard across all sections:
            C5:AE5 - Week number
            C6:AE6 - Week ended 
            
          Section: By age group and Sex : rows 8 - 75
            B9, B12:B31, B34:B53, B66:B85 - Age group
            B10, B32, B54 - Sex
            Add Region Column with value: England and Wales
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
         
         Section : Deaths by region of usual residence : rows 76 - 86 
            B77:B86 - Region 
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count

#### Table Structure
        Week number, Week ended, Weekly registrations or occurrences, Sex, Age group, Region, Measure Type, Unit
           
           
#### Sheet 03: Covid-19 - Covid-19 - Weekly occurrences
           
         note each sheet might be easier to transform in sections; 
            - By age group and Sex : rows 8 - 75
            - Deaths by region of usual residence : rows 76 - 86 
          
         Standard across all sections:
            C5:AE5 - Week number
            C6:AE6 - Week ended 
            
          Section: By age group and Sex : rows 8 - 75
            B9, B12:B31, B34:B53, B66:B85 - Age group
            B10, B32, B54 - Sex
            Add Region Column with value: England and Wales
            Add Weekly registrations or occurrences Column with value: Occurrences
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
         
         Section : Deaths by region of usual residence : rows 76 - 86 
            B77:B86 - Region 
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Weekly registrations or occurrences Column with value: Occurrences
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
             
        

#### Table Structure
        Week number, Week ended, Weekly registrations or occurrences, Sex, Age group, Region, Measure Type, Unit


#### Sheet 04: Covid-19 - UK - Covid-19 - Weekly reg
            
         note each sheet might be easier to transform in sections; 
            - UK deaths involving COVID-19, all ages : rows 8 - 12
            - Deaths involving COVID-19 by age : rows 14 - 41
            
         Standard across all sections:
            A4:AE4 - Week number
            A5:AE4 - Week ended 

        Section : UK deaths involving COVID-19, all ages : rows 8 - 12
            A8:A12 - Region 
            Add Sex Column with value: Persons
            Add Age group Column with value: All ages
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
        
        Section : Deaths involving COVID-19 by age : rows 14 - 41
            B17:B23, B25:32, B35:B41 - Age group
            B15, B24, B33 - Sex
            Add Region Column with value: All UK
            Add Weekly registrations or occurrences Column with value: Registrations
            Add Measure Type Column with value: Deaths
            Add Unit column with value: Count
            

#### Table Structure
        Week number, Week ended, Weekly registrations or occurrences, Sex, Age group, Region, Measure Type, Unit


#### Sheet 05: Covid-19 - E&W comparisons
        A6:A140 - Date 
        B5:E5 - Comparison Category 
        Add Region Column with value: England and Wales
        Add Weekly registrations or occurrences Column with value: Registrations and Occurrences
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count
        

#### Table Structure
    Date, Region, Comparison Category, Weekly registrations or occurrences, Measure Type, Unit


#### Sheet 06: Covid-19 - England comparisons
        A6:A140 - Date 
        B5:E5 - Comparison Category 
        Add Region Column with value: England
        Add Weekly registrations or occurrences Column with value: Registrations and Occurrences
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count
        

#### Table Structure
    Date, Region, Comparison Category, Weekly registrations or occurrences, Measure Type, Unit

#### Sheet 07: Covid-19 - Wales comparison
        A6:A140 - Date 
        B5:E5 - Comparison Category 
        Add Region Column with value: Wales
        Add Weekly registrations or occurrences Column with value: Registrations and Occurrences
        Add Measure Type Column with value: Deaths
        Add Unit column with value: Count
        

#### Table Structure
    Date, Region, Comparison Category, Weekly registrations or occurrences, Measure Type, Unit

#### Sheet 08: Covid-19 - Covid-19 - Place of occurrence 
       
       note each sheet might be easier to transform in sections; 
           - Deaths registered Week ended comparision : rows 8 - 14
           - Deaths registered date duration : rows 16 - 25
            
       Section : Deaths registered Week ended comparision : rows 8 - 14
           B5:DF5 - Week ended (Period) 
           B7:DF7 - Region
           B8:DF8 - Death classification 
           A9:A14 - Place of occurance
           Add Weekly registrations or occurrences Column with value: Registrations
           Add Measure Type Column with value: Deaths
           Add Unit column with value: Count
       
       Section : Deaths registered date duration : rows 16 - 25
           A16 - Date range (Period)
           B17:DF17 - Region
           B18:DF18 - Death classification 
           A19:A25 - Place of occurance
           Add Weekly registrations or occurrences Column with value: Registrations
           Add Measure Type Column with value: Deaths
           Add Unit column with value: Count


#### Table Structure
        Week number, Period, Region, Death classification, Place of occurance, Weekly registrations or occurrences, Marker, Measure Type, Unit


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

```python

```

```python

```
