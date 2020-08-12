# +
# Temp scraper here.
# TODO - move it into gss-utils

from gssutils.metadata.dcat import Distribution
from gssutils.metadata.mimetype import CSV
from dateutil.parser import parse
from lxml import html 


# TODO - when we're happy his works, move it into gss-utils!
def opendata_nhs(scraper, tree):

    # TODO - this feels more like a catalogue than a list of distributions, investigate
    
    # Populate the dataset
    details = tree.xpath('//tr/td[@class="dataset-details"]')
    
    dates = tree.xpath('//span[@class="automatic-local-datetime"]/text()')
    date_updated = parse(" ".join([x.replace("\n", "").replace("(BST)", "").strip() for x in dates[0].split(" ")]))
    date_created = parse(" ".join([x.replace("\n", "").replace("(BST)", "").strip() for x in dates[1].split(" ")]))
    
    # Populate distributions
    distro_resources = tree.xpath('//li[@class="resource-item"]')
    for dr in distro_resources:
        
        title = dr.xpath('a[@class="heading"]/text()')
        title = " ".join([x.replace("\n", "").strip() for x in title])
            
        # Need to go to the preview page for full description and title as they've helpfully truncated both...
        preview_url = "https://www.opendata.nhs.scot" + dr.xpath('div/ul[@class="dropdown-menu"]/li/a/@href')[0]
        r = scraper.session.get(preview_url)
        if r.status_code != 200:
            raise Exception("Unable to follow url to get full description, url: '{}', status code '{}'.".format(preview_url, r.status_code))
            
        preview_tree = html.fromstring(r.content)
        print(preview_tree)
        
        #description = dr.xpath('p[@class="description"]/text()')
        #description = " ".join([x.replace("\n", "").strip() for x in description])

        download = dr.xpath('div/ul/li/a[@class="resource-url-analytics"]/@href')[0]
        
        this_distribution = Distribution(scraper)

        this_distribution.issued = date_updated
        this_distribution.downloadURL = download
        this_distribution.mediaType = CSV

        this_distribution.title = title.strip()
        this_distribution.description = description

        scraper.distributions.append(this_distribution)


# -


# ## Helpers

# +
def format_daily_dates(date):
    
    # Confirm the input is what we think it is
    try:
        int(date) # Cast it, make sure it fits as an int
        date = str(date) 
    except Exception as e:
        raise Exception("Aborting, expected the provided date '{}' to be an integer sequence of 8 digits".format(date_string)) from e
        
    # 20200729
    year = date[:4]
    month = date[4:-2]
    day = date[-2:]
    
    # day/{year}-{month}-{day}
    return "day/{}-{}-{}".format(year, month, day)

def handler_cumulative_cases_by_age_and_sex(df):
    """
    Makes appropriate changes for the source dataset titles 'Cumulative Cases By Age and Sex'
    """
    
    # TRACE - QF columns as attributes?
    
    
    
    return df
    

def handler_daily_cumulative_case(df):
    """
    Makes appropriate changes for the source dataset titles 'Daily and Cumulative Cases'
    """
    daily_df = df.drop("CumulativeCases", axis=1)
    daily_df["Cases"] = "Daily"
    daily_df = daily_df.rename(columns={"DailyCases": "Value"})
        
    cumulative_df = df.drop("DailyCases", axis=1)
    cumulative_df["Cases"] = "Cumulative"
    cumulative_df = cumulative_df.rename(columns={"CumulativeCases": "Value"})
        
    df = pd.concat([daily_df, cumulative_df])
    return df
    


# +
from gssutils import *

scrapers.scraper_list = [('https://www.opendata.nhs.scot', opendata_nhs)]
scraper = Scraper(seed="info.json")
scraper
# +

# A certain amount of nonsense to focus the scraper on each distribution in turn
for distro_title in [x.description for x in scraper.distributions]:
    
    # Note: filter by desription as they're reusing the same title more than once for different data ...
    distro = scraper.distribution(description=distro_title)
    
    df = distro.as_pandas()
    
    # Date
    for col in df.columns.values.tolist():
        if col == "Date":
            if distro.title.startswith("Daily"):
                df[col] = df[col].apply(format_daily_dates)
    
    # Define handlers
    handlers = {
        "Daily and Cumulative Cases": handler_daily_cumulative_case,
        "Cumulative Cases By Age and Sex": handler_cumulative_cases_by_age_and_sex
    }
    
    print(distro.description)
    
    if distro.title not in handlers.keys():
        import sys
        sys.exit(1)

    # Handle
    df = handlers[distro.title](df)
    df.to_csv("{}.csv".format(pathify(distro.title)), index=False)

    


# -




