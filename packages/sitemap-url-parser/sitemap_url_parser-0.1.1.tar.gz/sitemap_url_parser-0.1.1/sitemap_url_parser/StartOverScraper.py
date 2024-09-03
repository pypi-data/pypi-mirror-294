import logging
import requests


import os
import xmltodict
import logging
import requests
import traceback
import csv
import sys
import re

def setup_logging():
    log_file = "sitemap_scraper.log"

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filename=log_file,          # Log file path
        level=logging.DEBUG,        # Log level
        format=log_format,          # Log format
        datefmt='%Y-%m-%d %H:%M:%S' # Date format
    )
    logging.info("Script started running.")


if __name__ == "__main__":
    setup_logging()



class BaseSitemapScraper():
    def __init__(
            self, 
            restaurant_name, 
            source_path, 
            result_path, 
            url_component_length, 
            datapoints,
            substring_check
    ):
        try:
            
            logging.info(f"Scraping started for {restaurant_name}.")
            self.restaurant_name = restaurant_name
            self.source_path = source_path
            self.result_path = result_path
            self.datapoints = datapoints
            self.url_component_length = url_component_length
            self.substring_check = substring_check
            self.basic_headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36"
            }
            os.makedirs("/".join(result_path.split("/")[:-1]) + "/", exist_ok=True)
            
            
        except Exception as e:
            logging.error(f"Error in __init__(): {traceback.format_exc()}")

    def load_source_data(self, url=""):
        try:
            if not url:
                url = self.source_path
            response = requests.get(url, headers=self.basic_headers)
            if int(response.status_code) == 200:
                input_data = xmltodict.parse(response.text)
                return True, input_data
            else:
                return False, response.text
        except Exception as e:
            logging.error(f"Error in load_source_data(): {traceback.format_exc()}")
            return False, ""

    def parse_sitemap_url(self, url):
        try:
            if self.substring_check and self.substring_check not in url:
                return False, None
            
            url_components = url.split("/")
            
            if len(url_components) < self.url_component_length:
                return False, None
            
            row_data = [url_components[index] for index in self.datapoints.values()]
            row_data.append(url)
            
            return True, row_data
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")
            return False, e

    def write_restaurant_row_to_csv(self, row, csv_writer):
        try:
            csv_writer.writerow(row)
            return True
        except Exception as e:
            logging.error(f"Error in write_restaurant_row_to_csv(): {traceback.format_exc()}")
            return False

    def configure_csv_writer(self):
        try:
            self.file = open(self.result_path, mode="w", newline="", encoding="utf-8")
            return csv.writer(self.file)
        except Exception as e:
            logging.error(f"Error in configure_csv_writer(): {traceback.format_exc()}")
            return False

    def write_output_headers(self, csv_writer):
        try:
            csv_header = list(self.datapoints.keys())
            csv_header.append("full_url")
            return self.write_restaurant_row_to_csv(row = csv_header, csv_writer=csv_writer)
        except Exception as e:
            logging.error(f"Error in write_output_headers(): {traceback.format_exc()}")
            return False

    def parse_sitemap_data(self, data, write_to_csv=True):
        try:
            logging.info(f"Parsing started for {len(data['urlset']['url'])} rows.")
            if write_to_csv:
                writer = self.configure_csv_writer()
                self.write_output_headers(csv_writer=writer)
            for row in data["urlset"]["url"]:
                parse_success, row_data = self.parse_sitemap_url(row.get("loc"))
                if not parse_success:
                    if row_data:
                        logging.error(f"Failed to parse URL: {row.get('loc')}")
                    continue
                    
                if write_to_csv:
                    self.write_restaurant_row_to_csv(row = row_data, csv_writer=writer)
            
            if write_to_csv:
                self.file.close()
            return True
        except Exception as e:
            logging.error(f"Error in parse_sitemap_data(): {traceback.format_exc()}")
            return False

    def scrape(self):
        try:
            sitemap_page_load_success, sitemap_page_data = self.load_source_data()
            if not sitemap_page_load_success:
                logging.error("Could not load data from sitemap page.")
                return False
            parsing_success = self.parse_sitemap_data(data = sitemap_page_data)
            if not parsing_success:
                logging.error("Parsing failed.")
            else:
                logging.info(f"Scraping done. Data saved at: {self.result_path}.")

        except Exception as e:
            logging.error(f"Error in scrape(): {traceback.format_exc()}")


