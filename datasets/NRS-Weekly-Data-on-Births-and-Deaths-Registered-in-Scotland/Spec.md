
## Actions to Take
* Alter the `Week Number` - remove the preceding `W` so we're left with just a number between 1 and 53.
* Remove all values for Week 53 where the cell value is `-`. These years do not have a 53rd week.
* The `Area` should be mapped to the ONS geography code for Scotland `http://statistics.data.gov.uk/id/statistical-geography/S01011834`.
    * This should be taken care of by my changes to the `info.json` file.
* Rename the `OBS` column to `Value`.

## Issues

* Information is encoded in the XLSX file by *italicising* text. Unfortunately we can't extract this information using databaker as it stands. 




## Leigh notes


	Year column needs to be converted to an integer
	Week and year column need to be combined into format week/{year}-{week} - week/2020-02
	Column needs a name like Period
	Value (OBS) column needs to be converted to integer
	Measure Type and Unit column can be removed as they will be taken care of in the info.json (this will hopefully change soon with the use of the cube class)

	If still can't do multi-measure cubes

	data needs to be split into two: 1 Births, 2 Deaths and dataset_paths (URIs), titles, comments and possibly descriptions need to be set separately 

	Dataset URI is usually:
	dataset_path = pathify(os.environ.get('JOB_NAME', f'gss_data/{scraper.dataset.family}/' + Path(os.getcwd()).name)).lower() + "/" + {EXTRA BIT}

	Check what the currently comments are and alter to reflect what the data represents
	Check what the description currently is and alter if needed

	dict form info.json needs to be changed to reflect which dataset is being output
	Dataset 1
 		Measure Type = births
		Unit = count
	Dataset 2
		Measure Type = deaths
		Unit = count

	Maybe speak to Shannon about the new cube class to see if it is possible to output multi-cube datasets with it. If so then we can keep to one dataset and won't need to change the path.
	
	Don't need any code lists , which makes things nice and simple