# Amazon Scraper

import os
import logging
from datetime import datetime
from dbConnector import AmazonDatabaseConnector
from concurrent.futures import ThreadPoolExecutor
from genricHtmlib import SeleniumScraper
from lxml import html
import re
from productList import product_categories
import time
import threading
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

        self.url = "https://www.amazon.in/s?k={}&page={}&ref=sr_pg_{}"
        self.website = "https://www.amazon.in"
        self.productUrlXpath = '//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//@href'
        self.paginationXpath = '//*[@class="a-section a-spacing-small a-spacing-top-small"]//span[1]//text()'
        self.pagination = 1

    def getProducts(self, keyword, page):
        try:
            url = self.url.format(keyword, page, page)
            print(f"Scraping {url}")

            response = SeleniumScraper.fetch_request_normal(url)

            if response == None:
                print("Normal request failed, trying selenium")
                doc = SeleniumScraper.fetch_request_selenium(url)
            else:
                doc = html.fromstring(response)

            productUrls = SeleniumScraper.get_xpath_link(doc, self.productUrlXpath, self.website)
            print(f"Found {len(productUrls)} products for product {keyword} on page {page}")

            pagination = SeleniumScraper.get_xpath_link(doc, self.paginationXpath, self.website)
            # 1-48 of over 40,000 results for
            # need 48 using regex
            pagination = re.findall(r'\d+', pagination[0])
            self.pagination = int(pagination[1])
            return productUrls

        except Exception as e:
            logging.error(f"Error while scraping products for keyword {keyword} on page {page}: {e}")
            return []        

    def getProductDetails(self, productUrl):
        try:
            response = SeleniumScraper.fetch_request_normal(productUrl)
            if response == None:
                print("Normal request failed, trying selenium")
                doc = SeleniumScraper.fetch_request_selenium(productUrl)
            else:
                doc = html.fromstring(response)
        except Exception as e:
            logging.error(f"Error while scraping product details for product {productUrl}: {e}")
            return {}

        productDetails = {}
        try:
            sku = productUrl.split("dp%2F")[1].split("%2F")[0]
        except:
            try:
                sku = productUrl.split("dp/")[1].split("/")[0]
            except:
                sku = []
            
        name = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="productTitle"]//text()'))
        try:
            description = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="productDescription"]//span//text()'))
            description = " ".join(description)
        except:
            description = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="feature-bullets"]//span//text()'))
            description = " ".join(description)

        try:
            image_path = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="landingImage"]//@src'))
            image_path = image_path[0]
        except:
            image_path = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="imgTagWrapperId"]//@src'))
            image_path = ''.join(image_path)

        category = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@class="a-link-normal a-color-tertiary"]//text()'))
        try:
            category = category[-1]
        except:
            category = []

        if description == []:
            description = "None"
        
        if image_path == []:
            image_path = "None"
        
        if category == []:
            category = "None"
        
        if name == []:
            name = "None"
        
        if sku == []:
            sku = "None"

        if category == []:
            category = "None"


        productDetails["sku"] = str(sku)
        productDetails["name"] = str(name[0])
        productDetails["description"] = str(description)
        productDetails["image_path"] = str(image_path)
        productDetails["category"] = str(category)
        productDetails["timestamp"] = str(self.stamp)
        productDetails["URL"] = str(productUrl)
        
        print(f"Scraping {productDetails['URL']}")
        return productDetails

    def main(self, keyword):
        # get products
        products = []
        for page in range(1, self.pagination+1):
            products.extend(self.getProducts(keyword, page))


        if self.pagination > 1:
            for page in range(2, self.pagination+1):
                products.extend(self.getProducts(keyword, page))
                if page >3:
                    break

        # get product details
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.getProductDetails, products)

            # save to db
            for result in results:
                print(f"Saving {result['sku']} to db")
                self.db.insertProduct(result)
        


if __name__ == '__main__':
    scraper = Scraper()

    # Create logs folder if it doesn't exists
    if not os.path.exists(scraper.storagePath + "logs"):
        os.makedirs(scraper.storagePath + "logs")

    # Log start of scraper
    logging.info("Starting Amazon Scraper")

    # make db amazon.db if it doesn't exist
    if not os.path.exists(scraper.storagePath + "amazon.db"):
        print(f'Creating amazon.db at {scraper.storagePath+"amazon.db"}')
        db = AmazonDatabaseConnector(scraper.stamp)
        logging.info("Creating amazon.db")  
        db.schemaMaker()
    
    scraper.db = AmazonDatabaseConnector(scraper.stamp)
    for keyword in product_categories:
        scraper.main(keyword)
        scraper.pagination = 1
    
    scraper.db.removeDuplicates()