class SitemapScraperOptionalDatapoints(BaseSitemapScraper):

    def __init__(self, *args, **kwargs):
        self.optional_datapoints = kwargs.pop("optional_datapoints")
        super().__init__(**kwargs)

    def parse_sitemap_url(self, url):
        try:
            if self.substring_check and self.substring_check not in url:
                return False, None
            
            url_components = url.split("/")
            
            if len(url_components) < self.url_component_length:
                return False, None
            
            row_data = [url_components[index] for index in self.datapoints.values()]
            optional_data = [url_components[index] if len(url_components) > index else "" for index in self.optional_datapoints.values()]
            row_data.extend(optional_data)
            row_data.append(url)
            
            return True, row_data
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")
            return False, e

    def write_output_headers(self, csv_writer):
        try:
            csv_header = list(self.datapoints.keys())
            csv_header.extend(list(self.optional_datapoints.keys()))
            csv_header.append("full_url")
            return self.write_restaurant_row_to_csv(row=csv_header, csv_writer=csv_writer)
        except Exception as e:
            logging.error(f"Error in write_output_headers(): {traceback.format_exc()}")
            return False


class SitemapScraperNestedSitemap(BaseSitemapScraper):
    def load_source_data(self, url=""):
        try:
            response_flag = False
            final_input_data = None
            if not url:
                url = self.source_path
            response = requests.get(url, headers=self.basic_headers)
            if int(response.status_code) == 200:
                logging.info(f"Fetched sitemap list from source: {url}")
                resp_dict = xmltodict.parse(response.text)
                
                if type(resp_dict["sitemapindex"]["sitemap"]) == list and len(resp_dict["sitemapindex"]["sitemap"]) > 1:
                    xml_urls = [sitemap["loc"] for sitemap in resp_dict["sitemapindex"]["sitemap"]]
                else:
                    xml_urls = [resp_dict["sitemapindex"]["sitemap"]["loc"]]
                
                for xml_url in xml_urls:
                    response = requests.get(xml_url, headers=self.basic_headers)
                    if int(response.status_code) == 200:
                        input_data = xmltodict.parse(response.text)
                        if not final_input_data:
                            final_input_data = input_data
                        else:
                            final_input_data["urlset"]["url"].extend(input_data["urlset"]["url"])        
                        response_flag = True
                        logging.info(f"Number of URLs found: {len(input_data['urlset']['url'])}")
                    else:
                        response_flag = response_flag or False
                return response_flag, final_input_data
            else:
                return False, response.text
        except Exception as e:
            logging.error(f"Error in load_source_data(): {traceback.format_exc()}")
            return False, ""


class SitemapScraperBlacklistedKeywords(BaseSitemapScraper):
    def __init__(self, *args, **kwargs):
        self.blacklisted_keywords = kwargs.pop("blacklisted_keywords")
        super().__init__(**kwargs)
    
    def parse_sitemap_url(self, url):
        try:
            if any([x in url for x in self.blacklisted_keywords]):
                return False, None
            return super().parse_sitemap_url(url)
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")


class Taco_bell_SitemapScraper(SitemapScraperOptionalDatapoints, SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Taco Bell", 
                source_path="https://locations.tacobell.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/taco_bell.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "country/state": 3,
                    "city": 4,
                    "location": 5,
                },
                substring_check="https://locations.tacobell.com/",
                optional_datapoints = {
                    "type": 6,
                }

    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
                optional_datapoints = optional_datapoints,
            )
        except Exception as e:
            logging.error(f"Error in Chick_fil_e_SitemapScraper class __init__(): {traceback.format_exc()}")


class Wendys_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Wendy's", 
                source_path="https://locations.wendys.com/sitemap.xml",
                result_path="Sitemaps/New Parser/wendys.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "city": 5,
                    "location": 6,
                },
                substring_check="https://locations.wendys.com",

    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Wendys_SitemapScraper class __init__(): {traceback.format_exc()}")


class Applebees_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Applebee's", 
                source_path="https://restaurants.applebees.com/sitemap.xml",
                result_path="Sitemaps/New Parser/applebees.csv",
                url_component_length=8,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "city": 5,
                    "location": 6,
                    "type": 7,
                },
                substring_check="https://restaurants.applebees.com/en-us",

    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Applebees_SitemapScraper class __init__(): {traceback.format_exc()}")


class OliveGarden_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Olive Garden", 
                source_path="https://www.olivegarden.com/en-locations-sitemap.xml",
                result_path="Sitemaps/New Parser/olive_garden.csv",
                url_component_length=8,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "location": 6,
                    "store_id": 7,
                },
                substring_check="https://www.olivegarden.com/locations/",

    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in OliveGarden_SitemapScraper class __init__(): {traceback.format_exc()}")


class Chipotle_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Chipotle", 
                source_path="https://locations.chipotle.com/sitemap.xml",
                result_path="Sitemaps/New Parser/chipotle.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "location": 5,        
                },
                substring_check="https://locations.chipotle.com/",
    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Chipotle_SitemapScraper class __init__(): {traceback.format_exc()}")


