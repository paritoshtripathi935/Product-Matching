import logging
from datetime import datetime
from dbConnector import FlipkartDatabaseConnector
from productList import product_categories
import os


class Scraper:
    def __init__(self):
        self.rival: str = "flipkart"
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

if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()