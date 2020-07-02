# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------

## ONS Key workers reference tables 

[Landing Page](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/keyworkersreferencetables)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Key-workers-reference-tables/flowchart.ttl)

----------

### Stage 1. Transform

#### Sheet: Table 1a: Total key workers in workforce and working age population

                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A8}",
                    "Workforce Breakdown": "N/A",
                    "Measure Type": "Count",
                    "Unit": "Person"

#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value

#### Sheet: Table 1b: Total key workers by occupation groups

                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A7-A14}",
                    "Workforce Breakdown": "{B5-B5}",
                    "Measure Type": "Count",
                    "Unit": "Person"

#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value

-------------### Stage 2. Harmonise

#### Sheet: Table 2a: Key workers and non-key workers by age bands

                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-X4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value

#### Sheet: Table 2b: Key workers by age bands and occupation groups
                    
		    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-X4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 3a: Key workers and non-key workers by ethnicity
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-J4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 3b: Key workers by ethnicity and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-J4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 4a: Key workers and non-key workers by gender
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 4b: Key workers by gender and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 5a: Key workers and non-key workers by country of birth
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 5b: Key workers by country of birth and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 6a: Key workers and non-key workers by disability status
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 6b: Key workers by disability status and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 7a: Key workers and non-key workers at moderate risk by risk type
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-L4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 7b: Key workers at moderate risk by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 8: Key worker and non-key worker by household type
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A5-A9}",
                    "Workforce Breakdown": "Has Dependant Child(s)",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 9a: Key workers and non-key workers with children aged under 4
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 9b: Key workers with children aged under 4 by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 10a: Key workers and non-key workers with children aged under 15
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-H4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 10b: Key workers with children under 15 by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-H4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 11a: Key worker and non-key worker unpaid carers
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 11b: Key worker unpaid carers by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 12a: Key workers and non-key workers working from home
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 12b: Key workers working from home and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-D4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 14a: Key workers and non-key workers travel to work method
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-R4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 14a (2): Key workers and non-key workers summary of travel to work method
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 14b: Key workers travel to work method by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-R4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 14b (2): Key workers summary of travel to work method by occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-F4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 16a: Key workers and non-key workers by highest qualification
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A7}",
                    "Workforce Breakdown": "{B4-N4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 16b: Key workers by highest qualification and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "E92000001",
                    "Workforce Category": "{A6-A13}",
                    "Workforce Breakdown": "{B4-N4}",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 17: Key workers by region and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "{B4-Z4}",
                    "Workforce Category": "{A6-A14}",
                    "Workforce Breakdown": "Key Workers",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 18: Key workers by city region and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "{A6-A20}",
                    "Workforce Category": "{B4-R4}",
                    "Workforce Breakdown": "Key Workers",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value
		
#### Sheet: Table 19: Key workers by local authority and occupation groups
                    
                    "Period": "A2",
                    "ONS Geography Code": "{A6-A383}",
                    "Workforce Category": "{B4-B4}",
                    "Workforce Breakdown": "Key Workers",
                    "Measure Type": "Count",
                    "Unit": "Person"

----------#### Table Structure

		Period, ONS Geography Code, Workforce Category, Measure Type, Unit, Value

--------------##### Footnotes

		All counts are individually rounded to the nearest thousand. Totals may not add exactly due to this rounding.
		The definition of disability used is consistent with the core definition of disability under the Equality Act 2010. A person is considered to be disabled if they self-report a physical or mental health condition or illness lasting or expecting to last 12 months or more which reduces their ability to carry out day-to-day activities.
		Respondents who did not provide disability status have been excluded.

##### DM Notes

		Multiple tabs with simple structures and multiple dimensions. Multiple footnotes in tabs.
		Dataset is on landing page under heading \"Your download option\"

