import sqlite3
import os

class AmazonDatabaseConnector:
    def __init__(self):
        self.dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../amazon.db")
        self.conn = sqlite3.connect(self.dbPath)
        self.cur = self.conn.cursor()

    def schemaMaker(self):
        self.cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, image_path TEXT NOT NULL, category TEXT NOT NULL);")
        self.cur.execute("CREATE TABLE product_matches (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL, match_id INTEGER NOT NULL, FOREIGN KEY (product_id) REFERENCES products(id), FOREIGN KEY (match_id) REFERENCES products(id));")
        self.conn.commit()