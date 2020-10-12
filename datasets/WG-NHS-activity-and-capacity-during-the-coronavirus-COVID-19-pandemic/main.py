

from gssutils import * 
import json
import math
import datetime

info = json.load(open('info.json'))
#etl_title = info["Name"] 
#etl_publisher = info["Producer"][0] 
#print("Publisher: " + etl_publisher) 
#print("Title: " + etl_title)

scraper = Scraper(seed = "info.json")
scraper.distributions[0].title = "NHS activity and capacity during the coronavirus (COVID-19) pandemic"
scraper

tabs = scraper.distributions[0].as_pandas()
trace = TransformTrace()
df = pd.DataFrame()
tbls = []


# +
def single_day_format(day_value):
    day_string = str(day_value).replace("''", "")
    day_len = len(day_string)
    if day_len == 10:       
        return "gregorian-day/" + day_string[6:10] + "-" + day_string[3:5] + "-" + day_string[0:2] + "T00:00:00" + "/P1D"
    
    else:
        return "Error: orginal date format was too long/short."
    
def week_period_format(period_value):
    period_string = str(period_value).replace("''", "")
    period_start = period_string[:10]
    period_end = period_string[len(period_string) - 10:]
    
    start_date = datetime.datetime(int(period_start[6:10]), int(period_start[3:5]), int(period_start[0:2]))
    end_date = datetime.datetime(int(period_end[6:10]), int(period_end[3:5]), int(period_end[0:2]))    
    period_diff = (end_date - start_date).days + 1
    
    return "gregorian-day/" + period_start[6:10] + "-" + period_start[3:5] + "-" + period_start[0:2] + "T00:00:00" + "/P" + str(period_diff) + "D"
    


# +
#### Tab 1: Number of New Daily Hospital Admissions Related to COVID-19

tab_title_1 = "Number of New Daily Hospital Admissions Related to COVID-19"
table1_tab = tabs["Table_1"]
table1_all = []

#tab1_columns = ["Date", "Location", "Geography Code", Measure Types", "Unit", "Value"]
#trace.start(tab_title_1, table1_tab, tab1_columns, scraper.distributions[0].downloadURL)

#Loop to build the new table up row-by-row.
for v in range(0, len(table1_tab[0])):
    #Data values start on row 9, so ignore anything before this
    if v < 9:
        continue
    
    #Stop loop when there are no more values in the column. Must be > 9 because there can be blank rows before the data starts.
    elif v >= 9 and table1_tab[0][v] == "":  
        table1_dat_len = v
        break
    
    else:
        tab1_date = single_day_format(table1_tab[0][v])
        table1_row = [tab1_date, "Wales", "W08000001", "Total Daily Hospital Admissions Related to Covid-19", "Count", table1_tab[1][v]]
        table1_all.append(table1_row)

#print(single_day_format(table1_tab[0][100]))
#trace.Date("Selected as all non-blank values from cell ref A10 down.")
#trace.Location("Hardcoded value")
#trace.Geography_Code("Hardcoded value")
#trace.Measure_Types("Hardcoded as reference cell B9 ('Total Admissions') is quite vague.")
#trace.Unit("Hardcoded value")
#trace.value("Selected as all non-blank values from cell ref B10 down.")

