# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## ONS Deaths involving COVID-19 in the care sector, England and Wales 

[Landing Page](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/datasets/deathsinvolvingcovid19inthecaresectorenglandandwales)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Deaths-involving-COVID-19-in-the-care-sector-England-and-Wales/flowchart.ttl)

----------### Stage 1. Transform

### NOTE - The perdio within each the datacube has a 'registerd up to' date that is different. We need to account for this somehow/somewhere in the metadata. 

#### Number of deaths of care home residents by leading cause groupings and COVID-19

#### Sheet: Table 17

Leading cause
-A6:A74 dimension 'Leading cause' taken as the CODES from column A

Sex
-C5:M5 dimension "Sex" taken from horizontal as "Persons", "Males" or "Females".

Area
-C4:K4 Area code from row near top as "England and Wales", "England" or "Wales".
-Converted all area labels to 9 digit ONS codes.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Leading cause, Sex, Area, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 6 Deaths reported in this table are for underlying causes only and do not include any mentions on the death certificate.
- 5 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 
- 4 Based on the date a death occurred rather than when a death was registered.
- 3 Based on boundaries as of May 2020
- 2 In England and Wales, a conclusion of suicide cannot be returned for children under the age of 10 years.
- 1 Excluding meningitis and meningococcal diseases (A39), sepsis due to haemophilus influenzae (A41.3), rabies (A82), certain mosquito-borne diseases (A83) and yellow fever (A95).

-----
#### Number of deaths of care home residents by age group

#### Sheet: Table 2

Sex
-B6:AJ6 Get dimension 'Sex', with values 'Persons', 'Male' and 'Female'

Age
-A9:A17 Get age dimension from column A, as number range plus 'All ages'

Area
-B4:Z4 Get dimension 'Area' with values 'England and Wales', 'England' and 'Wales'
-Converted all area labels to 9 digit ONS codes.

Period

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Sex, Age, Area, Period, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 4 Based on the date a death occurred rather than when a death was registered
- 3 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 2 Based on boundaries as of May 2020
- 1 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 

-----
#### Number of deaths of care home residents notified to the Care Quality Commission

#### Sheet: Table 7

Period
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Place of death
-B5:J5 the dimension "Place of death" taken as "Care Home", "Hospital", "Elsewhere","Not Stated"
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Area
-Set to 'England for table 7, else 'Wales'.
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Cause of death
-B4:G4 the dimension "Cause of death" taken as "All deaths", "COVID-19"
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Date of notification
-A6:A77 Period dimension taken as date types from column A plus 'Total'.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'


#### Table structure
Period, Place of death, Area, Cause of death, Date of notification, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 2 Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Quality Commission

#### Sheet: Table 8

Period
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Place of death
-B5:J5 the dimension "Place of death" taken as "Care Home", "Hospital", "Elsewhere","Not Stated"
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Area
-Set to 'England for table 7, else 'Wales'.
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Cause of death
-B4:G4 the dimension "Cause of death" taken as "All deaths", "COVID-19"
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Date of notification
-A6:A117 Period dimension taken as date types from column A plus 'Total'.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths of care home residents notified to the Care Quality Commission'
-Added to dataframe 'Number of deaths of care home residents notified to the Care Quality Commission'


#### Table structure
Period, Place of death, Area, Cause of death, Date of notification, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 2 Figures only include deaths that were notified by 5pm on 19 June 2020, and may be underestimate due to notification delays.
- 1 Data provided by Care Inspectorate Wales

#### Sheet: Number of deaths of care home residents notified to the Care Quality Commission

Period

Place of death

Area

Cause of death

Date of notification

Unit Multiplier

Measure Type

Unit of Measure


#### Table structure
Period, Place of death, Area, Cause of death, Date of notification, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes

-----
#### Historic number of deaths notified to the Care Quality Commission involving care home residents and home care (domiciliary care) service users by place of occurrence

#### Sheet: Table 10

Value

Category
-B4:C4 dimension 'Category' taken as 'Care home resident' and 'Home care service user'.

Period

Area
-Hard coded Area to England
-Converted all area labels to 9 digit ONS codes.

Date of notification
-A5:A1270 Period dimension taken as date types from column A.
-Format to single day URI pattern.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Value, Category, Period, Area, Date of notification, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 2 Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Quality Commission

-----
#### Number of deaths of care home residents by region and date of death

#### Sheet: Table 11

Cause of death
-B4:M4 "Cause of death" taken as either "All deaths" or "Deaths involving COVID-19".

Period
-A6:A173 Period dimension taken as date types from column A.

