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
import requests

SeleniumScraper = SeleniumScraper()

class Scraper:
    def __init__(self):
        self.rival = "amazon"
        self.stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.storagePath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../"
        )

        logging.basicConfig(
            filename=self.storagePath + "logs/{}_Scraper_{}.log".format(self.rival, self.stamp),
            level=logging.INFO,
            filemode="w",
        )
        if not os.path.exists(self.storagePath + "logs"):
            print(f"Creating logs folder at {self.storagePath + 'logs'}")
            os.makedirs(self.storagePath + "logs")

        self.url = "https://www.amazon.in/s?k={}&page={}&ref=sr_pg_{}"
        self.website = "https://www.amazon.in"
        self.productUrlXpath = '//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//@href'
        self.paginationXpath = '//*[@class="a-section a-spacing-small a-spacing-top-small"]//span[1]//text()'
        self.pagination = 1

    def getProducts(self, keyword, page):
        try:
            url = self.url.format(keyword, page, page)

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
        except Exception as e:
            try:
                description = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="feature-bullets"]//span//text()'))
                description = " ".join(description)
            except:
                logging.error(f"Error while scraping product description for product {productUrl}: {e}")

        try:
            image_path = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="landingImage"]//@src'))
            image_path = image_path[0]
        except Exception as e:
            try:
                image_path = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@id="imgTagWrapperId"]//@src'))
                image_path = ''.join(image_path)
            except:
                logging.error(f"Error while scraping product image for product {productUrl}: {e}")

        category = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@class="a-link-normal a-color-tertiary"]//text()'))
        try:
            category = category[-1]
        except:
            category = []

        try:
            price = SeleniumScraper.cleanData(SeleniumScraper.get_xpath_data(doc, '//*[@class="a-price-whole"]//text()'))[0]
            price = price.replace(",", "")
            price = int(price)
        except Exception as e:
            logging.error(f"Error while scraping product price for product {productUrl}: {e}")
            price = []

        if price == []:
            price = "None"

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
        productDetails['price'] = price
        
        
        print(productDetails)
        return productDetails

    def main(self, keyword, number_of_threads):
        # get products
        products = []
        for page in range(1, self.pagination+1):
            products.extend(self.getProducts(keyword, page))


        if self.pagination > 1:
            for page in range(2, self.pagination+1):
                products.extend(self.getProducts(keyword, page))


        # get product details
        with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            results = executor.map(self.getProductDetails, products)

            # save to db
            for result in results:
                print(f"Saving {result['sku']} to db")
                self.db.insertProduct(result)
        


if __name__ == '__main__':
    
    number_of_threads = 10
    scraper = Scraper()

    # Log start of scraper
    logging.info(f"Starting {scraper.rival} scraper")

    # make db amazon.db if it doesn't exist
    if not os.path.exists(scraper.storagePath + scraper.rival + ".db"):
        print(f'Creating amazon.db at {scraper.storagePath+ scraper.rival + ".db"}')
        db = AmazonDatabaseConnector(scraper.stamp)
        logging.info(f"Creating {scraper.rival}.db")
        db.schemaMaker()
    
    scraper.db = AmazonDatabaseConnector(scraper.stamp)
    
    
    for keyword in product_categories:
        scraper.main(keyword, number_of_threads)
        scraper.pagination = 1
        # make new request session 
        SeleniumScraper.reqSession = requests.Session()
    
    scraper.db.removeDuplicates()
    
