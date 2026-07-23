from db import get_connection
from student import Student
from user import User



def add_student():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter Student Name : ")
    age = int(input("Enter Student Age : "))
    email = input("Enter Student Email : ")

    obj = Student(name, age, email)

    query = "INSERT INTO student(name,age,email) VALUES(%s,%s,%s)"
    values = (obj.name, obj.age, obj.email)

    cursor.execute(query, values)
    conn.commit()

    print("Student Added Successfully.")

    cursor.close()
    conn.close()


def view_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()

    if rows:
        print("\n-----------------------------")
        print("ID\tNAME\tAGE\tEMAIL")
        print("-----------------------------")

        for row in rows:
            print(row[0], "\t", row[1], "\t", row[2], "\t", row[3])
    else:
        print("No Students Found.")

    cursor.close()
    conn.close()


def update_student():
    conn = get_connection()
    cursor = conn.cursor()

    id = int(input("Enter Student ID : "))
    name = input("Enter New Name : ")
    age = int(input("Enter New Age : "))
    email = input("Enter New Email : ")

    query = "UPDATE student SET name=%s, age=%s, email=%s WHERE id=%s"

    cursor.execute(query, (name, age, email, id))
    conn.commit()

    if cursor.rowcount > 0:
        print("Student Updated Successfully.")
    else:
        print("Student ID Not Found.")

    cursor.close()
    conn.close()


def delete_student():
    conn = get_connection()
    cursor = conn.cursor()

    id = int(input("Enter Student ID : "))

    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Student Deleted Successfully.")
    else:
        print("Student ID Not Found.")

    cursor.close()
    conn.close()



def add_user():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter Username : ")
    password = input("Enter Password : ")
    role = input("Enter Role(admin/user) : ")

    obj = User(username, password, role)

    query = "INSERT INTO login(username,password,role) VALUES(%s,%s,%s)"
    values = (obj.username, obj.password, obj.role)

    cursor.execute(query, values)
    conn.commit()

    print("User Added Successfully.")

    cursor.close()
    conn.close()


def view_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM login")
    rows = cursor.fetchall()

    if rows:
        print("\n----------------------------")
        print("ID\tUSERNAME\tROLE")
        print("----------------------------")

        for row in rows:
            print(row[0], "\t", row[1], "\t\t", row[3])
    else:
        print("No Users Found.")

    cursor.close()
    conn.close()


def update_user():
    conn = get_connection()
    cursor = conn.cursor()

    id = int(input("Enter User ID : "))
    username = input("Enter New Username : ")
    password = input("Enter New Password : ")
    role = input("Enter New Role : ")

    query = "UPDATE login SET username=%s,password=%s,role=%s WHERE id=%s"

    cursor.execute(query, (username, password, role, id))
    conn.commit()

    if cursor.rowcount > 0:
        print("User Updated Successfully.")
    else:
        print("User ID Not Found.")

    cursor.close()
    conn.close()


def delete_user():
    conn = get_connection()
    cursor = conn.cursor()

    id = int(input("Enter User ID : "))

    cursor.execute("DELETE FROM login WHERE id=%s", (id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("User Deleted Successfully.")
    else:
        print("User ID Not Found.")

    cursor.close()
    conn.close()