Area
-B5:V5 Area dimension is left to right starting from East
-Converted all area labels to 9 digit ONS codes.

Date of notification
-Format to single day URI pattern.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Cause of death, Period, Area, Date of notification, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 4 Based on the date a death occurred rather than when a death was registered.
- 3 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 2 Based on boundaries as of May 2020
- 1 Does not include deaths of those resident outside England and Wales or those records where the place of residence is either missing or not yet fully coded. For this reason counts for "Deaths by Region of usual residence" may not sum to "Total England and Wales" figures.

-----
#### Proportion of deaths of care home residents involving COVID-19 by main pre-existing condition

#### Sheet: Table 18

Sex
-B4:M4 dimension "Sex" taken from horizontal as "All persons", "Males", "Females"

Age Group
-B4:T5 dimension "Age Group" taken from horizontal, plus the "All persons" entry from column B (as otherwise it would be blank).

Pre-existing Condition
-A6:A20 dimension 'Pre-existing condition' taken  from column A

Period

Area
-Hard coding area to 'England and Wales'
-Converted all area labels to 9 digit ONS codes.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Sex, Age Group, Pre-existing Condition, Period, Area, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 4 Based on boundaries as of May 2020
- 3 Based on the date a death occurred rather than when a death was registered.
- 2 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 1 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 

-----
#### Number of deaths, age standardised and age specific mortality rates, by sex

#### Sheet: Table 3

Sex
-B5:N5 Get dimension 'Sex', with values 'Persons', 'Male', 'Females'.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Age
-A8:A58 Dimension 'Age' is from column A
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Rate
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Lower 95% CI
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Lower 95% CI
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Area
-B4:B4 Area is either 'England' or 'Wales'.
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Category
-A2:A47 Get dimension 'category' as things starting 'Number of deaths..' from column A.
-Shortened categories to remove repeated (and super long) date info. Took everything to the left of the first comma
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Period
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'


#### Table structure
Sex, Age, Rate, Lower 95% CI, Lower 95% CI, Area, Category, Period, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 5 The lower and upper 95% confidence limits form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the figure. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
- 4 Rates for 'all ages' are age-standardised and for age groups are age-specific mortality rates, expressed per 100,000 population.
- 3 Based on the date a death occurred rather than when a death was registered.
- 2 COVID-19 defined as ICD-10 codes U07.1 and U07.2
- 1 Based on boundaries as of May 2020.

#### Sheet: Table 4 

Sex
-B5:N5 Get dimension 'Sex', with values 'Persons', 'Male', 'Females'.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Age
-A8:A58 Dimension 'Age' is from column A
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Rate
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Lower 95% CI
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Lower 95% CI
-Flatten the observations, pulling thesevalues into their own appropriate attribute column
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Area
-B4:B4 Area is either 'England' or 'Wales'.
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Category
-A2:A47 Get dimension 'category' as things starting 'Number of deaths..' from column A.
-Shortened categories to remove repeated (and super long) date info. Took everything to the left of the first comma
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Period
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths, age standardised and age specific mortality rates, by sex'
-Added to dataframe 'Number of deaths, age standardised and age specific mortality rates, by sex'


#### Table structure
Sex, Age, Rate, Lower 95% CI, Lower 95% CI, Area, Category, Period, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 5 The lower and upper 95% confidence limits form a confidence interval, which is a measure of the statistical precision of an estimate and shows the range of uncertainty around the figure. As a general rule, if the confidence interval around one figure overlaps with the interval around another, we cannot say with certainty that there is more than a chance difference between the two figures.
- 4 Rates for 'all ages' are age-standardised and for age groups are age-specific mortality rates, expressed per 100,000 population.
- 3 Based on the date a death occurred rather than when a death was registered.
- 2 COVID-19 defined as ICD-10 codes U07.1 and U07.2
- 1 Based on boundaries as of May 2020.

#### Sheet: Number of deaths, age standardised and age specific mortality rates, by sex

Sex

Age

Rate

Lower 95% CI

Area

Category

Period

Unit Multiplier

Measure Type

Unit of Measure


#### Table structure
Sex, Age, Rate, Lower 95% CI, Area, Category, Period, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes

-----
#### Number of deaths of care home residents by date of death (ONS) and date of notification (CQC and CIW)

#### Sheet: Table 1 

Marker
-Converting data markers with the lookup: {":": "no-data-availible"}

Date of notification
-A6:A180 Got 'Date of notification' as datatime types in column A
-Format to single day URI pattern.

Period

Cause of death
-B5:T5 Selected category items as 'Deaths involving COVID-19, 'All deaths'2019 Comparison

