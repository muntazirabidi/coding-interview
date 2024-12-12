import pandas as pd
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.connection = None
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return self.connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
        return None

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

class ProductManager:
    def __init__(self, connection):
        self.connection = connection

    def insert_product(self, product_name, price, stock_quantity):
        cursor = self.connection.cursor()
        insert_query = """INSERT INTO products (product_name, price, stock_quantity) 
                          VALUES (%s, %s, %s)"""
        cursor.execute(insert_query, (product_name, price, stock_quantity))
        self.connection.commit()
        print(f"{cursor.rowcount} record inserted.")

    def update_stock(self, product_id, new_quantity):
        cursor = self.connection.cursor()
        update_query = """UPDATE products SET stock_quantity = %s WHERE product_id = %s"""
        cursor.execute(update_query, (new_quantity, product_id))
        self.connection.commit()
        print(f"{cursor.rowcount} record updated.")

    def get_all_products(self):
        query = """SELECT * FROM products"""
        cursor = self.connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        df = pd.DataFrame(records, columns=['product_id', 'product_name', 'price', 'stock_quantity'])
        return df

# Usage
if __name__ == "__main__":
    db_connection = DatabaseConnection('localhost', 'grocery_store', 'yourusername', 'yourpassword')
    conn = db_connection.connect()
    
    if conn:
        product_manager = ProductManager(conn)
        
        # Add products
        product_manager.insert_product("Apple", 0.50, 100)
        product_manager.insert_product("Banana", 0.30, 150)

        # Update stock
        product_manager.update_stock(1, 95)  # Assuming first product inserted has ID 1

        # Retrieve all products
        products_df = product_manager.get_all_products()
        print(products_df)

        # Example of data manipulation with Pandas (sorting by price)
        sorted_df = products_df.sort_values('price', ascending=False)
        print(sorted_df)

        db_connection.close()