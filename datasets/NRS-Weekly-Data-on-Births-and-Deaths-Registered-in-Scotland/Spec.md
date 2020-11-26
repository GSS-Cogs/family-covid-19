
## Actions to Take
* Alter the `Week Number` - remove the preceding `W` so we're left with just a number between 1 and 53.
* Remove all values for Week 53 where the cell value is `-`. These years do not have a 53rd week.
* The `Area` should be mapped to the ONS geography code for Scotland `http://statistics.data.gov.uk/id/statistical-geography/S01011834`.
    * This should be taken care of by my changes to the `info.json` file.
* Rename the `OBS` column to `Value`.

## Issues

* Information is encoded in the XLSX file by *italicising* text. Unfortunately we can't extract this information using databaker as it stands. 