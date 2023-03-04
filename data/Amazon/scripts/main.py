# Amazon Scraper

import os
import logging
from datetime import datetime
from dbConnector import AmazonDatabaseConnector
import re
import time
import uuid
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import json
from genricHtmlib import SeleniumScraper
from lxml import html
import traceback

SeleniumScraper = SeleniumScraper()


class Scraper:
    def __init__(self):
        self.stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.storagePath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../"
        )

        logging.basicConfig(
            filename=self.storagePath + "logs/amazonScraper_{}.log".format(self.stamp),
            level=logging.INFO,
            filemode="w",
        )
        self.db = AmazonDatabaseConnector(self.stamp)

        self.url = "https://www.amazon.com/s?k={}&page={}&ref=sr_pg_{}"
        self.website = "https://www.amazon.com"
        self.productUrlXpath = '//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//@href'
    
    def getProducts(self, keyword, page):
        try:
            url = self.url.format(keyword, page, page)
            print(f"Scraping {url}")

            doc = SeleniumScraper.fetch_request_selenium(url)
            #doc = html.fromstring(response)
            # get product urls

            productUrls = SeleniumScraper.get_xpath_link(doc, self.productUrlXpath, self.website)
            print(f"Found {len(productUrls)} products for product {keyword} on page {page}")
            return productUrls

        except Exception as e:
            traceback.print_exc()
            logging.error(f"Error while scraping products for keyword {keyword} on page {page}: {e}")
            print(f"Error while scraping products for keyword {keyword} on page {page}: {e}")
            return []        

    def getProductDetails(self, productUrl):
        print(f"Scraping {productUrl}")
        response = SeleniumScraper.fetch_request_normal(productUrl)
        doc = html.fromstring(response)
        

        productDetails = {}
        sku = productUrl.split("/dp/")[1].split("/ref")[0]
        productDetails["sku"] = sku
        productDetails["url"] = productUrl


        self.db.insertProduct(productDetails)
        return productDetails


    def main(self, keyword, pages):
        # get products
        products = []
        for page in range(1, pages+1):
            products.extend(self.getProducts(keyword, page))

        # get product details
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.getProductDetails, products)

                    


if __name__ == '__main__':
    scraper = Scraper()

    # Create logs folder if it doesn't exists
    if not os.path.exists(scraper.storagePath + "logs"):
        os.makedirs(scraper.storagePath + "logs")

    # Log start of scraper
    logging.info("Starting Amazon Scraper")
    logging.info(scraper.db.welcomeMessage)

    # make db amazon.db if it doesn't exist
    if not os.path.exists(scraper.storagePath + "amazon.db"):
        logging.info("Creating amazon.db")  
        scraper.db.schemaMaker()
    
    # start scraper
    scraper.main("shoes", 1)
    