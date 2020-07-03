<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## NRS Deaths involving coronavirus  COVID-19  in Scotland 

[Landing Page](https://www.nrscotland.gov.uk/covid19stats)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?NRS-Deaths-involving-coronavirus-COVID-19-in-Scotland/flowchart.ttl)

### Stage 1. Transform

#### Sheet: Table 1 - COVID deaths

         'Period' - Extract date C4 to till end 
         'COVID 19 Deaths' - A7 : A9 , 
         'Deaths by Council Area' - B53 : B84 ,
         'Deaths by NHS Board' - B37 : B50,
         'Deaths by age group'- B13: B34,
         'Deaths by location' - B87: B90, 
         'Deaths by Gender' - B11,A21,A28 , 
         'Measure Type' - 'Deaths',
         'Unit'- 'Count', 
         'Value' - Extract C7 till end
		
 
#### Table Structure
        Output CSV - 'NRS COVID deaths.csv'
        
		'Period','COVID 19 Deaths','Deaths by Council Area','Deaths by NHS Board',
        'Deaths by age group','Deaths by location', 'Deaths by Gender', 'Measure Type','Unit','Value'

#### Sheet: Table 2 - All deaths

		'Period' - Extract date C4 to till end 
         'COVID 19 Deaths' - A7 : A10 , 
         'Deaths by Council Area' - B55 : B86 ,
         'Deaths by NHS Board' - B39 : B52,
         'Deaths by age group'- B15: B36,
         'Deaths by location' - B89: B92, 
         'Deaths by Gender' - B13,A23,A30 , 
         'Measure Type' - 'Deaths',
         'Unit'- 'Count', 
         'Value' - Extract C7 till end

#### Table Structure

		Output CSV - 'NRS All Deaths.csv'
        
		'Period','COVID 19 Deaths','Deaths by Council Area','Deaths by NHS Board',
        'Deaths by age group','Deaths by location', 'Deaths by Gender', 'Measure Type','Unit','Value'

#### Sheet: Table 3 - deaths by location

         'Deaths Registered', - B3 & H3 , 
         'Deaths by Council Area' - A8 & A29 : A60 ,
         'Deaths by NHS Board' - A12 : A25,
         'Deaths by location' - B4: L4, 
         'Measure Type' - 'Deaths',
         'Unit'- 'Count', 
         'Value' - Extract B8 till end
		
 
#### Table Structure
        Output CSV - 'NRS Registered Deaths.csv'
        
		'Deaths Registered', 'Deaths by Council Area', 'Deaths by Location', 'Deaths by NHS Board', 'Measure Type', 'Unit', 'Value'
  

-------------

### Stage 2. Harmonise

	Currently have names for Council Area and NHS Board but could be replaced with Geography Codes

#### Sheet: Table 1 - COVID deaths

		'Period' - Date ranges need to be added for 'Year to Date' rows. Needs to reference http://purl.org/linked-data/sdmx/2009/dimension#refPeriod
        	Rename 'COVID 19 Deaths' to 'Deaths Registered'
        	Rename 'Deaths by Gender' to 'Sex. Needs to reference 'http://purl.org/linked-data/sdmx/2009/dimension#sex'. Reformat to F | M | T
        	Rename 'Deaths by Age Group' too 'NRS Age Group'. Needs to reference 'http://purl.org/linked-data/sdmx/2009/dimension#age'

#### Sheet: Table 2 - All Deaths 

	'Period' - Date ranges need to be added for 'Year to Date' rows. Needs to reference http://purl.org/linked-data/sdmx/2009/dimension#refPeriod
        	Change name of column 'COVID 19 Deaths' to 'Deaths Registered'
        	Rename 'Deaths by Gender' to 'Sex. Needs to reference 'http://purl.org/linked-data/sdmx/2009/dimension#sex'. Reformat to F | M | T
        Rename 'Deaths by Age Group' too 'NRS Age Group'. Needs to reference 'http://purl.org/linked-data/sdmx/2009/dimension#age'

#### Sheet: Table 3 - Death by Location 

		Add column 'Period' and populate with relevant date range
		Add column 'NRS Age Group' column with value 'All'
		Add column 'Sex' with value 'T'		

#### Join 

		Tables: Join 3 tables
		Output CSV - 'NRS Registered COVID-19 and All Deaths.csv'

		Period column to reference refPeriod

		Apply codelists
        
			'Deaths Registered', Deaths by Council Area', 'Deaths by NHS Board', 'NRS Age Group','Deaths by location'



##### DM Notes

		Need to decide if referencing Geography codes 


