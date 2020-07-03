<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## ONS Coronavirus and the social impacts on those with a disability in Great Britain 

[Landing Page](https://www.ons.gov.uk/releases/coronavirusandthesocialimpactsonthosewithadisabilityingreatbritain)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Coronavirus-and-the-social-impacts-on-those-with-a-disability-in-Great-Britain/flowchart.ttl)

----------### Stage 1. Transform

#### Sheet: 1

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, J, P, - Lower CI - (LCL column's down) - (Attribute)
    E, K, Q - Upper CI - (UCL column's down) - (Attribute)
    F, L, R- Weighted Count - (Weighted count column's down) - (Attribute)
    G, M, S - Sample - (Sample column's down) - (Attribute)
	C, I, O - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 2

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold -  (Codelist) 
    B4:J4 - Disabled Status (Codelist)
    C, G, K - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI  - (UCL column's down) - (Attribute)
    B14:J14, B37:J37  - Weighted Count - (Weighted count column's across) - (Attribute)
    B15:J15, B38:J38 - Sample - (Sample column's across) - (Attribute)
	B, F, J - obervations  - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

				Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
            
#### Sheet: 3

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold -  (Codelist
    B4:J4 - Disabled Status (Codelist)
    C, G, K - Lower CI - (LCL column's down) - (Attribute)
    D, H, J - Upper CI  - (UCL column's down) - (Attribute)
    B21:J21 - Weighted Count - (Weighted count column across) - (Attribute)
    B22:J22 - Sample - (Sample column across) - (Attribute)
	B, F, J - obervations  - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

				Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 4

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold -  (Codelist
    B4:J4 - Disabled Status (Codelist)
    C, G, K - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI  - (UCL column's down) - (Attribute)
    B13:J13, B32:J32  - Weighted Count - (Weighted count column's across) - (Attribute)
    B14:J14, B33:J33 - Sample - (Sample column's across) - (Attribute)
	B, F, J - obervations  - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

				Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
                
#### Sheet: 5

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold (Codelist)
    C4:O4 - Disabled Status (Codelist)
    D, J, P  - Lower CI - (LCL column's down) - (Attribute)
    E, K, Q - Upper CI - (UCL column's down) - (Attribute)
    F, L, R - Weighted Count - (Weighted count column's down) - (Attribute)
    G, M, S - Sample - (Sample column's down) - (Attribute)
	C, I, O - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker  

#### Sheet: 6

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist)  
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B16:K16, B27:K27, B38:K38 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B17:K17, B28:K28, B39:K39 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 7

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B13:K13, B22:K22, B30:K30 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B14:K14, B23:K23, B31:K31 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
        
#### Sheet: 8

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B12:K12, B18:K18, B36:K36 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B13:K13, B19:K19, B37:K37 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
#### Sheet: 9

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B22:K22 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B23:K23 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        

#### Sheet: 10

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B22:K22 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B23:K23 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent
    Marker :  ~ indicates a proportion less than 0.1

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 11

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B12:K12, B20:K20 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B13:K13, B21:K21 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
#### Sheet: 12

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B10:K10, B19:K19, B34:K34, B43:K43 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B10:K10, B20:K20, B35:K35, B44:K44 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
#### Sheet: 13

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B10:K10 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B11:K11 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
 
#### Sheet: 14a

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B11:K11 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B12:K12 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 14b

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B21:K21 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B22:K22 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, G - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 15

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, I, O - Lower CI - (LCL column's down) - (Attribute)
    D, J, P - Upper CI - (UCL column's down) - (Attribute)
    E, K, Q - Weighted Count - (Weighted count column's down) - (Attribute)
    F, L, R - Sample - (Sample column's down) - (Attribute)
	B, H, N - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 16

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B15:K15, B24:K24 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B16:K16, B25:K25 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
#### Sheet: 17

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B15:K15, B26:K26 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B16:K16, B27:K27 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 18

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, G, K  - Lower CI - (LCL column's down) - (Attribute)
    D, H, L - Upper CI - (UCL column's down) - (Attribute)
    B11:K11, B18:K18 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B12:K12, B19:K19 - Sample - (Sample Size row's Across) - (Attribute)
	B, F, J - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker
        
#### Sheet: 19

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    Footnotes - Response - 'Each of these questions is answered on a scale of 0 to 10, where 0 is “not at all” and 10 is “completely” ' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    C, I, O  - Lower CI - (LCL column's down) - (Attribute)
    D, J, P - Upper CI - (UCL column's down) - (Attribute)
    E, K, Q - Weighted Count - (Weighted count row's Across) - (Attribute)
    F, L, R - Sample - (Sample Size row's Across) - (Attribute)
	B, H, N - obervations - (Mean column's down) 
	Add Measure Type column with value Mean
	Add Unit column with value Mean

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 20

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B14:K14, B24:K24 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B15:K15, B25:K25 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker

#### Sheet: 21

	A2: - Date Range - Change name to Period and format as required. 
	A1: - Survey Topic - Remove 'Table 1' to leave the topic of the survey only.  (Codelist)
	A - Question - In bold - (Codelist)
    A - Response - Not in bold and remove 'Weighted Count' and 'Sample Size' -  (Codelist) 
    C4:O4 - Disabled Status (Codelist)
    D, H, L  - Lower CI - (LCL column's down) - (Attribute)
    E, I, M - Upper CI - (UCL column's down) - (Attribute)
    B14:K14 - Weighted Count - (Weighted count row's Across) - (Attribute)
    B15:K15 - Sample - (Sample Size row's Across) - (Attribute)
	C, G, K - obervations - (% column's down) 
	Add Measure Type column with value Percentage
	Add Unit column with value Percent

#### Table Structure

		Period, Survey Topic, Question, Response, Disabled Status, Value, Measure Type, Unit, Lower CI, Upper CI, Weighted Count, Sample , Marker


##### Footnotes 
         Footnotes need to be added to the metadata and the Notes (Marker) column changed as mentioned when required. Note as the date range is the same throughout the dataset the duration could be added to the metadata using temporal coverage.



-------------### Stage 2. Harmonise

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value

#### Sheet: 2

		spec

----------#### Table Structure

		Period, Measure Type, Unit, Marker, Value

--------------##### Footnotes

		footnotes

##### DM Notes

		notes

<!-- #endregion -->

```python

```
