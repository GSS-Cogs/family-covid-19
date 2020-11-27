# Tables

## Overall Footnotes
* The figures shown for the latest year (or two) will be provisional, pending the publication of the final figures for each calendar year in the following summer (for examplethe final figures for 2007 were published in summer 2008).
* The information presented is based on the date of registration, not the date on which the event occurred. This is consistent with all routine data published by the National Records of Scotland (NRS) for examplein the Registrar General’s Annual Reports (http://www.nrscotland.gov.uk/statistics-and-data/statistics/stats-at-a-glance/registrar-generals-annual-review). Further information on date of registration versus date of occurrence is given on the Monthly data on Births and Deaths (http://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/general-publications/weekly-and-monthly-data-on-births-and-deaths/monthly-data-on-deaths-registered-in-scotland) page of the NRS website.

## Geographical Definitions
Scotland - http://statistics.data.gov.uk/id/statistical-geography/S01011834

### NHS Board Areas
Use S08 - Health Board area geography types.

### Council Areas
Using S12 geography codes for councils.

## Table 1: Births in Scotland by month of registration and NHS Board area, 1990 - 2020

### Footnotes
* The health board areas are based on the boundaries introduced on 1 April 2014.
* During the second half of March 2020 most registration offices closed due to the Covid-19 pandemic and most birth registrations were postponed. 

## Table 2: Births in Scotland by month of registration and council area, 1996 - 2020

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
