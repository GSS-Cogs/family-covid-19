# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## WG NHS activity and capacity during the coronavirus COVID-19 pandemic 

### Welsh Government

[Landing Page](https://gov.wales/nhs-activity-and-capacity-during-coronavirus-covid-19-pandemic)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?WG-NHS-activity-and-capacity-during-the-coronavirus-COVID-19-pandemic/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		WG NHS activity and capacity during the coronavirus COVID-19 pandemic

#### Table Structure

		Period, Local Health Board, Case Count Type, Measure Type, Unit, Marker, Value

#### Filename: nhs-activity-and-capacity-during-the-coronavirus-covid-19-pandemic-14-may-2020.ods

#### Sheet: Cases_by_LHB

		A8:A18 - Local Health Board (Codelist) - Should change to ONS Geography code but it has the extra categories
		B6:CU6 - Date - change to Period and format as required
		B7:CU7 - Case Count Type
			New Cases
			Cumulative Cases
		Add Measure Type column with value Cases
		Add Unit column with value Count
		

#### Sheet: Cases

		A8:A63 - Date - change to Period and format as required
		B7:E7 - Case Count type (Codelist)
			New cases reported
			Cumulative cases reported
			New cases by test date
			Cumulative cases by test date
		Values with ~ choice of either deleting as they hold no information or replace with 0 and add "Not all tests completed"" to Marker column
		Add Local Health Board column with value All
		Add Measure Type column with value Cases
		Add Unit column with value Count

#### Sheet: Deaths

		A11:A68 - Date - change to Period and format as required
		B10:E10 - Case Count type (Codelist)
			Newly reported deaths
			cumulative deaths reported
			Date of Death
			ONS deaths by actual date of death, registered by 9 May - ONS deaths by actual date of death
		Values with ~ choice of either deleting as they hold no information or replace with 0 and add "Not all Deaths Reported" to Marker column
		Values with .. delete as they hold no information that is useful
		Add Local Health Board column with value All
		Add Measure Type column with value Deaths
		Add Unit column with value Count

#### Sheet: Admissions

		A8:A58 - Date - change to Period and format as required
		B8 - Case Count type (Codelist)
			Admissions - Hospital Admissions	
		Add Local Health Board column with value All
		Add Measure Type column with value Patients
		Add Unit column with value Count	


#### Sheet: Hospitalisations

		A8:A56 - Date - change to Period and format as required
		B7:C7 - Case Count type (Codelist)
			All Hospitalisations
			Hospitalisations for COVID-19
		Add Local Health Board column with value All
		Add Measure Type column with value Hospitalisations
		Add Unit column with value Count

#### Sheet: Critical_Care_Beds

		A10:A60 - Date - change to Period and format as required
		B9:D9 - Case Count type (Codelist)
			COVID-19 Patients - Critical Care Beds COVID-19 Patients Occupied
			Non-COVID-19 Patients - Critical Care Beds Non-COVID-19 Patients Occupied
			Spare - Critical Spare Beds Vacant
		Add Local Health Board column with value All
		Add Measure Type column with value Beds
		Add Unit column with value Count

#### Sheet: General_and_Acute_Beds

		A10:A60 - Date - change to Period and format as required
		B9:D9 - Case Count type (Codelist)
			COVID-19 Patients - General and Acute Beds COVID-19 Patients Occupied
			Non-COVID-19 Patients - General and Acute Beds Non-COVID-19 Patients Occupied
			Spare - General and Acute Beds Vacant
		Add Local Health Board column with value All
		Add Measure Type column with value Beds
		Add Unit column with value Count

#### Sheet: Ambulance_Calls

		A9:A79 - Date - change to Period and format as required
		B8 - Case Count type (Codelist)
			Emergency Ambulance Calls - Ambulances Attendance
		Add Local Health Board column with value All
		Add Measure Type column with value Incidents
		Add Unit column with value Count

#### Sheet: 111_Calls

		A11:A83 - Date - change to Period and format as required
		B8 - Case Count type (Codelist)
			111 or NHS Direct Answered or Abandoned Calls
		Add Local Health Board column with value All
		Add Measure Type column with value Calls
		Add Unit column with value Count

#### Sheet: A&E_Attendances

		IGNORE AS DATA IS IN NEXT FILE

#### Filename: a&e-attendances-during-the-coronavirus-covid-19-pandemic-11-may-2020.ods

#### Sheet: A&E_Attendances

	A9:A109 - Date - change to Period and format as required
	B8:BI - Local Health Board (Codelist)
			Total attendances - Total
	B8 - Case Count type (Codelist)
		A&E
	Add Measure Type column with value Attendances
	Add Unit column with value Count

##### Footnotes

		Sheet Deaths: Add info on rows 2, 3, 4 and footnotes about figures on rows 73 and 74
		Sheet Admissions: Hospital Admission figures include field hospitals from 21 April 2020 and community hospitals from 23 April 2020
		Sheet Hospitalisations: Hospitalisation for COVID-19 includes both suspected and confirmed COVID-19 cases
		Sheet Critical_Care_Beds: Spare Bed figures exclude closed beds
		Sheet 111_Calls: Add information on rows 2, 3, 4 and 5

		Sheet Ambulance_Calls: States that this week incidents in England have been excluded, will have to see what it says when actually transformed

		Sheet A&E_Attendances: Add info in row 2

##### DM Notes

		Each sheet could realistically be its own dataset as they are not really related to each other but I have put them all into one data cube to make things easier, I'm sure WG know how to use a filter, if they will transform ok is another matter!

		Cannot use the Geography codes because of the extra categories:
	
		Aneurin Bevan University = W11000028
		Betsi Cadwaladr University = W11000023
		Cardiff and Vale University = W11000029
		Cwm Taf Morgannwg University = W11000030
		Hywel Dda University = W11000025
		Powys Teaching = W11000024
		Swansea Bay University = W11000031
		**To be confirmed = ?
		Resident outside Wales = ?
		Total = ?**

