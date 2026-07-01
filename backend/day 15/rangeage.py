import sqlite3

conn = sqlite3.connect("E:\SARTHAK/assignment\internship - linkcode/backend\day 15/studentdb.db")

cursor = conn.cursor()

cursor.execute('''

    create table if not exists stud2(
               id integer primary key,
               name varchar2(50) not null,
               age integer 
               )
               '''
               )
print("Table created")

cursor.executemany("insert into stud2(id,name,age) values(?,?,?)",((1,"Ram",34),(2,"Shyam",23),(3,"Shubham",13),(4,"Sarthak",21),(5,"Atharva",17)))

cursor.execute("select name from stud2 where age between 18 and 25")
rows = cursor.fetchall()

print("Names of student between the age 18 and 25 are: ")
for i in rows:
    print(i[0])