table1 = pd.DataFrame(table1_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
#trace.with_preview(table1)
#df = trace.combine_and_trace(tab_title_1, "combined_tab_1")
#trace.output()

#tidy_tab1 = df
#tidy_tab1
table1

# +
#### Tab 2: Number of People in Hospitals

table2_tab = tabs["Table_2"]
table2_all = []

#List of all dimensions relating to the observations. Used in the embedded for loop so that when building each row
#it doesnt skip to the next after just a single measure type.
table2_measure_types = ["Covid-19 Confirmed", "Covid-19 Recovering", "Covid-19 Suspected", "All Covid-19 Patients", "All Hospitalisations"]

for v in range(0, len(table2_tab[0])):
    #Data values start on row 13
    if v < 13:
        continue
        
    elif v >= 13 and table2_tab[0][v] == "":
        table2_dat_len = v
        break
    
    else:
        tab2_date = single_day_format(table2_tab[0][v])
        #Embedded for loop to construct a new row in the final table per observation value.
        for u in range(0, 5):
            table2_row = [tab2_date, "Wales", "W08000001", table2_measure_types[u], "Count", table2_tab[u + 1][v]]
            table2_all.append(table2_row)

table2 = pd.DataFrame(table2_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table2
# +
#### Tab 3: Number of Invasive Ventilated Beds, by use

table3_tab = tabs["Table_3"]
table3_all = []

table3_measure_types = ["Covid-19 Confirmed Occupied Invasive Ventilated Beds", "Covid-19 Recovering Occupied Invasive Ventilated Beds", "Covid-19 Suspected Occupied Invasive Ventilated Beds", "All Covid-19 Patients Occupied Invasive Ventilated Beds", "Non-Covid-19 Patients Occupied Invasive Ventilated Beds", "Vacant Invasive Ventilated Beds"]

for v in range(0, len(table3_tab[0])):
    #Data values start on row 17
    if v < 17:
        continue
        
    elif v >= 17 and table3_tab[0][v] == "":
        table3_dat_len = v
        break
    
    else:
        tab3_date = single_day_format(table3_tab[0][v])
        for u in range(0, 6):
            table3_row = [tab3_date, "Wales", "W08000001", table3_measure_types[u], "Count", table3_tab[u + 1][v]]
            #print(table3_row)
            table3_all.append(table3_row)

table3 = pd.DataFrame(table3_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table3

# +
#### Tab 4: Number of General and Acute Beds, by use

table4_tab = tabs["Table_4"]
table4_all = []

table4_measure_types = ["Covid-19 Confirmed Occupied General and Acute Beds", "Covid-19 Recovering Occupied General and Acute Beds", "Covid-19 Suspected Occupied General and Acute Beds", "All Covid-19 Patients Occupied General and Acute Beds", "Non-Covid-19 Patients Occupied General and Acute Beds", "Vacant General and Acute Beds"]

for v in range(0, len(table4_tab[0])):
    #Data values start on row 15
    if v < 15:
        continue
        
    elif v >= 15 and table4_tab[0][v] == "":
        table4_dat_len = v
        break
    
    else:
        tab4_date = single_day_format(table4_tab[0][v])
        for u in range(0, 6):
            table4_row = [tab4_date, "Wales", "W08000001", table4_measure_types[u], "Count", table4_tab[u + 1][v]]
            table4_all.append(table4_row)

table4 = pd.DataFrame(table4_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table4

# +
#### Tab 5: Number of Emergency Ambulance Calls

table5_tab = tabs["Table_5"]
table5_all = []

for v in range(0, len(table5_tab[0])):
    #Data values start on row 19
    if v < 9:
        continue
        
    elif v >= 9 and table5_tab[0][v] == "":
        table5_dat_len = v
        break
    
    else:
        tab5_date = single_day_format(table5_tab[0][v])
        table5_row = [tab5_date, "Wales", "W08000001", "Emergency Ambulance Calls", "Count", table5_tab[1][v]]
        table5_all.append(table5_row)

table5 = pd.DataFrame(table5_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table5

# +
#### Tab 6: Number of 111 & NHS Direct Calls

table6_tab = tabs["Table_6"]
table6_all = []

for v in range(0, len(table6_tab[0])):
    #Data values start on row 10
    if v < 10:
        continue
        
    elif v >= 10 and table6_tab[0][v] == "":
        table6_dat_len = v
        break
    
    else:
        tab6_date = single_day_format(table6_tab[0][v])
        table6_row = [tab6_date, "Wales", "W08000001", "Answered Calls or Abandoned Calls After 60 Seconds Without Answer to 111 and NHS Direct", "Count", table6_tab[1][v]]
        table6_all.append(table6_row)

table6 = pd.DataFrame(table6_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table6

# +
#### Tab 7: Number of Daily A&E Attendances

table7_tab = tabs["Table_7"]
table7_all = []

for v in range(0, len(table7_tab[0])):
    #Data values start on row 9
    if v < 9:
        continue
        
    elif v >= 9 and table7_tab[0][v] == "":
        table7_dat_len = v
        break
    
    else:
        tab7_date = single_day_format(table7_tab[0][v])
        table7_row = [tab7_date, "Wales", "W08000001", "Total Daily A&E Attendances", "Count", table7_tab[1][v]]
        table7_all.append(table7_row)

table7 = pd.DataFrame(table7_all, columns = ["Date", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table7

# +
#### Tab 8: Weekly Average Percentage of NHS Staff Absences

table8_tab = tabs["Table_8"]
table8_all = []

#Empty string measure type needed becuase in the tab there is a blank column which. separted the 2 halves of the data (due to Covid, self isolating).
table8_measure_types = ["NHS Medical and Dental Staff Absent Due to Covid-19", "NHS Nursing and Midwifery(registered) Absent Due to Covid-19", "Other NHS Staff Groups Absent Due to Covid-19", "Total NHS Workforce Absent Due to Covid-19", "", "NHS Medical and Dental Staff in Self-Isolation", "NHS Nursing and Midwifery(registered) in Self-Isolation", "Other NHS Staff Groups in Self-Isolation", "Total NHS Workforce in Self-Isolation"]

for v in range(0, len(table8_tab[0])):
    #Data values start on row 13
    if v < 13:
        continue
        
    elif v >= 13 and table8_tab[0][v] == "":
        table8_dat_len = v
        break
    
    else:
        if len(str(table8_tab[0][v])) > 12:
            tab8_date = week_period_format(table8_tab[0][v])
        
        else:
            tab8_date = single_day_format(table8_tab[0][v])
            
        for u in range(0, 9):
            #Skip if the current column (u) is the blank one.
            if u == 4:
                continue
            #Raw data taken from tab not the percentage was displayed. E.g. 14.04.2020 = 1.9% but would come out as 0.019
            #So have multiplied all values by 100 so that it matches the unit.
            #Although in the tab, the formatting of each cell stops early in column J (J15) and for the whole row 38.
            table8_row = [tab8_date, "Wales", "W08000001", table8_measure_types[u], "Percentage", (table8_tab[u + 1][v] * 100)]
            table8_all.append(table8_row)

table8 = pd.DataFrame(table8_all, columns = ["Period", "Location", "Geography Code", "Measure Types", "Unit", "Value"])
table8

# +
#Outputs:
    #table1 = Number of New Daily Hospital Admissions Related to COVID-19
    #table2 = Number of People in Hospitals
    #table3 = Number of Invasive Ventilated Beds, by use
    #table4 = Number of General and Acute Beds, by use
    #table5 = Number of Emergency Ambulance Calls
    #table6 = Number of 111 & NHS Direct Calls
    #table7 = Number of Daily A&E Attendances
    #table8 = Weekly Average Percentage of NHS Staff Absences
    
#Notes:
    #Changed .json file to use the landingpage and welshgov scraper instead of the dataURL for an out of date dataset.
    
    #Transform not able to be completed with databaker because of a hidden ('phantom') tab in the file with a name too long - it's a filepath link.
    
    #There are two other hidden tabs in the file which contain non-current data which has not been updated since late spring 2020
    #These have not been transformed.
    
    #Raw data taken from tab 8 not the percentage was displayed. E.g. 14.04.2020 = 1.9% but would come out as 0.019
    #So have multiplied all values by 100 so that it matches the unit.
    #Although in the tab, the formatting of each cell stops early in column J (J15) and for the whole row 38.
    
# -