class BuffaloWildwings_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Buffalo Wildwings", 
                source_path="https://www.buffalowildwings.com/locations.xml",
                result_path="Sitemaps/New Parser/buffalo_wildwings.csv",
                url_component_length=9,
                datapoints={
                    "base_url": 2,
                    "country": 4,
                    "state": 5,
                    "city": 6,
                    "location": 7,
                    "id": 8,            
                },
                substring_check="https://www.buffalowildwings.com/locations/",

    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in BuffaloWildwings_SitemapScraper class __init__(): {traceback.format_exc()}")


class Chick_fil_e_SitemapScraper(BaseSitemapScraper):
    """
    This class is used to scrape the sitemap URLs for Chick-fil-e restaurant chain from their sitemap.
    It has no additional changes and can be handled entirely by the base class.
    Hence, it only defines the default attributes for the BaseSitemapScraper to function.
    """
    def __init__(self, 
                restaurant_name="Chick-fil-e", 
                source_path="https://www.chick-fil-a.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/chick-fil-e7.csv",
                url_component_length=6, 
                datapoints={
                    "base_url": 2,
                    "state/country": 4,
                    "city/location": 5,
                },
                substring_check="https://www.chick-fil-a.com/locations"
    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Chick_fil_e_SitemapScraper class __init__(): {traceback.format_exc()}")


class Popeyes_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Popeyes", 
                source_path="https://www.popeyes.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/popeyes.csv",
                url_component_length=7, 
                datapoints={
                    "base_url": 2,
                    "state": 6,
                    "city": 6,
                    "address": 6,
                    "zip_code": 6,
                    "id": 5,
                },
                substring_check="https://www.popeyes.com/store-locator/store/"
    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Popeyes_SitemapScraper class __init__(): {traceback.format_exc()}")


    def parse_sitemap_url(self, url):
        "https://www.popeyes.com/store-locator/store/13177/3411-s-camden-rd-pine-bluff--arkansas--arkansas--71603"
        {
            "base_url": 2,
            "state": 6,
            "city": 6,
            "address": 6,
            "zip_code": 6,
            "id": 5,
        }
        try:
            if self.substring_check and self.substring_check not in url:
                return False, None
            
            url_components = url.split("/")
            if len(url_components) < self.url_component_length:
                return False, None
            
            address_string = url_components[6]
            address_components = address_string.split("--")
                        
            row_data = []
            row_data.append(url_components[2]) # base_url
            row_data.append(address_components[0]) # address
            row_data.append(address_components[-3]) # city
            row_data.append(address_components[-2]) # state
            row_data.append(address_components[-1]) # zip_code
            row_data.append(url_components[5]) # id
            row_data.append(url)
            
            return True, row_data
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")
            return False, e


class Arbys_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Arby's", 
                source_path="https://www.arbys.com/locations.xml", 
                result_path="Sitemaps/New Parser/arbys.csv",
                url_component_length=9,
                datapoints={
                    "base_url": 2,
                    "country": 4,
                    "state": 5,
                    "city": 6,
                    "address": 7,
                    "id": 8,
                },
                substring_check="https://www.arbys.com/locations/"
    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Arbys_SitemapScraper class __init__(): {traceback.format_exc()}")


class DairyQueen_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Dairy Queen", 
                source_path="https://www.dairyqueen.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/dairy_queen.csv",
                url_component_length=9,
                datapoints={
                    "base_url": 2,
                    "state": 5,
                    "city": 6,
                    "address": 7,
                    "id": 8,
                },
                substring_check="https://www.dairyqueen.com/en-us/locations/"
    ):
        try:
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in DairyQueen_SitemapScraper class __init__(): {traceback.format_exc()}")


class JackInTheBox_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Jack In The Box", 
                source_path="https://locations.jackinthebox.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/jack_in_the_box.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "city": 5,
                    "address": 6,
                },
                substring_check="https://locations.jackinthebox.com/"
    ):
        try:
            "https://locations.jackinthebox.com/us/wa/bellingham/1020-w-bakerview-rd"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in JackInTheBox_SitemapScraper class __init__(): {traceback.format_exc()}")


class Ihop_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Ihop", 
                source_path="https://restaurants.ihop.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/ihop.csv",
                url_component_length=8,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "restaurant": 6,
                    "type": 7,
                },
                substring_check="https://restaurants.ihop.com/en-us/"
    ):
        try:
            "https://restaurants.ihop.com/en-us/tx/cedar-hill/breakfast-205-e-fm-1382-1450/takeout"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Ihop_SitemapScraper class __init__(): {traceback.format_exc()}")


