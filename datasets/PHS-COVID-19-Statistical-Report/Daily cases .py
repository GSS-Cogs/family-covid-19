# # PHS COVID-19 Statistical Report 

# ## Daily and cumulative positive COVID-19 cases at Scotland level

from gssutils import * 
import json 

scrape = Scraper(seed="info_cumulativecases.json")   
scrape.distributions[0].title = "COVID-19 Statistical Report"
scrape

dist = scrape.distribution(latest=True, mediaType='text/csv')
table = dist.as_pandas(encoding='Windows-1252')

table

table.rename(index=str,
               columns={
                   'Date':'Period'                   
               }, inplace = True)
table.count()

new_table = pd.melt(table, id_vars = ['Period'], var_name = "Case Count Type")


def date_time(time_value):
    time_string = str(time_value).replace(".0", "").strip()
    time_len = len(time_string)
    if time_len == 8:       
        return 'gregorian-day/' + time_string[:4] + '-' + time_string[4:6]+'-'+ time_string[6:8] + 'T00:00:00'
new_table["Period"] = new_table["Period"].apply(date_time)

new_table['Measure Type'] = 'Cases'
new_table['Unit'] = 'Count'

list(new_table)

tidy = new_table[['Period', 'Case Count Type', 'value', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'phs COVID-19 Statistical Report.csv', index = False)

new_table
