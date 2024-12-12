import mysql.connector
import pandas as pd
from mysql.connector import Error

class MySQLQuerySystem:
    def __init__(self, host_name, user_name, user_password, db_name):
        self.connection = self.create_connection(host_name, user_name, user_password, db_name)
        self.cursor = None

    def create_connection(self, host_name, user_name, user_password, db_name):
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("Connection to MySQL DB successful")
            return connection
        except Error as err:
            print(f"Error: '{err}'")
            return None

    def execute_query(self, query):
        if self.connection is None:
            raise ConnectionError("No database connection established.")
        
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: '{e}'")
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def query_to_dataframe(self, query, columns):
        results = self.execute_query(query)
        if results:
            return pd.DataFrame(results, columns=columns)
        return pd.DataFrame()

    def update_db(self, df, table_name, id_column='id'):
        if self.connection is None:
            raise ConnectionError("No database connection established.")
        
        try:
            self.cursor = self.connection.cursor()
            for i, row in df.iterrows():
                sql = f"UPDATE {table_name} SET " + \
                      ", ".join([f"{col} = %s" for col in df.columns if col != id_column]) + \
                      f" WHERE {id_column} = %s"
                self.cursor.execute(sql, tuple(row))
            self.connection.commit()
        except Error as e:
            print(f"Error updating database: '{e}'")
        finally:
            if self.cursor:
                self.cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

# Usage example
if __name__ == "__main__":
    query_system = MySQLQuerySystem("localhost", "your_username", "your_password", "your_database")

    if query_system.connection:
        # Example query to get data
        query = "SELECT id, column1, column2 FROM your_table_name"
        df = query_system.query_to_dataframe(query, ['id', 'column1', 'column2'])

        # Data manipulation
        filtered_df = df[df['column1'] > 10]
        grouped = df.groupby('column2').agg({'column1': ['mean', 'count']})
        sorted_df = df.sort_values(by='column1', ascending=False)
        
        print(filtered_df)
        print(grouped)
        print(sorted_df)

        # Example of updating the database
        # query_system.update_db(filtered_df, 'your_table_name')

        query_system.close_connection()
    else:
        print("Failed to connect to database")