class OutbackSteakhouse_SitemapScraper(SitemapScraperBlacklistedKeywords):
    def __init__(self, 
                restaurant_name="Outback Steakhouse", 
                source_path="https://locations.outback.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/outback_steakhouse.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.outback.com/",
                blacklisted_keywords = ["careers"]
    ):
        try:
            "https://locations.outback.com/north-carolina/gastonia/501-north-new-hope-road"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
                blacklisted_keywords=blacklisted_keywords,
            )
        except Exception as e:
            logging.error(f"Error in OutbackSteakhouse_SitemapScraper class __init__(): {traceback.format_exc()}")


class FiveGuys_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Five Guys", 
                source_path="https://restaurants.fiveguys.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/five_guys.csv",
                url_component_length=4,
                datapoints={
                    "base_url": 2,
                    "restaurant": 3,
                },
                substring_check="https://restaurants.fiveguys.com"
    ):
        try:
            "https://restaurants.fiveguys.com/6860-highway-90"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in FiveGuys_SitemapScraper class __init__(): {traceback.format_exc()}")

    def parse_sitemap_url(self, url):
        try:
            if len(url.split("/")) > 4:
                return False, None
            return super().parse_sitemap_url(url)
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")


class JimmyJohns_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Jimmy Johns", 
                source_path="https://locations.jimmyjohns.com/sitemap.xml",
                result_path="Sitemaps/New Parser/jimmy_johns.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.jimmyjohns.com/"
    ):
        try:
            "https://locations.jimmyjohns.com/in/kokomo/delivery-1692.html"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in JimmyJohns_SitemapScraper class __init__(): {traceback.format_exc()}")

    def parse_sitemap_url(self, url):
        try:
            if url.endswith("/"):
                return False, None
            return super().parse_sitemap_url(url)
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")


class Subway_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Subway", 
                source_path="https://restaurants.subway.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/subway.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "city": 5,
                    "address": 6,
                },
                substring_check="https://restaurants.subway.com/"
    ):
        try:
            "https://restaurants.subway.com/canada/qc/thurso/299-rue-victoria"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Subway_SitemapScraper class __init__(): {traceback.format_exc()}")


class DunkinDonut_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Dunkin Donuts", 
                source_path="https://locations.dunkindonuts.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/dunkin_donuts.csv",
                url_component_length=8,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "address": 6,
                    "store_id": 7,
                },
                substring_check="https://locations.dunkindonuts.com/en"
    ):
        try:
            "https://locations.dunkindonuts.com/en/ok/oklahoma-city/9100-s-western-ave/354523"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in DunkinDonut_SitemapScraper class __init__(): {traceback.format_exc()}")


class Dominos_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Dominos", 
                source_path="https://pizza.dominos.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/dominos.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5,
                },
                substring_check="https://pizza.dominos.com/"
    ):
        try:
            "https://pizza.dominos.com/north-carolina/greensboro/4610-woody-mill-road"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Dominos_SitemapScraper class __init__(): {traceback.format_exc()}")


class Pizzahut_SitemapScraper(SitemapScraperNestedSitemap, SitemapScraperOptionalDatapoints):
    def __init__(self, 
                restaurant_name="Pizza Hut", 
                source_path="https://locations.pizzahut.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/pizza_hut.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5,
                },
                optional_datapoints = {
                    "type": 6
                },
                substring_check="https://locations.pizzahut.com/",
    ):
        try:
            "https://locations.pizzahut.com/ca/redwood-city/600-w-whipple/food-places"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
                optional_datapoints = optional_datapoints,
            )
        except Exception as e:
            logging.error(f"Error in Pizzahut_SitemapScraper class __init__(): {traceback.format_exc()}")


class KFC_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="KFC", 
                source_path="https://locations.kfc.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/kfc.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5,
                    "type": 6,
                },
                substring_check="https://locations.kfc.com/",
    ):
        try:
            "https://locations.kfc.com/in/elkhart/1900-cassopolis-street/delivery"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in KFC_SitemapScraper class __init__(): {traceback.format_exc()}")


class DelTaco_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Del Taco", 
                source_path="https://locations.deltaco.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/del_taco.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "address": 6,
                },
                substring_check="https://locations.deltaco.com/",
    ):
        try:
            "https://locations.deltaco.com/us/ca/escondido/110-w-el-norte-parkway"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in DelTaco_SitemapScraper class __init__(): {traceback.format_exc()}")


class KrispyKreme_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Kripsy Kreme", 
                source_path="https://site.krispykreme.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/krispy_kreme.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5,
                },
                substring_check="https://site.krispykreme.com/",
    ):
        try:
            "https://site.krispykreme.com/fl/tallahassee/1300-e-park-ave"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in KrispyKreme_SitemapScraper class __init__(): {traceback.format_exc()}")


