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
  def addItem(self, item_name, price, imported_price, stock):
    self.cursor.execute("INSERT INTO item (item_name, price, imported_price, stock) VALUES (?, ?, ?, ?)", (item_name, price, imported_price, stock))
    self.conn.commit()
    return self.cursor.lastrowid
  def addOrder(self, customer_id, order_date, total_amount):
    self.cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)", (customer_id, order_date, total_amount))
    self.conn.commit()
    return self.cursor.lastrowid
  def addOrderItem(self, order_id, item_id, quantity):
    self.cursor.execute("INSERT INTO ordered_items (order_id, item, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
    self.conn.commit()
    return self.cursor.lastrowid
  def close(self):
    self.conn.close()
  def getItemById(self, item_id):
    self.cursor.execute("SELECT * FROM item WHERE item_id = ?", (item_id,))
    return self.cursor.fetchone()
  def getOrderById(self, order_id):
    self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    return self.cursor.fetchone()
  def getCustomerById(self, customer_id):
    self.cursor.execute("SELECT * FROM customer WHERE customer_id = ?", (customer_id,))
    return self.cursor.fetchone()
  def getOrderedItemsByOrderId(self, order_id):
    self.cursor.execute("SELECT * FROM ordered_items WHERE order_id = ?", (order_id,))
    return self.cursor.fetchall()
  def getOrdersByCustomerId(self, customer_id):
    self.cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,))
    return self.cursor.fetchall()
  def getItemsByOrderId(self, order_id):
    self.cursor.execute("SELECT * FROM ordered_items WHERE order_id = ?", (order_id,))
    return self.cursor.fetchall()
  def getOrderByDate(self, order_date):
    self.cursor.execute("SELECT * FROM orders WHERE order_date = ?", (order_date,))
    return self.cursor.fetchall()
  def getOrdersByDate(self, start_date, end_date):
    self.cursor.execute("SELECT * FROM orders WHERE order_date BETWEEN ? AND ?", (start_date, end_date))
    return self.cursor.fetchall()
  def getItemByName(self, item_name):
    self.cursor.execute("SELECT * FROM item WHERE item_name = ?", (item_name,))
    return self.cursor.fetchone()
  def getCustomerByName(self, name):
    self.cursor.execute("SELECT * FROM customer WHERE name = ?", (name,))
    return self.cursor.fetchone()
  def getCustomerByIdCard(self, id_card):
    self.cursor.execute("SELECT * FROM customer WHERE id_card = ?", (id_card,))
    return self.cursor.fetchone()
  def getCustomerByPhoneNumber(self, phone_number):
    self.cursor.execute("SELECT * FROM customer WHERE phone_number = ?", (phone_number,))
    return self.cursor.fetchone()
  def getCustomerByDebt(self):
    self.cursor.execute("SELECT * FROM customer WHERE debt > ?", (0,))
    return self.cursor.fetchall()
  def changeItemStock(self, item_id, new_stock):
    self.cursor.execute("UPDATE item SET stock = ? WHERE item_id = ?", (new_stock, item_id))
    self.conn.commit()
  def changeItemPrice(self, item_id, new_price):
    self.cursor.execute("UPDATE item SET price = ? WHERE item_id = ?", (new_price, item_id))
    self.conn.commit()
  def changeItemImportedPrice(self, item_id, new_imported_price):
    self.cursor.execute("UPDATE item SET imported_price = ? WHERE item_id = ?", (new_imported_price, item_id))
    self.conn.commit()
  def removeItemById(self, item_id):
    self.cursor.execute("DELETE FROM item WHERE item_id = ?", (item_id,))
    self.conn.commit()
  def removeOrderById(self, order_id):
    self.cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    self.conn.commit()
  def removeCustomerById(self, customer_id):
    self.cursor.execute("DELETE FROM customer WHERE customer_id = ?", (customer_id,))
    self.conn.commit()
  def removeOrderItemsByOrderId(self, order_id):
    self.cursor.execute("DELETE FROM ordered_items WHERE order_id = ?", (order_id,))
    self.conn.commit()


