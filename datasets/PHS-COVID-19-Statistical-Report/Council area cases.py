# # PHS COVID-19 Statistical Report 

# ## Cumulative number of positive COVID-19 cases at council area level.

from gssutils import * 
import json 

scrape = Scraper(seed="info_councilareacases.json")   
scrape.distributions[0].title = "COVID-19 Statistical Report"
scrape

dist = scrape.distribution(latest=True, mediaType='text/csv')
table = dist.as_pandas(encoding='Windows-1252')

table

table.rename(index=str,
               columns={
                   'CA':'Geography'                   
               }, inplace = True)
table.count()

new_table = pd.melt(table, id_vars = ['Geography'], var_name = "Case Count Type")

new_table['Measure Type'] = 'Cases'
new_table['Unit'] = 'Count'

list(new_table)

tidy = new_table[['Geography', 'Case Count Type', 'value', 'Measure Type', 'Unit']]

out = Path('out')
out.mkdir(exist_ok=True)
tidy.drop_duplicates().to_csv(out / 'council area COVID-19 Statistical Report.csv', index = False)

new_table


