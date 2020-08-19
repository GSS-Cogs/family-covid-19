<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## ONS Deaths involving COVID-19 by local area and deprivation

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingcovid19bylocalareaanddeprivation)

[Transform Flowchart]()

### Stage 1. Transform

#### Sheet: Table 1

	A6:A113 - Cause of Death 
    B6:B113 - Sex
    C6:C113 - Area of usual residence code
    D6:D113 - Area of usual residence name 
    E4:AD4 - Period 
    G6:G113, M6:M113, S6:S113, Y6:Y113, AE6:AE113 - Rate (Attribute)
    I6:I113, O6:O113, U6:U113, AA6:AA113, AG6:AG113 - Lower CI (Attribute)
    J6:J113, P6:P113, V6:V113, AB6:AB113, AH6:AH113 - Upper CI (Attribute)
    Add Country column with value England and Wales
	Add Measure Type column with value Count
	Add Unit column with value Deaths

#### Table Structure
    Period, Cause of death, Sex, Area of usual residence code, Area of usual residence name, Rate, Lower CI, Upper CI, Value, Measure Type, Unit

#### Sheet: Table 2

    A6:A3488 - Cause of Death 
    B6:B3488 - Sex
    D6:D3488 - Area of usual residence code
    E6:E3488 - Area of usual residence name 
    G4:AE4 - Period 
    H6:H3488, N6:N3488, T6:T3488, Z6:Z3488, AF6:AF3488 - Rate (Attribute)
    J6:J3488, P6:P3488, V6:V3488, AB6:AB3488, AH6:AH3488 - Lower CI (Attribute)
    K6:K3488, Q6:Q3488, W6:W3488, AC6:AC3488, AI:AI3488 - Upper CI (Attribute)
    Add Country column with value England and Wales
	Add Measure Type column with value Count
	Add Unit column with value Deaths

#### Table Structure
     Period, Cause of death, Sex, Area of usual residence code, Area of usual residence name, Rate, Lower CI, Upper CI, Value, Measure Type, Unit
            
#### Sheet: Table 3
    A6:A95 - Cause of death 
    B6:B95 - Sex
    C7:C95 - Declie 
    E4:AD4 - Period 
    F6:F96, L6:L96, R6:R96, X6:X96, AD6:AD96 - Rate (Attribute)
    H6:H96, N6:N96, T6:T96, Z6:Z96, AF6:AF96 - Lower CI (Attribute)
    IF6:I96, O6:O96, U6:U96, AA6:AA96, AG6:AG96 - Upper CI (Attribute)
    Add Country column with value England
	Add Measure Type column with value Count
	Add Unit column with value Deaths
    
#### Table Structure
    Period, Cause of death, Sex, Country, Decile, Rate, Lower CI, Upper CI, Value, Measure Type, Unit

#### Sheet: Table 4
    A6:A50 - Cause of death 
    B6:B50 - Sex
    C7:C50 - Quintile 
    E4:AD4 - Period 
    F6:F50, L6:L50, R6:R50, X6:X50, AD6:AD50 - Rate (Attribute)
    H6:H50, N6:N50, T6:T50, Z6:Z50, AF6:AF50 - Lower CI (Attribute)
    IF6:I50, O6:O50, U6:U50, AA6:AA50, AG6:AG50 - Upper CI (Attribute)
    Add Country column with value Wales
	Add Measure Type column with value Count
	Add Unit column with value Deaths

#### Table Structure
    Period, Cause of death, Sex, Country, Quintile, Rate, Lower CI, Upper CI, Value, Measure Type, Unit
              
#### Sheet: Table 5
    A14:A7214 - MSOA code 
    B14:B7214 - ONS geography MSOA name
    C14:B7214 - House of Commons Library MSOA Names
    E12:Q12 - Cause of death
    E12:Q12 - Period   
    Add Country column with Zalue England and Wales
    Add Measure Type column with value Count
    Add Unit column with value Deaths

#### Table Structure
    Period, Cause of death, Country, MSOA code, ONS geography MSOA name, House of Commons Library MSOA Names, Value, Measure Type, Unit

#### Sheet: Table 6
    A6:A25 - Cause of death
    B6:B25 - Rural-Urban Classification Areas
    D4:AB4 - Period 
    E6:E25, K6:K25, Q6:Q25, W6:W25, AC6:AC25 - Rate (Attribute)
    G6:G25, M6:M25, S6:S25, Y6:Y25, AE6:AE25 - Lower CI (Attribute)
    H6:H25, N6:N25, T6:T25, E6:Z25, AF6:AF25 - Upper CI (Attribute)
    Add Country column with value England and Wales
    Add Measure Type column with value Count
    Add Unit column with value Deaths
    
#### Table Structure
    Period, Cause of death, Country, Rural-Urban Classification Areas, Rate, Upper CI, Lower CI Value, Measure Type, Unit

#### Sheet: Table 7
    A6:A227 - Cause of death 
    B6:B227 - Major Towns and Cities
    D4:AB4 - Period 
    E6:E227, K6:K227, Q6:Q227, W6:W227, AC6:AC227 - Rate (Attribute)
    G6:G227, M6:M227, S6:S227, Y6:Y227, AE6:AE227 - Lower CI (Attribute)
    H6:H227, N6:N227, T6:T227, E6:Z227, AF6:AF227 - Upper CI (Attribute)
    Add Country column with value England and Wales
    Add Measure Type column with value Count
    Add Unit column with value Deaths
    
#### Table Structure
    Period, Cause of death, Country, Major Towns and Cities, Rate, Upper CI, Lower CI Value, Measure Type, Unit

#### Sheet: Table 8 

    A6:A351 - Cause of death
    B6:B351 - Travel To Work Areas
    D4:AB4 - Period     
    E6:E351, K6:K351, Q6:Q351, W6:W351, AC6:AC351 - Rate (Attribute)
    G6:G351, M6:M351, S6:S351, Y6:Y351, AE6:AE351 - Lower CI (Attribute)
    H6:H351, N6:N351, T6:T351, Z6:Z351, AF6:AF351 - Upper CI (Attribute)
    Add Country column with value Wales
	Add Measure Type column with value Count
	Add Unit column with value Deaths

#### Table Structure
    Period, Cause of death, Country, Travel To Work Areas, Rate, Upper CI, Lower CI Value, Measure Type, Unit

       
##### Footnotes 
    Each tab has various footnotes and details markers. See source for details. 


### Stage 2. Harmonise

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: 2

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

##### Footnotes

		footnotes

##### DM Notes

		notes

<!-- #endregion -->

```python

```
