import logging
import os
from datetime import datetime
import lxml.html as html
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class htmlLib:
    def __init__(self, timeout=10):
        self.stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.storagePath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../"
        )
        
    def get_xpath_link(self, doc, xpath, website):
        try:
            name = doc.xpath("".join(xpath))
            print(name)
            for i in range(len(name)):
                if name[i].startswith("/"):
                    name[i] = website + name[i]
                else:
                    name[i] = name[i]
            return name

        except Exception as e:
            logging.info("Error in getting {}: {}".format(name, e))
            pass
            return None
            pass
        
    def get_xpath_data(self, doc, xpath):
        try:
            name = doc.xpath(xpath)
            return name

        except Exception as e:
            print("Error in getting {}: {}".format(name, e))
            pass
            return None
        
    def data_storage(self, df_list, unique_id, name):
        df_combined = pd.concat(df_list, ignore_index=True)
        df_combined.drop_duplicates(subset=unique_id, inplace=True)
        df_combined.to_csv(
            self.storagePath + "raw/" + "{}_{}.csv".format(name, self.stamp),
            index=False,
        )
      
    def cleanData(self, array):
        array = [x.strip() for x in array]
        array = list(filter(None, array))
        array = [x.encode("ascii", "ignore").decode() for x in array]
        array = [x.replace("\n", "") for x in array]
        return array
    
    