# Flipkart Scraper

import os
import logging
from datetime import datetime

class Scraper:
    def __init__(self):
        self.stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 
        self.storagePath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../"
        )
        logging.basicConfig(
            filename=self.storagePath + "logs/FlipkartScraper_{}.log".format(self.stamp),
            level=logging.INFO,
            filemode="w",
        )





if __name__ == '__main__':
    scraper = Scraper()