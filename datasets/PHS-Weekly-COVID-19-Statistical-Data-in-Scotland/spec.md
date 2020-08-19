# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19-AIRTABLE/datasets/index.html)


----------### Stage 1. Transform

#### Daily ICU Admissions for new COVID-19 Patients

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily ICU Admissions for new COVID-19 Patients - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Move NumberAdmitted and SevenDayAverage admissions to Value column, differentiate them via Measure Type as: ['SevenDayAverage', 'Count']

Unit of Measure
- Admissions

#### Table structure
Period, Value, Measure Type, Unit of Measure


-----
#### Cumulative Cases By Age and Sex

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases By Age and Sex - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Move Rate and Total cases to Value column, differentiate them via Measure Type as: ['Rate', 'Count']

Unit of Measure
- Set to Cases

SexQF
- Applied pathified qualifiers lookup (i.e data markers).

AgeGroupQF
- Applied pathified qualifiers lookup (i.e data markers).

RateQF
- Applied pathified qualifiers lookup (i.e data markers).

Marker
- Renamed RateQF to Marker

#### Table structure
Period, Value, Measure Type, Unit of Measure, SexQF, AgeGroupQF, RateQF, Marker


-----
#### Cumulative COVID-19 Hospital Admissions By Deprivation

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Deprivation - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Cases

#### Table structure
Period, Value, Measure Type, Unit of Measure


-----
#### Daily Consultations by Contact Type

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily Consultations by Contact Type - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Consulations

ContactTypeQF
- Applied pathified qualifiers lookup (i.e data markers).

NumberOfConsultations
- Renamed to Value

#### Table structure
Period, Value, Measure Type, Unit of Measure, ContactTypeQF, NumberOfConsultations


-----
#### Cumulative Suspected COVID-19 SAS Incidents By Age

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Age - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Move Incidents and Rate to Value column, differentiate them via Measure Type as: ['Rate', 'Count']

Unit of Measure
- Incidents

RateQF
- Applied pathified qualifiers lookup (i.e data markers).

Marker
- Renamed RateQF to Marker, as it not only applies to Rate observations (i.e contents of Value)

#### Table structure
Period, Value, Measure Type, Unit of Measure, RateQF, Marker


-----
#### Daily NHS24 COVID-19 Calls

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily NHS24 COVID-19 Calls - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Phone Calls

NHS24CovidCalls
- Renamed to Value

#### Table structure
Period, Value, Measure Type, Unit of Measure, NHS24CovidCalls


-----
#### Cumulative Suspected COVID-19 SAS Incidents By Deprivation

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative Suspected COVID-19 SAS Incidents By Deprivation - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date
- ALL: Renamed Incidents column to Value

Value
- ALL: Renamed Incidents column to Value

Measure Type
- Set to Count
- ALL: Renamed Incidents column to Value

Unit of Measure
- Set to Incidents
- ALL: Renamed Incidents column to Value

#### Table structure
Period, Value, Measure Type, Unit of Measure


-----
#### Daily COVID-19 Hospital Admissions

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily COVID-19 Hospital Admissions - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Move NumberAdmitted and SevenDayAverage cases to Value column, differentiate them via Measure Type as: ['SevenDayAverage', 'Count']

Unit of Measure
- Set to Admissions

SevenDayAverageQF
- Applied pathified qualifiers lookup (i.e data markers).

#### Table structure
Period, Value, Measure Type, Unit of Measure, SevenDayAverageQF


-----
#### Daily SAS Incidents

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily SAS Incidents - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Incidents

Incident Type
- Created an 'Incident Type' column and pivotted the following column into it: '['AllSASIncidents', 'COVIDAll', 'COVIDAttended', 'COVIDConveyed']'.

#### Table structure
Period, Value, Measure Type, Unit of Measure, Incident Type


-----
#### Cumulative Admissions to ICU

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative Admissions to ICU - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Move NumberAdmitted and Rate Admitted admissions to Value column, differentiate them via Measure Type as: ['Rate', 'Count']

Unit of Measure
- Admissions

AgeGroupQF
- Applied pathified qualifiers lookup (i.e data markers).

SexQF
- Applied pathified qualifiers lookup (i.e data markers).

#### Table structure
Period, Value, Measure Type, Unit of Measure, AgeGroupQF, SexQF


-----
#### Daily and Cumulative Cases

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Daily and Cumulative Cases - Scottish Health and Social Care Open Data

Period
- Converted Period to /day format.

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Cases

Case Type
- Added a 'Case Type' dimension so we can differentiate between a daily count ofcases and a cumulative count of cases

#### Table structure
Period, Value, Measure Type, Unit of Measure, Case Type


-----
#### Cumulative COVID-19 Hospital Admissions By Age, Sex

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative COVID-19 Hospital Admissions By Age, Sex - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Move NumberAdmitted and Rate cases to Value column, differentiate them via Measure Type as: ['SevenDayAverage', 'Rate']

Unit of Measure
- Cases

SexQF
- Applied pathified qualifiers lookup (i.e data markers).

AgeGroupQF
- Applied pathified qualifiers lookup (i.e data markers).

RateQF
- Applied pathified qualifiers lookup (i.e data markers).

Marker
- Renamed RateQF to Marker, as it not only applies to Rate observations (i.e contents of Value)

#### Table structure
Period, Value, Measure Type, Unit of Measure, SexQF, AgeGroupQF, RateQF, Marker


-----
#### Cumulative Cases by Deprivation

#### Sheet: Weekly COVID-19 Statistical Data in Scotland - Cumulative Cases by Deprivation - Scottish Health and Social Care Open Data

Period
- No date provided against observations. Set as the issued date

Value

Measure Type
- Set to Count

Unit of Measure
- Set to Cases

#### Table structure
Period, Value, Measure Type, Unit of Measure


-----