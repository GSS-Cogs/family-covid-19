# NRS Weekly Births and Deaths

## Actions to Take

* Split into two seperate datasets, one for `births` and the other for `deaths`.
  * Use the `info.births.json` and `info.deaths.json` files respectively with the new cubes class.
  * `births` and `deaths` would be good graph names to use to distinguish them.
* Remove the `Measure Type` and `Unit` columns.
* Alter the `Week Number` column - remove the preceding `W` so we're left with just an integer between 1 and 53.
* Convert the `Year` column values to integers.
* Remove all values for Week 53 where the cell value is `-`. These years do not have a 53rd week.
* The `Area` should be mapped to the ONS geography code for Scotland `http://statistics.data.gov.uk/id/statistical-geography/S01011834`.
  * This should be taken care of by my changes to the `info.json` file.
* Rename the `OBS` column to `Value`. Map all values in the column to integers.
* Add `Period` column and set the value to be `week/{year}-{week}`, e.g. `week/2020-28`.
  * You can remove the `Week Number` and `Year` columns now.

## Issues

* Information is encoded in the XLSX file by *italicising* text. Unfortunately we can't extract this information using databaker as it stands.
