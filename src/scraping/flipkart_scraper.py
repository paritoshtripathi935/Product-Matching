import logging
from datetime import datetime
from dbConnector import FlipkartDatabaseConnector
from productList import product_categories
from genricHtmlib import SeleniumScraper
import os
import lxml.html as html
import concurrent.futures

SeleniumScraper = SeleniumScraper()

class FlipkartScraper:
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
        self.skuXpath = '//tr[contains(@class, "row")]//td[contains(text(), "Model Number")]/following-sibling::td[1]/ul/li/text()'
        self.nameXpath = '//*[@class="B_NuCI"]//text()'
        self.description = '//div[contains(text(), "Description")]/following-sibling::div[1]/div/text()'
        self.image = '//*[@class="_396cs4 _2amPTt _3qGmMb"]//@src'
        self.category = '//*[@class="_3GIHBu"]//text()'
        self.price = '//*[@class="_30jeq3 _16Jk6d"]//text()'
        
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
                print(f'Geting Page {page} for {keyword}')
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
        print(f'Getting product details for {productLink}')
        response = SeleniumScraper.fetch_request_normal(productLink)
        if response is None:
            doc = SeleniumScraper.fetch_request_selenium(productLink)
        else:
            doc = html.fromstring(response)

        productDetails = {}

        '''
        productDetails["sku"] = str(sku)
        productDetails["name"] = str(name[0])
        productDetails["description"] = str(description)
        productDetails["image_path"] = str(image_path)
        productDetails["category"] = str(category)
        productDetails["timestamp"] = str(self.stamp)
        productDetails["URL"] = str(productUrl)
        productDetails['price'] = price
        '''
        try:
            sku = SeleniumScraper.get_xpath_data(doc ,self.skuXpath)
            sku = sku[0]
        except:
            sku = "None"

        try:
            name = SeleniumScraper.get_xpath_data(doc ,self.nameXpath)
            name = name[0]
        except:
            name = "None"

        try:
            description = SeleniumScraper.get_xpath_data(doc, self.description)
            description = ''.join(description)
        except:
            description = "None"

        try:
            image_path = SeleniumScraper.get_xpath_link(doc, self.image, self.websiteName)
            image_path = image_path[0]
        except:
            image_path = "None"

        try:
            category = SeleniumScraper.get_xpath_data(doc, self.category)
            category = category[1]
        except:
            category = "None"

        try:
            price = SeleniumScraper.get_xpath_data(doc, self.price)
            price = SeleniumScraper.cleanData(price)
            price = price[0]
        except:
            price = "None"    

        productDetails["sku"] = str(sku)
        productDetails["name"] = str(name)
        productDetails["description"] = str(description)
        productDetails["image_path"] = str(image_path)
        productDetails["category"] = str(category)
        productDetails["timestamp"] = str(self.stamp)
        productDetails["URL"] = str(productLink)
        productDetails['price'] = price

        return productDetails

    def start(self):
        productList = []
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
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
           productUrls =  executor.map(self.getProductList, product_categories)
           productList.extend(productUrls)

        
        # flatten the list productList
        productList = [item for sublist in productList for item in sublist]
        print(f'Total products for {self.rival} is {len(productList)}')

        with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            results = executor.map(self.getProductDetails, productList)

            for result in results:
                print(f"Saving {result['sku']} to db")
                self.db.insertProduct(result)

        self.db.removeDuplicates()
        
    
# if __name__ == '__main__':
#     scraper = Scraper()
#     scraper.start()