from db import cursor, conn

def insertemp(name, age, department):
    cursor.execute("INSERT INTO emp (name, age, department) VALUES (%s, %s, %s)", (name, age, department))
    conn.commit()
    print("Employee inserted")