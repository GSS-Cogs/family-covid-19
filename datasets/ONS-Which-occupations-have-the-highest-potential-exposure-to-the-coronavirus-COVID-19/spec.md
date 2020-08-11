<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## ONS Which occupations have the highest potential exposure to the coronavirus COVID-19

[Landing Page](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/articles/whichoccupationshavethehighestpotentialexposuretothecoronaviruscovid19/2020-05-11)

[Transform Flowchart]

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
    These are measured using a sandardised scale;
    
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
    Occupation title , Workforce category, Measure type, Unit, Value


### Stage 2. Harmonise

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
