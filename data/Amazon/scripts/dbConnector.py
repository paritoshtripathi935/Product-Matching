import sqlite3
import os

class AmazonDatabaseConnector:
    def __init__(self, stamp):
        self.dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../amazon.db")
        self.conn = sqlite3.connect(self.dbPath)
        self.cur = self.conn.cursor()
        self.welcomeMessage = "Welcome to Amazon Scraper. This is the database for the Amazon Scraper. This database was created on {}.".format(stamp)

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