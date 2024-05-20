# Amazon Scraper
import os
import logging
from datetime import datetime
from lxml import html
import re

from lib import RequestHandler, htmlLib, DatabaseUtil

class AmazonScraper(htmlLib):
    def __init__(self):
        super().__init__()
        self.wesbite_name = "amazon"
        self.stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.url = "https://www.amazon.in/s?k={}&page={}&ref=sr_pg_{}"
        self.website = "https://www.amazon.in"
        self.productUrlXpath = '//*[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]//@href'
        self.paginationXpath = '//*[@class="a-section a-spacing-small a-spacing-top-small"]//span[1]//text()'
        self.product_title_xpath = '//*[@id="productTitle"]//text()'
        self.product_description_xpath = '//*[@id="productDescription"]//span//text()'
        self.product_image_xpath = '//*[@id="landingImage"]//@src'
        self.product_category_xpath = '//*[@class="a-link-normal a-color-tertiary"]//text()'
        self.product_price_xpath = '//*[@class="a-price-whole"]//text()'
        
        self.pagination = 1

    def getProducts(self, keyword, page):
        return None

    def getProductDetails(self, productUrl): 
        return None

    # def main(self, keyword, number_of_threads):
    #     # get products
    #     products = []
    #     for page in range(1, self.pagination+1):
    #         products.extend(self.getProducts(keyword, page))


    #     if self.pagination > 1:
    #         for page in range(2, self.pagination+1):
    #             products.extend(self.getProducts(keyword, page))


    #     # get product details
    #     with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
    #         results = executor.map(self.getProductDetails, products)

    #         # save to db
    #         for result in results:
    #             print(f"Saving {result['sku']} to db")
    #             self.db.insertProduct(result)
        


# if __name__ == '__main__':
    
#     number_of_threads = 10
#     scraper = Scraper()

#     # Log start of scraper
#     logging.info(f"Starting {scraper.rival} scraper")

#     # make db amazon.db if it doesn't exist
#     if not os.path.exists(scraper.storagePath + scraper.rival + ".db"):
#         print(f'Creating amazon.db at {scraper.storagePath+ scraper.rival + ".db"}')
#         db = AmazonDatabaseConnector(scraper.stamp)
#         logging.info(f"Creating {scraper.rival}.db")
#         db.schemaMaker()
    
#     scraper.db = AmazonDatabaseConnector(scraper.stamp)
    
    
#     for keyword in product_categories:
#         scraper.main(keyword, number_of_threads)
#         scraper.pagination = 1
#         htmlLib.reqSession = requests.Session()
    
#     scraper.db.removeDuplicates()
    