Source
-B4:R4 Selected source items as '['England and Wales (ONS data)', 'England (ONS data)', 'England (CQC data)', 'Wales (ONS data)', 'Wales (CIW data)']'. Please note - we'll be splitting these into an area  dimension and a seperate 'Source' attribute in post.
-Split the cells extracted as 'Source' into seperate Source and Area columns

Area
-Split the cells extracted as 'Source' into seperate Source and Area columns
-Converted all area labels to 9 digit ONS codes.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Marker, Date of notification, Period, Cause of death, Source, Area, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 8 ":" denotes data unavailable. 2019 was not a leap year and therefore no data is available for this date.
- 7 Figures relating to deaths involving COVID-19 for the Care Inspectorate Wales (CIW) are from 17 March 2020 when CIW was first notified of a death involving COVID-19.
- 6 Figures relating to deaths involving COVID-19 for the Care Quality Commission (CQC) are from 10 April 2020 when CQC introduced a new method to understand whether COVID-19 was involved in the death.
- 5 Figures for the Care Quality Commission (CQC) and the Care Inspectorate Wales (CIW) are based on the date notified of the death by the care home operator, up to 19 June 2020.
- 4 Figures for ONS are based on the date a death occurred rather than when a death was registered. Date of death is available from 28 December 2020 to 12 June 2020, registered up to 20 June 2020.
- 3 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 2 ONS data is based on boundaries as of May 2020
- 1 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 

-----
#### Number of weekly deaths of care home residents by local authority

#### Sheet: Table 12

Period
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Area
-A6:A339 Area code taken as the continusous sequence of codes from column A.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Week Number
-C4:Q4 Week number taken as left-to-right integers across the top.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Cause of death
-Based on tab name, value set to All deaths.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Date of death
-B5:Q5 Period taken as continuous honizontal sequence of dates across  the top.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'


#### Table structure
Period, Area, Week Number, Cause of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 5 City of London is a separate local authority, however due to their low death count, they have been combined with Hackney.
- 4 Isles of Scilly are separately administered by an Isles of Scilly council and do not form part of Cornwall, however due to their low death count, they have been combined with Cornwall.
- 3 Based on the date a death occurred rather than when a death was registered.
- 2 Based on boundaries as of May 2020
- 1 Does not include deaths of those resident outside England and Wales or those records where the place of residence is either missing or not yet fully coded. For this reason counts for "Deaths by Region of usual residence" may not sum to "Total England and Wales" figures.

#### Sheet: Table 13

Period
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Area
-A6:A339 Area code taken as the continusous sequence of codes from column A.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Week Number
-C4:Q4 Week number taken as left-to-right integers across the top.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Cause of death
-Based on tab name, value set to All deaths.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Date of death
-B5:Q5 Period taken as continuous honizontal sequence of dates across  the top.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'
-Added to dataframe 'Number of weekly deaths of care home residents by local authority'


#### Table structure
Period, Area, Week Number, Cause of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 6 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 5 City of London is a separate local authority, however due to their low death count, they have been combined with Hackney.
- 4 Isles of Scilly are separately administered by an Isles of Scilly council and do not form part of Cornwall, however due to their low death count, they have been combined with Cornwall.
- 3 Based on the date a death occurred rather than when a death was registered.
- 2 Based on boundaries as of May 2020
- 1 Does not include deaths of those resident outside England and Wales or those records where the place of residence is either missing or not yet fully coded. For this reason counts for "Deaths by Region of usual residence" may not sum to "Total England and Wales" figures.

#### Sheet: Number of weekly deaths of care home residents by local authority

Period

Area

Week Number

Cause of death

Date of death

Unit Multiplier

Measure Type

Unit of Measure


#### Table structure
Period, Area, Week Number, Cause of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes

#### Sheet: Table 14

Period

Area
-A6:A155 Area is taken from column A, below 'England' minus footnotes.

Week Ending
-B5:L5 'Week' dimension taken as continuous sequence of dates across the top
-Formatted to single day period URI

Week Number
-A4:L4 Week number taken as left-to-right integers across the top.

Cause of death
-Based on tab name, value set to All deaths.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Period, Area, Week Ending, Week Number, Cause of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 3 City of London has been removed to suppress low numbers. 
- 2 Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Quality Commission

#### DE notes
Cant codify geography for this. Needs investigating but they seem to be inventing geographies by ramming some places together randomly. eg 'Bournemouth, Christchurch and Poole'.

#### Sheet: Table 15

Period

Area
-A6:A155 Area is taken from column A, below 'England' minus footnotes.

