# Tables

## Cause of Death Notes
Seems to be based on ICD-10 code: https://www.cdc.gov/nchs/data/dvs/im9_2002.pdf.pdf

https://www.cdc.gov/nchs/icd/icd10.htm

https://www.nrscotland.gov.uk/files/statistics/vital-events/ve-deaths-underlying-cause-codes.pdf

https://www.nrscotland.gov.uk/files/statistics/vital-events/coding-causes-of-death.pdf

https://icd.who.int/browse10/2019/en#/C00-C97

Cause of Death is mapped to a local code-list called `cause-of-death` which links to the [ICD10 Ontology](http://purl.bioontology.org/ontology/ICD10) where appropriate using `owl:sameAs`.
 
## Overall Footnotes
* The figures shown for the latest year (or two) will be provisional, pending the publication of the final figures for each calendar year in the following summer (for examplethe final figures for 2007 were published in summer 2008).
* The information presented is based on the date of registration, not the date on which the event occurred. This is consistent with all routine data published by the National Records of Scotland (NRS) for examplein the Registrar General’s Annual Reports (http://www.nrscotland.gov.uk/statistics-and-data/statistics/stats-at-a-glance/registrar-generals-annual-review). Further information on date of registration versus date of occurrence is given on the Monthly data on Births and Deaths (http://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/general-publications/weekly-and-monthly-data-on-births-and-deaths/monthly-data-on-deaths-registered-in-scotland) page of the NRS website.
* From the information held on NRS databases it is possible to derive data relating to the actual date of the event. For detailed studies of short time periods we recommend that users consider using such data. For all enquiries on data availability please email NRS Statistics Customer Services (statisticscustomerservices@nrscotland.gov.uk).
* Please note that there may be some minor discrepancies between the figures which are given here and those that are appear in the Quarterly and Preliminary Annual tables, because the tables may have been extracted at different times, and a small number of records may have been added to the statistical database in the intervening period.

## Table 1: Births in Scotland by month of registration and NHS Board area, 1990 - 2020

* Map `Area` column to `S08` geographies for health boards (except where the value is `Scotland`, the value should be `S01011834` then).
* Rename `OBS` column to `Value`.
* Ensure `Value` and `Year` columns are floored to integers.
* Map `Month` column values to the month numbers 01 to 12.

### Footnotes
* The health board areas are based on the boundaries introduced on 1 April 2014.
* During the second half of March 2020 most registration offices closed due to the Covid-19 pandemic and most birth registrations were postponed. 

## Table 2: Births in Scotland by month of registration and council area, 1996 - 2020

* Set `Area` column to `S01011834` (`http://statistics.data.gov.uk/id/statistical-geography/S01011834` - Scotland).
* Rename `OBS` column to `Value`.
* Ensure `Value` and `Year` columns are floored to integers.
* Map `Month` column values to the month numbers 01 to 12.

### Footnotes
* During the second half of March 2020 most registration offices closed due to the Covid-19 pandemic and most birth registrations were postponed. During late June 2020, registration of births restarted. There are a large number of birth registrations still to be processed from the period when registrations were postponed. The number of registrations shown for March to September 2020 does not reflect the actual number of births in those months.

## Table 3: Deaths in Scotland by month of registration and NHS Board area, 1990 - 2020

* Map `Area` column to `S08` geographies for health boards (except where the value is `Scotland`, the value should be `S01011834` then).
* Rename `OBS` column to `Value`.
* Ensure `Value` and `Year` columns are floored to integers.
* Map `Month` column values to the month numbers 01 to 12.
* Add `Cause of Death` column and set to `All Causes`

### Footnotes
* The health board areas are based on the boundaries introduced on 1 April 2014.

## Table 4: Deaths in Scotland by month of registration and council area, 1996 - 2020

* Map `Area` column to `S12` geographies for councils (except where the value is `Scotland`, the value should be `S01011834` then).
* Rename `OBS` column to `Value`.
* Ensure `Value` and `Year` columns are floored to integers.
* Map `Month` column values to the month numbers 01 to 12.
* Add `Cause of Death` column and set to `All Causes`

## Table 5: Deaths in Scotland by month of registration and cause of death1, 2000 - 2020

* Set `Area` column to `S01011834` (`http://statistics.data.gov.uk/id/statistical-geography/S01011834` - Scotland).
* Rename `OBS` column to `Value`.
* Ensure `Value` and `Year` columns are floored to integers.
* Map `Month` column values to the month numbers 01 to 12.

RTB:
* Create or find Cause of Death lookup.

### Footnotes
* The full breakdown of cause of death is not shown because there is not enough time between registration and publication of monthly death figures to quality assure the data to provide reliable figures for more detailed causes of death.  The causes in this table were chosen because they each account for more than 10 per cent of all deaths.

## Joins

* Join tables 1 & 2 together on [`Area`, `Year` and `Month`]. 
* Join tables 3, 4 & 5 together on [`Area`, `Year`, `Month` and `Cause of Death`]. 

## Issues

* Information is encoded in the XLSX file by *italicising* text. Unfortunately we can't extract this information using databaker as it stands