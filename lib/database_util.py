import sqlite3
import os
import sys

class DatabaseUtil:
    def __init__(self, stamp, database_name):
        self.dbPath = "data/{}.db".format(database_name)
        self.conn, self.cur = self.connect(self.dbPath)
        self.welcomeMessage = f"Welcome to {database_name} Scraper. This is the database for the {database_name} Scraper. This database was created on {stamp}."

    def schemaMaker(self):
        # creating tables
        self.cur.execute("""CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            image_path TEXT NOT NULL,
            category TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            URL TEXT NOT NULL,
            price TEXT NOT NULL
        );""")
        self.conn.commit()
        self.cur.execute("CREATE TABLE product_matches (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, product_sku INTEGER NOT NULL, match_id INTEGER NOT NULL, match_sku INTEGER NOT NULL);")
        self.conn.commit()
    
    def insertProduct(self, productDetails):
        self.cur.execute("INSERT INTO products (sku, name, description, image_path, category, timestamp, URL, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (productDetails["sku"], productDetails["name"], productDetails["description"], productDetails["image_path"], productDetails["category"], productDetails["timestamp"], productDetails["URL"], productDetails["price"]))
        self.conn.commit()

    def fetchAllProducts(self):
        self.cur.execute("SELECT * FROM products")
        return self.cur.fetchall()

    def clearDatabase(self):
        self.cur.execute("DELETE FROM products")
        self.conn.commit()
        self.cur.execute("DELETE FROM product_matches")
        self.conn.commit()
    
    def removeDuplicates(self):
        self.cur.execute("DELETE FROM products WHERE rowid NOT IN (SELECT MIN(rowid) FROM products GROUP BY sku)")
        self.conn.commit()
    
    def convertDBtoCsv(self):
        self.cur.execute("SELECT * FROM products")
        with open('products.csv', 'w') as f:
            for row in self.cur:
                f.write(str(row))
                f.write(' ')
        self.conn.commit()
    
    def connect(self, db_name: str):
        if not os.path.exists(db_name):
            print(f"The database {db_name} does not exist")
            sys.exit(1)
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        return conn, cursor

    def generate_stats(self):
        cursor = self.connect(self.database)
        cursor.execute("SELECT COUNT(DISTINCT sku) FROM products")
        products = cursor.fetchall()
        self.stats["products"] = products[0][0]
        return self.stats