class Carrabbas_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Carrabba's Italian Grill", 
                source_path="https://locations.carrabbas.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/carrabbas.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5,
                },
                substring_check="https://locations.carrabbas.com/",
    ):
        try:
            "https://locations.carrabbas.com/virginia/roanoke/4822-d-valley-view-blvd-nw"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Carrabbas_SitemapScraper class __init__(): {traceback.format_exc()}")


class PapaJohn_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Papa Johns", 
                source_path="https://locations.papajohns.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/papa_johns.csv",
                url_component_length=8,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "zipcode": 5,
                    "city": 6,
                    "address": 7,
                },
                substring_check="https://locations.papajohns.com/",
    ):
        try:
            "https://locations.papajohns.com/united-states/tx/78253/san-antonio/11823-culebra-rd"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in PapaJohn_SitemapScraper class __init__(): {traceback.format_exc()}")


class Sonic_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Sonic", 
                source_path="https://www.sonicdrivein.com/locations.xml", 
                result_path="Sitemaps/New Parser/sonic.csv",
                url_component_length=9,
                datapoints={
                    "base_url": 2,
                    "country": 4,
                    "state": 5,
                    "city": 6,
                    "address": 7,
                    "store_id": 8
                },
                substring_check="https://www.sonicdrivein.com/locations/",
    ):
        try:
            "https://www.sonicdrivein.com/locations/us/va/chesapeake/1216-battlefield-blvd--north/store-4385"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Sonic_SitemapScraper class __init__(): {traceback.format_exc()}")


class PandaExpress_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Panda Express", 
                source_path="https://www.pandaexpress.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/panda_express.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "store_id": 6
                },
                substring_check="https://www.pandaexpress.com/locations/",
    ):
        try:
            "https://www.pandaexpress.com/locations/fl/jacksonville/3047"

            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in PandaExpress_SitemapScraper class __init__(): {traceback.format_exc()}")


class BaskinRobbins_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Baskin Robbins", 
                source_path="https://locations.baskinrobbins.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/baskin_robbins.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5
                },
                substring_check="https://locations.baskinrobbins.com/",
    ):
        try:
            "https://locations.baskinrobbins.com/va/luray/1046-us-highway-211-w-357066-br"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in BaskinRobbins_SitemapScraper class __init__(): {traceback.format_exc()}")


class TropicalSmothie_SitemapScraper(SitemapScraperNestedSitemap):
    def __init__(self, 
                restaurant_name="Tropical Smoothie", 
                source_path="https://locations.tropicalsmoothiecafe.com/sitemap.xml", 
                result_path="Sitemaps/New Parser/tropical_smoothie.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5
                },
                substring_check="https://locations.tropicalsmoothiecafe.com/",
    ):
        try:
            "https://locations.tropicalsmoothiecafe.com/sc/charleston/869-folly-rd"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in TropicalSmothie_SitemapScraper class __init__(): {traceback.format_exc()}")


class Dennys_SitemapScraper(SitemapScraperOptionalDatapoints):
    def __init__(self, 
                restaurant_name="Denny's", 
                source_path="https://locations.dennys.com/sitemap.xml",
                result_path="Sitemaps/New Parser/dennys.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "address": 5
                },
                substring_check="https://locations.dennys.com/",
                optional_datapoints = {
                    "type": 6
                }
    ):
        try:
            "https://locations.dennys.com/MD/WALDORF/9569-breakfast/breakfast.html"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
                optional_datapoints = optional_datapoints,
            )
        except Exception as e:
            logging.error(f"Error in Dennys_SitemapScraper class __init__(): {traceback.format_exc()}")


class Chilis_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Chili's", 
                source_path="https://www.chilis.com/sitemap.xml",
                result_path="Sitemaps/New Parser/chilis.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "country": 4,
                    "state": 5,
                    "city": 6,
                },
                substring_check="https://www.chilis.com/locations/",
    ):
        try:
            "https://www.chilis.com/locations/us/connecticut/stamford"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Chilis_SitemapScraper class __init__(): {traceback.format_exc()}")


class FirehouseSub_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Firehouse Subs", 
                source_path="https://www.firehousesubs.com/sitemap.xml",
                result_path="Sitemaps/New Parser/firehouse_subs.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "state": 6,
                    "city": 6,
                    "address": 6,
                    "zip_code": 6,
                    "store_id": 5
                },
                substring_check="https://www.firehousesubs.com/store-locator",
    ):
        try:
            "https://www.firehousesubs.com/store-locator/store/1999/2681-fort-campbell-blvd--clarksville--tennessee--37042"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in FirehouseSub_SitemapScraper class __init__(): {traceback.format_exc()}")


    def parse_sitemap_url(self, url):
        try:
            if self.substring_check and self.substring_check not in url:
                return False, None
            
            url_components = url.split("/")
            if len(url_components) < self.url_component_length:
                return False, None
            
            address_string = url_components[6]
            address_components = address_string.split("--")
                        
            row_data = []
            row_data.append(url_components[2]) # base_url
            row_data.append(address_components[-2]) # state
            row_data.append(address_components[-3]) # city
            row_data.append(address_components[0]) # address
            row_data.append(address_components[-1]) # zip_code
            row_data.append(url_components[5]) # id
            row_data.append(url)
            
            return True, row_data
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")
            return False, e



