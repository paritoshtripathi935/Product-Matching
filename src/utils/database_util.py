# connect with the database
import sqlite3
import os
import sys
import time
import datetime

class DatabaseUtils:
    def __init__(self, database: str):
        self.database = database
        self.stats = {}
    
    def connect(self, db_name: str):
        if not os.path.exists(db_name):
            print(f"The database {db_name} does not exist")
            sys.exit(1)
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        return cursor

    def generate_stats(self):
        cursor = self.connect(self.database)
        cursor.execute("SELECT COUNT(DISTINCT sku) FROM products")
        products = cursor.fetchall()
        self.stats["products"] = products[0][0]
        return self.stats



