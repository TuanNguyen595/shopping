import sqlite3
from datetime import datetime

class Model:
  def __init__(self):
    self.conn = sqlite3.connect('tap_hoa.db')
    self.cursor = self.conn.cursor()
    self.createTable()
  def createTable(self):
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS item (
          item_id INTEGER PRIMARY KEY AUTOINCREMENT,
          item_name TEXT NOT NULL,
          price REAL NOT NULL,
          imported_price REAL NOT NULL,
          stock INTEGER NOT NULL
        )
      ''')
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS ordered_items (
        items_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY(item) REFERENCES item(item_id)
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
      )
    ''')
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        birthday DATE,
        id_card TEXT,
        resident_address TEXT,
        department TEXT,
        phone_number TEXT
        debt REAL
      )
    ''')
    self.cursor.execute('''
      CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
      )
    ''')
    self.conn.commit()


