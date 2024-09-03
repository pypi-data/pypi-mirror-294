# Sitemap Parser

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Satyam Singh 2024

## Examples of How To Use (Alpha Version)

Initialise SitemapScraper

```python
from sitemap_scraper import BaseSitemapScraper

scraper = BaseSitemapScraper(
    restaurant_name="Wendy's", # the name of the restaurant (this will be changed to scrape any sites, not just restaurants)
    source_path="https://locations.wendys.com/sitemap.xml", # path to the sitemap URL
    result_path="Sitemaps/wendys.csv", # path where the output CSV will be saved
    url_component_length=7, # Check for only saving the URL with at least the given number of datapoints
    datapoints={
    "base_url": 2,
    "country": 3,
    "state": 4,
    "city": 5,
    "location": 6,
    }, # mapping of which data resides at which index in the URL (index are calulated by splitting URL on '/')
    substring_check="https://locations.wendys.com", # Check for asserting a specific substring that must be present in the URL
)
```
