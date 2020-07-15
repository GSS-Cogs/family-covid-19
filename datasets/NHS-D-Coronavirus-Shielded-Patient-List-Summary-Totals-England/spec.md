# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## NHS-D Coronavirus Shielded Patient List Summary Totals, England 

[Landing Page](https://digital.nhs.uk/data-and-information/publications/statistical/mi-english-coronavirus-covid-19-shielded-patient-list-summary-totals/latest)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NHS-D-Coronavirus-Shielded-Patient-List-Summary-Totals-England/flowchart.ttl)

----------

### Stage 1. Transform

#### Filename: Coronavirus Shielded Patient List, England - Open Data - LA, Sheet: Coronavirus Shielded Patient Li

#### Coronavirus Shielded Patient List Summary Totals, Local Authority, England

NOTE - There's lots of badly stacked dimensions in this source (so they've basicall stuck Age+Gender+All into the
same column). To fix it we've pulled it apart into three dataframes (think "virtual sheets" or "sub slice"), flattened them, then glued them back together. The notes should make sense if you think in those terms.

Be aware there is a little mashing together of geography codes going on here (eg a code of literally 'E06000052+E06000053') not sure how we handle that.

#### Sheet: sub slice for breakdown field 'ALL'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Value
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'


#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value


#### Sheet: sub slice for breakdown field 'Age'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set 'Age' to the breakdown value.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value

#### Sheet: sub slice for breakdown field 'Gender'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set 'Gender' to the breakdown value.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, Local Authority, England'

#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value


#### Sheet: Coronavirus Shielded Patient List Summary Totals, Local Authority, England

Period
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively
- Format period as single day URI.

Area
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively

Age
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes

Gender
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes

Measure Type
- Set to 'Count'.

Unit of measure
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes

Unit multiplier
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes

Value
- ALL: Remove unwanted columns, get rid of column 'LA Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively

Unit
- Set to 'People'.

#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value, Unit

-------------

#### Filename: Coronavirus Shielded Patient List, England - Open Data - CCG, Sheet: Coronavirus Shielded Patient Li

#### Coronavirus Shielded Patient List Summary Totals, CCG, England

NOTE - There's lots of badly stacked dimensions in this source (so they've basicall stuck Age+Gender+All into the
same column). To fix it we've pulled it apart into three dataframes (think "virtual sheets" or "sub slice"), flattened them, then glued them back together. The notes should make sense if you think in those terms.

I've also no idea about CCG codes so just taken as is (though I suspect "ENG" isn't one).

#### Sheet: sub slice for breakdown field 'ALL'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value


#### Sheet: sub slice for breakdown field 'Age'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set 'Age' to the breakdown value.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'


#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value

#### Sheet: sub slice for breakdown field 'Gender'

Period
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Area
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Age
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set value to all.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England'

Gender
- Pivot the Breakdown Field and Values columns to make Age and Gender dimensions
- Set 'Gender' to the breakdown value.
- ALL: Stored under the identifier 'Coronavirus Shielded Patient List Summary Totals, CCG, England'
- Added to dataframe 'Coronavirus Shielded Patient List Summary Totals, CCG, England's


#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value

#### Sheet: Coronavirus Shielded Patient List Summary Totals, CCG, England

Period
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively
- Format period as single day URI.

Area
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively

Age
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes

Gender
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes

Measure Type
- Set to 'Count'.

Unit of measure
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes

Unit multiplier
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes

Value
- ALL: Remove unwanted columns, get rid of column 'CCG Name' as we have the codes
- Rename LA Code, Extract Date and Patient Count to Area, Period and Value respectively

Unit
- Set to 'People'.


#### Table structure
Period, Area, Age, Gender, Measure Type, Unit of measure, Unit multiplier, Value, Unit

-------------

### Stage 2. Harmonise

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: 2

		spec

----------

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

--------------##### Footnotes

		footnotes

##### DM Notes

		notes

