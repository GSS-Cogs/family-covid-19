<!-- #region -->
# COGS Dataset Specification

[Family Home](https://gss-cogs.github.io/family-covid-19/datasets/specmenu.html)

[Family Transform Status](https://gss-cogs.github.io/family-covid-19/datasets/index.html)

----------## ONS Online price changes for high-demand products 

[Landing Page](https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/onlinepricechangesforhighdemandproducts)

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

#### Sheet: 1

		spec

#### Table Structure

		Period, Measure Type, Unit, Marker, Value


##### DM Notes

		notes

<!-- #endregion -->

```python

```

```python

```
