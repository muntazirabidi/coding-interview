import sqlite3

conn = sqlite3.connect('customer.db')

c = conn.cursor()

#c.execute("CREATE TABLE customers (first_name TEXT, last_name TEXT, email TEXT)")

#many_customers = [
#  ('Wes', 'Brown', 'wes@brown.com'),
#  ('Steph', 'Kuewa', 'steph@kuewa.com'),
#  ('Dan', 'Pas', 'dan@pas.com')
#]
#c.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)

c.execute("SELECT * FROM customers")
#c.fetchone()
#c.fetchmany(3)
items = c.fetchall()
for item in items:
  print(item)

print("Command executed successfully...")

conn.commit()

conn.close()