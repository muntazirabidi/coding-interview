# test_mysql.py
import sys
print(f"Using Python from: {sys.executable}")

try:
    import mysql.connector
    print("MySQL Connector version:", mysql.connector.__version__)
    
    # Try to make a connection to verify the installation
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password'  # Replace with your actual password
    )
    
    if connection.is_connected():
        server_info = connection.get_server_info()
        print(f"Connected to MySQL Server version {server_info}")
        
        # Get cursor and database information
        cursor = connection.cursor()
        cursor.execute("select database();")
        database = cursor.fetchone()
        print("Current database:", database)
        
        # Clean up
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        
except ImportError as e:
    print("Import Error Details:")
    print(f"Error message: {str(e)}")
    print("\nPython path:")
    for path in sys.path:
        print(f"- {path}")
    
except mysql.connector.Error as err:
    print(f"MySQL Connection Error: {err}")
    print("Error Code:", err.errno)
    print("SQLSTATE:", err.sqlstate)
    print("Error Message:", err.msg)