# # WG Testing data for coronavirus  COVID-19 

from gssutils import * 
import json 

scrape = Scraper(seed="info.json")   # add dataURL to info.json first!
scrape.distributions[0].title = "Testing data for coronavirus (COVID-19)"
scrape
