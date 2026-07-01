import sqlite3

conn = sqlite3.connect("E:\SARTHAK/assignment\internship - linkcode/backend\day 15/studentdb.db")

cursor = conn.cursor()

cursor.execute('''

    create table if not exists stud(
               id integer primary key,
               name varchar2(50) not null,
               age integer 
               )
               '''
               )
print("Table created")

id = int(input("Enter id: "))
name = input("Enter name: ")
age = int(input("Enter age: "))
try:
    cursor.execute("insert into stud(id,name,age) values(?,?,?)",(id,name,age))
    print("Data inserted")
except Exception as e:
    print(e)  
conn.commit()

cursor.execute("select * from stud")
rows = cursor.fetchall()

for i in rows:

    print("---------------------------------")
    print("Sid: ", i[0])
    print("Name: ", i[1])
    print("Age: ",i[2])

print("---------------------------------")
id = int(input("Enter the id to fetch: "))

cursor.execute("Select * from stud where id=?",(id,))
row = cursor.fetchone()

print("---------------------------------")
print("Sid: ", row[0])
print("Name: ",row[1])
print("Age: ",row[2])

print("")
print("---------------------------------")

id = int(input("Enter the id to update: "))
name = input("Enter name to update: ")
age = int(input("Enter age to update: "))

cursor.execute("update stud set name=?,age=? where id=?",(name,age,id))
print("Table updated")
conn.commit()