Week Ending
-B5:L5 'Week' dimension taken as continuous sequence of dates across the top
-Formatted to single day period URI

Week Number
-A4:L4 Week number taken as left-to-right integers across the top.

Cause of death
-Based on tab name, value set to Deaths involving COVID-19.

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Period, Area, Week Ending, Week Number, Cause of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 3 City of London has been removed to suppress low numbers. 
- 2 Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Quality Commission

#### DE notes
Cant codify geography for this. Needs investigating but they seem to be inventing geographies by ramming some places together randomly. eg 'Bournemouth, Christchurch and Poole'.

-----
#### Number of notifications of weekly deaths of adult care home residents from all causes of death and COVID-19 (both confirmed and suspected) notified to the Care Inspectorate Wales by local authority

#### Sheet: Table 16

Period

Area
-A7:A29 Area code taken as the continuous sequence of codes from column A.

Week Ending
-C5:AG5 week_ending taken as continuous horizontal sequence of dates across  the top.
-Formatted to single day period URI

Week Number
-C4:AG4 Week number taken as horizontal sequence of integers across the top.

Cause of death
-C6:AH6 dimension "Cause of death" taken as "All deaths", "COVID-19"

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Period, Area, Week Ending, Week Number, Cause of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 2 Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Inspectorate Wales

-----
#### Number of deaths notified to the Care Quality Commission involving COVID-19 in home care (domiciliary care) service users by place of occurrence

#### Sheet: Table 9

Period

Place Of Death
-B5:J5 the dimension "Place of death" taken as "Care Home", "Hospital", "Elsewhere","Not Stated"

Date of notification
-A6:A77 Period dimension taken as date types from column A plus 'Total'.
-Format to single day URI pattern.

Area
-Hard coded Area to England
-Converted all area labels to 9 digit ONS codes.

Cause Of Death
-B4:G4 the dimension "Cause of death" taken as "All deaths", "COVID-19"

Unit Multiplier
-Set unit multiplier to 1.

Measure Type
-Set Measure Type to Count.

Unit of Measure
-Set Unit of Measure to People.


#### Table structure
Period, Place Of Death, Date of notification, Area, Cause Of Death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 2 Figures are for deaths CQC are notified of on the days specified. Figures only include deaths that were notified by 5pm on 19 June 2020, and may be an underestimate due to notification delays.
- 1 Data provided by Care Quality Commission

-----
#### Number of deaths of care home residents by place of death

#### Sheet: Table 5

Period
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Area
-B4:J4 Area dimension taken as "England and Wales", "England", "Wales"
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Place of death
-B5:L5 the dimension "Place of death" taken as "Care Home", "Hospital","Elsewhere"
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Date of death
-A6:A109 'Date of death' dimension taken as date types from column A plus 'Total'.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'


#### Table structure
Period, Area, Place of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 5 The "Elsewhere" category in this table includes deaths in private homes, hospices, other communal establishments, and all other places.
- 4 Based on the date a death occurred rather than when a death was registered.
- 3 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 2 Based on boundaries as of May 2020
- 1 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 

#### Sheet: Table 6

Period
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Area
-B4:J4 Area dimension taken as "England and Wales", "England", "Wales"
-Converted all area labels to 9 digit ONS codes.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Place of death
-B5:L5 the dimension "Place of death" taken as "Care Home", "Hospital","Elsewhere"
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Date of death
-A6:A109 'Date of death' dimension taken as date types from column A plus 'Total'.
-Format to single day URI pattern.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Unit Multiplier
-Set unit multiplier to 1.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Measure Type
-Set Measure Type to Count.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'

Unit of Measure
-Set Unit of Measure to People.
-ALL: Stored under the identifier 'Number of deaths of care home residents by place of death'
-Added to dataframe 'Number of deaths of care home residents by place of death'


#### Table structure
Period, Area, Place of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes
- 5 The "Elsewhere" category in this table includes deaths in private homes, hospices, other communal establishments, and all other places.
- 4 Based on the date a death occurred rather than when a death was registered.
- 3 COVID-19 defined as ICD10 codes U07.1 and U07.2
- 2 Based on boundaries as of May 2020
- 1 England and Wales totals may include deaths of some people who are not permanent residents of the relevant area. 

#### Sheet: Number of deaths of care home residents by place of death

Period

Area

Place of death

Date of death

Unit Multiplier

Measure Type

Unit of Measure


#### Table structure
Period, Area, Place of death, Date of death, Unit Multiplier, Measure Type, Unit of Measure

#### Footnotes

-----
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