class TheBurgerDen_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="The Burger Den", 
                source_path="https://img.cdn4dd.com/s/managed/storefront/sitemap-stores.xml",
                result_path="Sitemaps/New Parser/the_burger_den.csv",
                url_component_length=5,
                datapoints={
                    "base_url": 2,
                    "store_id": 4
                },
                substring_check="https://order.online/store/",
    ):
        try:
            "https://order.online/store/Zantigo-Mexican-Restaurant-160874/?hideModal=true"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in TheBurgerDen_SitemapScraper class __init__(): {traceback.format_exc()}")




class Hardees_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Hardees", 
                source_path="https://order.hardees.com/sitemap.xml",
                result_path="Sitemaps/New Parser/hardees.csv",
                url_component_length=5,
                datapoints={
                    "base_url": 2,
                    "restaurant": 4
                },
                substring_check="https://order.hardees.com/location",
    ):
        try:
            "https://order.hardees.com/location/-ms-booneville-1202-n-2nd-st/menu"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Hardees_SitemapScraper class __init__(): {traceback.format_exc()}")

    def parse_sitemap_url(self, url):
        try:
            url = url[8:]

            return super().parse_sitemap_url(url)
        except Exception as e:
            logging.error(f"Error in parse_sitemap_url(): {traceback.format_exc()}")
            return False, e



class Whataburger_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Whataburger", 
                source_path="https://locations.whataburger.com/sitemap.xml",
                result_path="Sitemaps/New Parser/whataburger.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.whataburger.com/",
    ):
        try:
            "https://locations.whataburger.com/ok/lawton/2201-nw-cache-rd/curbside.html"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Whataburger_SitemapScraper class __init__(): {traceback.format_exc()}")


    def parse_sitemap_url(self, url):
        if len(url.split("/")) > 6:
            return None, "Category URL."
        if "/area/" in url:
            return None, "Area URL"
        return super().parse_sitemap_url(url)


class CheckersSitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Checkers", 
                source_path="https://locations.checkers.com/sitemap.xml",
                result_path="Sitemaps/New Parser/checkers.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.checkers.com",
    ):
        try:
            "https://locations.checkers.com/tn/lavergne/5062-murfreesboro-rd."
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in CheckersSitemapScraper class __init__(): {traceback.format_exc()}")


class Churchs_Chicken_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Church's Chicken", 
                source_path="https://locations.churchs.com/sitemap.xml",
                result_path="Sitemaps/New Parser/churchs_chicken.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.churchs.com/",
    ):
        try:
            "https://locations.churchs.com/mo/st-louis/4401-marshall-road"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Churchs_Chicken_SitemapScraper class __init__(): {traceback.format_exc()}")



class Bonjangles_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Bojangle's Chicken", 
                source_path="https://locations.bojangles.com/sitemap.xml",
                result_path="Sitemaps/New Parser/bonjangle.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.bojangles.com/",
    ):
        try:
            "https://locations.bojangles.com/nc/statesville/107-beechnut-lane.html"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Bonjangles_SitemapScraper class __init__(): {traceback.format_exc()}")




class Greggs_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Gregggs", 
                source_path="https://www.greggs.co.uk/sitemap.xml",
                result_path="Sitemaps/New Parser/greggs.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "city": 4,
                    "restaurant": 5,
                    "store_id": 6
                },
                substring_check="https://www.greggs.co.uk/shops/",
    ):
        try:
            "https://www.greggs.co.uk/shops/darlington/68-skinnergate/0030"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Greggs_SitemapScraper class __init__(): {traceback.format_exc()}")




class CrumblCookies_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Crumbl_Cookies", 
                source_path="https://crumblcookies.com/sitemap.xml",
                result_path="Sitemaps/New Parser/crumbl_cookies.csv",
                url_component_length=5,
                datapoints={
                    "base_url": 2,
                    "restaurant": 4,
                    "store_id": 4
                },
                substring_check="https://crumblcookies.com/nutrition/",
    ):
        try:
            "https://crumblcookies.com/nutrition/flbannerman"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in CrumblCookies_SitemapScraper class __init__(): {traceback.format_exc()}")




