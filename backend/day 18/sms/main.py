from crud import *
from db import get_connection


def login():

    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter Username : ")
    password = input("Enter Password : ")

    cursor.execute(
        "SELECT * FROM login WHERE username=%s AND password=%s",
        (username, password)
    )

    row = cursor.fetchone()

    if row is None:
        print("Invalid Username or Password")
        return

    print("Login Successful")

    role = row[3]

    if role == "admin":

        while True:

            print("""
                    ========== ADMIN MENU ==========
                    1. Add User
                    2. Add Student
                    3. View Students
                    4. Update Student
                    5. Delete Student
                    6. View Users
                    7. Update User
                    8. Delete User
                    9. Exit
                    """)

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    add_user()

                case 2:
                    add_student()

                case 3:
                    view_students()

                case 4:
                    update_student()

                case 5:
                    delete_student()

                case 6:
                    view_users()

                case 7:
                    update_user()

                case 8:
                    delete_user()

                case 9:
                    print("Thank You...")
                    break

                case _:
                    print("Invalid Choice")

    elif role == "user":

        while True:

            print("""
                    ========== USER MENU ==========
                    1. View Students
                    2. Exit
                    """)

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    view_students()

                case 2:
                    print("Thank You...")
                    break

                case _:
                    print("Invalid Choice")

    cursor.close()
    conn.close()


login()