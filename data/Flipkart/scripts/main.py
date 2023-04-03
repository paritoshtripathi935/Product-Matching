import logging
from datetime import datetime
from dbConnector import FlipkartDatabaseConnector
from productList import product_categories
from genricHtmlib import SeleniumScraper
import os
import lxml.html as html

SeleniumScraper = SeleniumScraper()

class Scraper:
    def __init__(self):
        self.rival: str = "flipkart"
        self.website = "https://www.flipkart.com/search?q="
        self.websiteName = "https://www.flipkart.com"
        self.stamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.storagePath: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../"
        )
        if not os.path.exists(self.storagePath + "logs"):
            print(f"Creating logs folder at {self.storagePath + 'logs'}")
            os.makedirs(self.storagePath + "logs")

        logging.basicConfig(
            filename=self.storagePath + "logs/{rival}_Scraper_{stamp}.log".format(rival=self.rival, stamp=self.stamp),
            level=logging.INFO,
            filemode="w",
        )
        self.productLinksXpath = '//*[@rel="noopener noreferrer"]//@href'

    def getProductList(self, keyword):
        try:
            productLinks = []
            url = self.website + keyword
            response = SeleniumScraper.fetch_request_normal(url)
            if response is None:
                doc = SeleniumScraper.fetch_request_selenium(url)
            else:
                doc = html.fromstring(response)
            
            Links = SeleniumScraper.get_xpath_link(doc, self.productLinksXpath, self.websiteName)
            productLinks.extend(Links)

            for page in range(2, 20):
                url = self.website + keyword + "&page=" + str(page)
                response = SeleniumScraper.fetch_request_normal(url)
                if response is None:
                    doc = SeleniumScraper.fetch_request_selenium(url)
                else:
                    doc = html.fromstring(response)
                
                Links = SeleniumScraper.get_xpath_link(doc, self.productLinksXpath, self.websiteName)
                productLinks.extend(Links)

            print(f'Total products for {keyword} is {len(productLinks)}')
            return productLinks
        
        except Exception as e:
            print(e)

    def getProductDetails(self, productLink):
        response = SeleniumScraper.fetch_request_normal(productLink)
        if response is None:
            doc = SeleniumScraper.fetch_request_selenium(productLink)
        else:
            doc = html.fromstring(response)

        try:
            productName = SeleniumScraper.get_xpath_data(doc, '//*[@class="_35KyD6"]//text()')
            productPrice = SeleniumScraper.get_xpath_data(doc, '//*[@class="_1vC4OE _3qQ9m1"]//text()')
            productRating = SeleniumScraper.get_xpath_data(doc, '//*[@class="_3LWZlK _1BLPMq"]//text()')
            productRatingCount = SeleniumScraper.get_xpath_data(doc, '//*[@class="_38sUEc"]//text()')
            productDescription = SeleniumScraper.get_xpath_data(doc, '//*[@class="_1mXcCf RmoJUZ"]//text()')
            productImage = SeleniumScraper.get_xpath_data(doc, '//*[@class="_3nWP9Q"]//@src')
            productBrand = SeleniumScraper.get_xpath_data(doc, '//*[@class="_2B_pmu"]//text()')

            print(productName)
            print(productPrice)
            print(productRating)
            print(productRatingCount)
            print(productDescription)
            print(productImage)
            print(productBrand)
        except Exception as e:
            print(e)
        


    def start(self):
        number_of_threads: int = 10

        # Log start of scraper
        logging.info(f"Starting {self.rival} scraper")

        # make db amazon.db if it doesn't exist
        if not os.path.exists(self.storagePath + self.rival + ".db"):
            print(f'Creating {self.rival}.db at {self.storagePath+self.rival+".db"}')
            db = FlipkartDatabaseConnector(self.stamp)
            logging.info(f'Creating {self.rival}.db at {self.storagePath+self.rival+".db"}')
            db.schemaMaker()
            logging.info(db.welcomeMessage)

        self.db = FlipkartDatabaseConnector(self.stamp)
        print(self.db.welcomeMessage)

        for category in product_categories:
            productUrls = self.getProductList(category)
            for productUrl in productUrls:
                self.getProductDetails(productUrl)
                break
            break

    

if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()