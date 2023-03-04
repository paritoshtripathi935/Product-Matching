# Amazon Scraper

import os
import logging
from datetime import datetime
from dbConnector import AmazonDatabaseConnector

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
        self.url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2" # search url



if __name__ == '__main__':
    scraper = Scraper()

    # Create logs folder if it doesn't exists
    if not os.path.exists(scraper.storagePath + "logs"):
        os.makedirs(scraper.storagePath + "logs")

    # Log start of scraper
    logging.info("Starting Amazon Scraper")

    # make db amazon.db if it doesn't exist
    if not os.path.exists(scraper.storagePath + "amazon.db"):
        logging.info("Creating amazon.db")  
        db = AmazonDatabaseConnector()
        db.schemaMaker()
    
    