class ItsJustWings_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="ItsJustWings", 
                source_path="https://locations.itsjustwings.com/sitemap.xml",
                result_path="Sitemaps/New Parser/its_just_wings.csv",
                url_component_length=5,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4
                },
                substring_check="https://locations.itsjustwings.com/",
    ):
        try:
            "https://locations.itsjustwings.com/co/littleton"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in ItsJustWings_SitemapScraper class __init__(): {traceback.format_exc()}")



class AandW_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="A&W", 
                source_path="https://awrestaurants.com/sitemap.xml",
                result_path="Sitemaps/New Parser/a_and_w.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "state": 4,
                    "city": 5,
                    "restaurant": 6,
                },
                substring_check="http://awdev.dev.wwbtc.com/locations/",
    ):
        try:
            "http://awdev.dev.wwbtc.com/locations/wisconsin/siren/24133-state-road-3570"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in AandW_SitemapScraper class __init__(): {traceback.format_exc()}")
    
    def write_restaurant_row_to_csv(self, row, csv_writer):
        try:
            print("here")
            row[0] = "https://awrestaurants.com/"
            row[-1] = row[-1].replace("http://awdev.dev.wwbtc.com/", "https://awrestaurants.com/")
            csv_writer.writerow(row)
            return True
        except Exception as e:
            logging.error(f"Error in write_restaurant_row_to_csv(): {traceback.format_exc()}")
            return False


class Qdoba_SitemapScraper(SitemapScraperBlacklistedKeywords):
    def __init__(self, 
                restaurant_name="Qdoba", 
                source_path="https://locations.qdoba.com/sitemap.xml",
                result_path="Sitemaps/New Parser/qdoba.csv",
                url_component_length=7,
                datapoints={
                    "base_url": 2,
                    "country": 3,
                    "state": 4,
                    "city": 5,
                    "restaurant": 6,
                },
                substring_check="https://locations.qdoba.com/",
                blacklisted_keywords = ["catering"]
                
    ):
        try:
            "https://locations.qdoba.com/us/in/columbus/1665-n-national-rd/catering.html"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
                blacklisted_keywords = blacklisted_keywords

            )
        except Exception as e:
            logging.error(f"Error in Qdoba_SitemapScraper class __init__(): {traceback.format_exc()}")
    



class PapaMurphys_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Papa Murphy's", 
                source_path="https://locations.papamurphys.com/sitemap.xml",
                result_path="Sitemaps/New Parser/papa_murphys.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.papamurphys.com/",
                
    ):
        try:
            "https://locations.papamurphys.com/ia/altoona/3418-8th-street-southwest"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in PapaMurphy_SitemapScraper class __init__(): {traceback.format_exc()}")
    

class Moes_SitemapScraper(BaseSitemapScraper):
    def __init__(self, 
                restaurant_name="Moe's Mexican Grill", 
                source_path="https://locations.moes.com/sitemap.xml",
                result_path="Sitemaps/New Parser/moes.csv",
                url_component_length=6,
                datapoints={
                    "base_url": 2,
                    "state": 3,
                    "city": 4,
                    "restaurant": 5,
                },
                substring_check="https://locations.moes.com/",
                
    ):
        try:
            "https://locations.moes.com/ar/little-rock/12312-chenal-parkway"
            super().__init__(
                restaurant_name = restaurant_name,
                source_path = source_path,
                result_path = result_path,
                url_component_length = url_component_length,
                datapoints = datapoints,
                substring_check = substring_check,
            )
        except Exception as e:
            logging.error(f"Error in Moes_SitemapScraper class __init__(): {traceback.format_exc()}")
    


