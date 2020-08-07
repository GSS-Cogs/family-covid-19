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

### Stage 2. Alignment

	Hardcoded URL used for both sheets where date of data is 1 July 2020. Latest data has date of 23 July 2020 when checked on 5 August 2020. 

#### Coronavirus Shielded patient list, England, Local Authority

		'Disease Group' from column 'Breakdown Field' has been removed. Data needs to be added back in as a column 'Disease Group' with value 'All' in 'Age' and 'Gender' columns and vice versa
		'Gender' column to be renamed 'Sex' and values changed to All = T, Male = M, Female = F
		'Age' column, 70+ to be changed to 70plus
		'Unit' column to be changed to 'Patients'
		'Area' column to be renamed 'Geography Area'
		'Geography Type' column to be added with value 'Local Authority'
		Rename "Period" column as "Extract Date"


#### Coronavirus Shielded patient list, England, CCG

		'Disease Group' from column 'Breakdown Field' has been removed. Data needs to be added back in as a column 'Disease Group' with value 'All' in 'Age' and 'Gender' columns and vice versa
		'Gender' column to be renamed 'Sex' and values changed to All = t, Male = M, Female = F
		'Age' column, 70+ to be changed to 70plus
		'Unit' column to be changed to 'Patients'
		'Area' column to be renamed 'Geography Code and CCG Name column to be mapped to ONS Geography codes instead. The file reference-geography.ttl is in the Reference folder and should hold all the codes for CCGs. 
		See the following example starting at line 1433 of how to query it using SPAQL if needed: https://github.com/GSS-Cogs/family-covid-19/blob/master/datasets/ONS-Deaths-involving-COVID-19-in-the-care-sector-England-and-Wales-deaths-occurring-up-to-1-May-2020-and-registered-up-to-9-May-2020-provisional/main.py
		'Geography Type' column to be added with value 'Clinical Commissioning Group'
		Rename "Period" column as "Extract Date"

#### Join

		Both tables to be joined and output with Title 'Coronavirus Shielded Patient List Summary Totals, England by Clinical Commissioning Group and Local Authority'
		output csv file to be called 'observations'
		Pathify things except for Sex and Geography Code columns

----------

#### Table Structure

		Extract Date, Geography Code, Geography Type, Disease Group, Sex, Age, Measure Type, Unit, Value


##### DM Notes

		info.json file has been updated with mapping information

