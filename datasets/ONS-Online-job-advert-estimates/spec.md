<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## ONS Online job advert estimates 

[Landing Page](https://www.ons.gov.uk/economy/economicoutputandproductivity/output/datasets/onlinejobadvertestimates)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Online-job-advert-estimates/flowchart.ttl)

----------### Stage 1. Transform

#### Sheet: Vacancies

        B12:CA12 - Date
        A13:A42 - Industry 
        A43:CA43 - Marker (Inputed Values row across relates to the following note: "Furthermore some weeks have no observation. The missing  values have been imputed using linear interpolation, and have been highlighted." Format as required)
        Add Measure Type Column with value: Adverts
        Add Unit column with value: Count

#### Table Structure

		Date, Industry, Value, Marker, Measure Type, Unit



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
