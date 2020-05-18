# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Development](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

## WG Summary data about coronavirus  COVID-19  and the response to it 

### Welsh Government

[Landing Page](https://gov.wales/summary-data-about-coronavirus-covid-19-and-response-it)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?wg-summary-data-about-coronavirus-covid-19-and-the-response-to-it/flowchart.ttl)

### Dataset One

#### Output Dataset Name:

		WG COVID-19 Food Parcel Support
		
#### Table Structure

		Period, Food Parcel Status, Measure Type, Unit, Marker, Value

#### Sheet: Food_parcels

		A7:A47 - Date - Change name to Period and format as required
			Time period for Total needs to be added for totals in row 47
		B6:C6 - Food Parcel Status (Codelist)
			Food parcel orders received - Orders Received
			Attempted deliveries - Attempted Deliveries
		Add Measure Type column with value Parcel
		Add Unit column with value Count
		Values with ~ need to be changed to 0 and "This data item is not yet available" put in Marker column

##### Footnotes
		Daily "order received" data are revised if there was a duplicate record or a box is no longer required and so some totals may be slightly lower than previously shown

### Dataset Two

#### Output Dataset Name:

		WG COVID-19 Support Response

#### Table Structure

		Period, Support Type, Finance Type, Measure Type, Unit, Marker, Value

#### Sheet: Discretionary_Assistance_Fund

		A8:A57 - Date - Change name to Period and format as required
			Time period for Total needs to be added for totals in row 58
		B7:C7 - Finance Type (Codelist)
			COVID-19 related Payments - COVID-19 Related
			Normal EAP Payments - Normal EAP
		Add Support Type Column with value Emergency Assistance
		Add Measure Type column with value Payments
		Add Unit column with value Count

		
#### Sheet: Business_Rates_Grants

		A7:A20 - Date - Change name to Period and format as required
		B6:C6 - Finance Type
			Number of business rates grants awarded (cumulative) - Awarded
			Amount awarded in business rates grants (£m) (cumulative) - Awarded
		Add Support Type Column with value Business Rate Grants
		Add Measure Type column with values Cumulative Count and Cumulative GBP Million
		Add Unit column with values Count and GBP 		

		
#### Sheet: DBW_loans

		A7:A15 - Date - Change name to Period and format as required
		B6:C6 - Finance Type (Codelist)
			Number of DBW loans approved (cumulative) - Approved
			Amount approved in DBW loans (£m) (cumulative) - Approved
		Add Support Type Column with value Development Wales Bank Loans
		Add Measure Type column with values Cumulative Count and Cumulative GBP Million
		Add Unit column with values Count and GBP 

		
#### Sheet: ERF

		A7:A12 - Date - Change name to Period and format as required
		B6:G6 - Finance Type (Codelist)
			Micro-business applications (cumulative) - Micro-business
			Micro-business amount applied for (£m) (cumulative) - Micro-business
			SME applications (cumulative) - SME
			SME amount applied for (£m) (cumulative) - SME
			Total applications (cumulative) - Total
			Total amount applied for (£m)(cumulative) - Total 
		Add Support Type Column with value Economic Resilience Fund
		Add Measure Type column with values Cumulative Applications and Cumulative GBP Million
		Add Unit column with values Count and GBP 
		

