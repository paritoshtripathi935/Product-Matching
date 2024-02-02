# connect with the database
import sqlite3
import os
import sys
import time
import datetime

def connect(db_name: str):
    # check if the database exists
    if not os.path.exists(db_name):
        print(f"The database {db_name} does not exist")
        sys.exit(1)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return cursor

def generate_stats(database: str):
    stats = {}
    cursor = connect(database)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    stats["tables"] = tables
    print(f"Tables in the database: {tables}")
    
        
    cursor.execute("SELECT COUNT(DISTINCT sku) FROM products")
    products = cursor.fetchall()
    print(f"Total unique products: {products[0][0]}")
    stats["products"] = products[0][0]
    
    return stats


