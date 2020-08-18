# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------
## ONS Online price changes for high-demand products 

[Landing Page](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts)

[Transform Flowchart](https://gss-cogs.github.io/family-covid-19/datasets/specflowcharts.html?ONS-Online-price-changes-for-high-demand-products/flowchart.ttl)

### Stage 1. Transform

#### Sheet: Online Price Change of HDP

        A4:A20 - Week
        B4:B20 - Period
        C3:AB3 - Products 
        
        Add Measure Type Column with value: Price Indice Change
        Add Unit column with value: Percent

#### Table Structure

		Week, Period, Products, Value, Measure Type, Unit


### Stage 2. Harmonise

#### Sheet: Online Price Change of HDP

		Remove the string 'week' from 'Week' column and convert to Integer. Kept this column as it is important in reference to the first week, which will always be 100.
		Rename 'Products' column to 'Product' (I know, its petty!)

#### Table Structure

		Period, Week, Product, Measure Type, Unit, Value

#### Dataset Output Name

		Online price changes for high-demand products


##### DM Notes

		Second table of week 2 vs week 1 has been removed as per Github comments (derivable)