class ScraperMapper():
    def __init__(self):
        self.mapper = {
            "chickfile": Chick_fil_e_SitemapScraper,
            "tacobell": Taco_bell_SitemapScraper,
            "wendys": Wendys_SitemapScraper,
            "applebees": Applebees_SitemapScraper,
            "olivegarden": OliveGarden_SitemapScraper,
            "chipotle": Chipotle_SitemapScraper,
            "buffalowildwings": BuffaloWildwings_SitemapScraper,
            "popeyes": Popeyes_SitemapScraper,
            "arbys": Arbys_SitemapScraper,
            "dairyqueen": DairyQueen_SitemapScraper,
            "jackinthebox": JackInTheBox_SitemapScraper,
            "ihop": Ihop_SitemapScraper,
            "outbacksteakhouse": OutbackSteakhouse_SitemapScraper,
            "fiveguys": FiveGuys_SitemapScraper,
            "jimmyjohns": JimmyJohns_SitemapScraper,
            "subway": Subway_SitemapScraper,
            "dunkindonuts": DunkinDonut_SitemapScraper,
            "dominos": Dominos_SitemapScraper,
            "pizzahut": Pizzahut_SitemapScraper,
            "kfc": KFC_SitemapScraper,
            "deltaco": DelTaco_SitemapScraper,
            "krispykreme": KrispyKreme_SitemapScraper,
            "carrabbas": Carrabbas_SitemapScraper,
            "papajohns": PapaJohn_SitemapScraper,
            "sonic": Sonic_SitemapScraper,
            "pandaexpress": PandaExpress_SitemapScraper,
            "baskinrobbins": BaskinRobbins_SitemapScraper,
            "tropicalsmoothie": TropicalSmothie_SitemapScraper,
            "dennys": Dennys_SitemapScraper,
            "chilis": Chilis_SitemapScraper,
            "firehousesub": FirehouseSub_SitemapScraper,
            "theburgerden": TheBurgerDen_SitemapScraper,
            "hardees": Hardees_SitemapScraper,
            "whataburger": Whataburger_SitemapScraper,
            "checkers": CheckersSitemapScraper,
            "churchschicken": Churchs_Chicken_SitemapScraper,
            "bojangles": Bonjangles_SitemapScraper,
            "greggs": Greggs_SitemapScraper,
            "crumblcookies": CrumblCookies_SitemapScraper,
            "itsjustwings": ItsJustWings_SitemapScraper,
            "aandw": AandW_SitemapScraper,
            "qdoba": Qdoba_SitemapScraper,
            "papamurphys": PapaMurphys_SitemapScraper,
            "moes": Moes_SitemapScraper,
        }
    
    def get_scraper_class(self, restaurant_name=None):
        if not restaurant_name:
            return None, "Please provide a restaurant name to start."
        cleaned_restaurant_name = self.remove_special_characters(restaurant_name)
        scraper_class = self.mapper.get(cleaned_restaurant_name, None)
        if not scraper_class:
            return None, f"Scraper not found for the restaurant {restaurant_name} (after cleaning: {cleaned_restaurant_name}).\nAvailable restaurants: {list(self.mapper.keys())}"
        return scraper_class(), ""
    
    def remove_special_characters(self, input_string):
        pattern = r'[^a-zA-Z0-9]'
        result = re.sub(pattern, '', input_string)
        
        return result.lower()

    

class WebUrlScraper:

    def __init__(self, output_path, output_format, datapoints):
        self.datapoints = datapoints
        self.output_path = output_path
        self.output_format = output_format
        self.output_filepath = (
            output_path + "." + output_format
        )
        self.input_data = None

    def fetch_data(self, url=None, file_path=None, source_type=None):
        if source_type == "filepath":
            pass
        elif source_type == "url":
            headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if int(response.status_code) == 200:
                parsed_dict = xmltodict.parse(response.text)
                self.input_data = parsed_dict
                return parsed_dict, True
            else:
                return response.text, False

    def parse_data(
        self,
        write_in_csv=False,
        substring_check=None,
        return_data=False,
        url_component_length=6,
        fixed_indices=[],
        optional_indices=[],
        blacklisted_keywords=[],
        custom_check=None,
        custom_parser=None,
    ):

        if write_in_csv:
            file = open(self.output_filepath, mode="w", newline="", encoding="utf-8")
            writer = csv.writer(file)
            writer.writerow(self.datapoints)

        if return_data:
            fetched_data = [self.datapoints]

        interrupt_processing = False

        if interrupt_processing:
            return True, "Process interrupted manually !"
        for row in self.input_data["urlset"]["url"]:
            try:
                url_path = row.get("loc")
                if substring_check and substring_check not in url_path:
                    continue
                if any([x in url_path for x in blacklisted_keywords]):
                    continue
                if custom_check:
                    custom_check_passed = custom_check(url_path)
                    if not custom_check_passed:
                        continue
                url_components = url_path.split("/")
                if len(url_components) >= url_component_length:
                    row_data = [url_components[index] for index in fixed_indices]
                    row_data.extend(
                        [
                            url_components[index] if len(url_components) > index else ""
                            for index in optional_indices
                        ]
                    )

                    row_data.append(url_path)
                    if custom_parser:
                        row_data = custom_parser(data=row_data)

                    if write_in_csv:
                        writer.writerow(row_data)
                    if return_data:
                        fetched_data.append(row_data)
            except Exception as e:
                import traceback

                print(
                    "Failed for row: ", row["loc"], "\nError: ", 
                )
        if write_in_csv:
            file.close()

        if return_data:
            return False, fetched_data
        return False, None

    def close(self):
        print("scraper closed elegantly !")



if __name__ == "__main__":
    scraper_mapper = ScraperMapper()
    scraper, message = scraper_mapper.get_scraper_class(restaurant_name=sys.argv[1])
    if not scraper:
        logging.info(message)
    else:
        scraper.scrape()

    logging.info("Scraping script finished executing.\n\n\n")


