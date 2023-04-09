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
        self.skuXpath = '//tr[contains(@class, "row")]//td[contains(text(), "Model Number")]/following-sibling::td[1]/ul/li/text()'
        self.nameXpath = '//*[@class="B_NuCI"]//text()'
        self.description = '//div[contains(text(), "Description")]/following-sibling::div[1]/div/text()'

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
            sku = None

        try:
            name = SeleniumScraper.get_xpath_data(doc ,self.nameXpath)
            name = name[0]
        except:
            name = None

        try:
            description = SeleniumScraper.get_xpath_data(doc, self.description)
            description = ''.join(description)
        except:
            description = None

        
        

        print(sku)

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
    
        self.getProductDetails("https://www.flipkart.com/flipkart-smartbuy-back-cover-poco-c50-redmi-a1-a1-plus/p/itm264e53259473c?pid=ACCGJFZC6W6KAJTH&lid=LSTACCGJFZC6W6KAJTHC1NL6B&marketplace=FLIPKART&fm=productRecommendation%2Fattach&iid=R%3Aa%3Bp%3AMOBGK8WZYEJ3G5AA%3Bl%3ALSTMOBGK8WZYEJ3G5AAMF47BF%3Bpt%3App%3Buid%3Afcc93816-d6ba-11ed-ab8a-f3d6a6c8dbc1%3B.ACCGJFZC6W6KAJTH&ppt=pp&ppn=pp&ssid=lwsg24277k0000001681033040330&otracker=pp_reco_Buy%2Btogether%2Band%2Bsave%2B30%2525%2Bmore_1_Buy%2Btogether%2Band%2Bsave%2B30%2525%2Bmore_ACCGJFZC6W6KAJTH_productRecommendation%2Fattach_1&otracker1=pp_reco_PINNED_productRecommendation%2Fattach_Buy%2Btogether%2Band%2Bsave%2B30%2525%2Bmore_NA_productCard_cc_1_NA_view-all&cid=ACCGJFZC6W6KAJTH")
        '''
        for category in product_categories:
            productUrls = self.getProductList(category)
            for productUrl in productUrls:
                self.getProductDetails(productUrl)
                break
            break
        '''
    

if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()