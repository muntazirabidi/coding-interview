import mysql.connector

class DatabaseConnection: 
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls_instance = super().__new__(cls)
      cls._instance._connection = mysql.connector.connect(
        host="localhost
        user="root",
        password="password"
        database="mydatabase"
      )
      
    return cls._instance
    
    def get_connection(self):
      return self._connection
      
    def __del__(self):
      if hasattr(self, '_connection'):
        self._connection.close()
        
        
        
db_connection = DatabaseConnection()
connection = db_connection.get_connection()
curor = connection.cursor()
cursor.execute("SELECT * FROM customers")
for user in cursor:
  print(user)