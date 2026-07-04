import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sarthak@123",
    database="linkcode"
)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS emp (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT check (age >= 18),
        department VARCHAR(100)
    )
''')
conn.commit()

print("Table created")