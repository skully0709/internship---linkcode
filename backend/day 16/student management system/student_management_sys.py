import sqlite3
from generate_pdf import generate_pdf
from send_email import send_email
conn=sqlite3.connect("student_management_sys.db")
cursor=conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                Roll_No integer PRIMARY KEY,
                Name text not null,
                Age integer,
                Marathi_Marks integer,
                English_Marks integer,
                Maths_Marks integer,
                Science_Marks integer,
                Economics_Marks integer
            )
''')

# cursor.executemany(
#     "insert into student values (?, ?, ?, ?, ?, ?, ?, ?)",
#         [(1, 'Aarav', 19, 85, 78, 92, 88, 80),
#         (2, 'Diya', 18, 90, 84, 87, 91, 86),
#         (3, 'Vivaan', 20, 76, 82, 79, 85, 81),
#         (4, 'Ananya', 25, 95, 89, 94, 93, 90),
#         (5, 'Aditya', 14, 68, 75, 72, 70, 74),
#         (6, 'Isha', 15, 88, 91, 85, 89, 87),
#         (7, 'Krishna', 16, 79, 77, 83, 81, 78),
#         (8, 'Meera', 17, 92, 94, 90, 95, 93),
#         (9, 'Rohan', 18, 71, 69, 74, 73, 70),
#         (10, 'Saanvi', 19, 87, 86, 89, 88, 85)
#          ]
# )
# conn.commit()
ch=0
while ch!=8:
    print("---------------------------------------")
    print("1.Add Student\n2.Update existing students\n3.view entire list of students\n4.Search the student\n5.Delete the student\n6.View result of the student\n7.View final report\n8.Exit")
    print("---------------------------------------")
    ch=int(input("Enter your choice:"))
    print("---------------------------------------")
    match ch:
        case 1:
            print("Enter the details of the student:")
            roll_no=int(input("Enter Roll No:"))
            name=input("Enter Name:")
            age=int(input("Enter Age:"))
            marathi_marks=int(input("Enter Marathi Marks:"))
            english_marks=int(input("Enter English Marks:"))
            maths_marks=int(input("Enter Maths Marks:"))
            science_marks=int(input("Enter Science Marks:"))
            economics_marks=int(input("Enter Economics Marks:"))
            cursor.execute("insert into student(Roll_No,Name,Age,Marathi_Marks,English_Marks,Maths_Marks,Science_Marks,Economics_Marks) values (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    roll_no,
                    name,
                    age,
                    marathi_marks,
                    english_marks,
                    maths_marks,
                    science_marks,
                    economics_marks
                )
            )

            conn.commit()
            print("---------------------------------------")
            print("Student added successfully!")
            print("---------------------------------------")
        case 2:
            print("\n1. update any column of a single student")
            print("2. update same column for multiple students")
            print("3. update entire column of database")

            
            choice = int(input("enter your choice: "))

            columns = [
                "name",
                "age",
                "marathi_marks",
                "english_marks",
                "maths_marks",
                "science_marks",
                "economics_marks"
            ]

            if choice == 1:
                
                roll = input("enter roll no: ")

                cursor.execute(
                    "select * from student where roll_no=?",
                    (roll,)
                )

                if cursor.fetchone():

                    col = input(
                        "enter column name: "
                    ).lower()

                    if col in columns:

                        value = input(f"enter new value for {col}: ")

                        cursor.execute(
                            f"update student set {col}=? where roll_no=?",
                            (value, roll)
                        )

                        conn.commit()
                        print("record updated successfully!")

                    else:
                        print("invalid column name")

                else:
                    print("student not found")

            elif choice == 2:

                col = input(
                    "enter column name: "
                ).lower()

                if col in columns:

                    n = int(
                        input("how many students do you want to update: ")
                    )

                    for i in range(n):

                        roll = input(
                            f"enter roll no of student {i+1}: "
                        )

                        cursor.execute(
                            "select * from student where roll_no=?",
                            (roll,)
                        )

                        if cursor.fetchone():

                            value = input(
                                f"enter new value for {col}: "
                            )

                            cursor.execute(
                                f"update student set {col}=? where roll_no=?",
                                (value, roll)
                            )

                        else:
                            print(
                                f"student with roll no {roll} not found"
                            )

                    conn.commit()
                    print("records updated successfully!")

                else:
                    print("invalid column name")

            elif choice == 3:

                col = input(
                    "enter column name: "
                ).lower()

                if col in columns:

                    value = input(
                        f"enter new value for all students in {col}: "
                    )

                    confirm = input(
                        "are you sure? (y/n): "
                    )

                    if confirm.lower() == "y":

                        cursor.execute(
                            f"update student set {col}=?",
                            (value,)
                        )

                        conn.commit()
                        print(
                            f"all values of {col} updated successfully!"
                        )

                    else:
                        print("update cancelled")

                else:
                    print("invalid column name")

            else:
                print("invalid choice")
            

        case 3:
            cursor.execute("select * from student")
            row=cursor.fetchall()
            print("\nEntire List of Students")
            print("-" * 95)

            print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'Marathi':<10}{'English':<10}{'Maths':<10}{'Science':<10}{'Economics':<10}")

            print("-" * 95)

            for i in row:
                print(f"{i[0]:<10}{i[1]:<15}{i[2]:<8}{i[3]:<10}{i[4]:<10}{i[5]:<10}{i[6]:<10}{i[7]:<10}")

            print("-" * 95)
        case 4:
            search = input("Enter Roll No or Name of the student to search: ")

            cursor.execute(
                    "select * from student where Roll_No=? or Name=?",(search,search))


            row = cursor.fetchall()

            if row:
                print("\nStudent Found")
                print("-" * 95)
                print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'Marathi':<10}{'English':<10}{'Maths':<10}{'Science':<10}{'Economics':<10}")
                print("-" * 95)

                for i in row:
                    print(f"{i[0]:<10}{i[1]:<15}{i[2]:<8}{i[3]:<10}{i[4]:<10}{i[5]:<10}{i[6]:<10}{i[7]:<10}")

                print("-" * 95)

            else:
                print("No student found.")
        case 5:
            ch = int(input("Enter how many students do you want to delete: "))

            for i in range(ch):
                search = input(f"Enter Roll No or Name of student {i+1} to delete: ")

                cursor.execute(
                        "select * from student where Roll_No=? or Name=?",(search,search))


                row = cursor.fetchone()

                if row:
                    cursor.execute(
                        "DELETE FROM student WHERE Roll_No = ? OR Name = ?",
                        (search, search)
                    )
                    print(f"Student '{search}' deleted successfully!")
                else:
                    print(f"Student '{search}' not found!")
            conn.commit()
        case 6:
            ch = int(input("How many reports of students do you want to see: "))

            for i in range(ch):
                search = input(f"Enter Roll No or Name of student {i+1} to view his/her report: ")

                cursor.execute(
                        "select * from student where Roll_No=? or Name=?",(search,search))

                row = cursor.fetchone()

                if row:
                    print("-" * 95)
                    print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'Marathi':<10}{'English':<10}{'Maths':<10}{'Science':<10}{'Economics':<10}")
                    print("-" * 95)

                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<8}{row[3]:<10}{row[4]:<10}{row[5]:<10}{row[6]:<10}{row[7]:<10}")

                    total = row[3] + row[4] + row[5] + row[6] + row[7]
                    percentage = total / 5

                    if (row[3] >= 35 and row[4] >= 35 and row[5] >= 35 and
                        row[6] >= 35 and row[7] >= 35):
                        result = "PASS"
                    else:
                        result = "FAIL"

                    print("-" * 95)
                    print(f"Total Marks : {total}/500")
                    print(f"Percentage  : {percentage:.2f}%")
                    print(f"Result      : {result}")
                    print("-" * 95)

                    print("1.Download this report\n2.send to an Email")
                    ch=int(input("Enter your choice"))
                    if ch==1: 
                        generate_pdf(row, total, percentage, result)

                    elif ch == 2:

                        filename = f"report_{row[0]}.pdf"

                        generate_pdf(row, total, percentage, result)

                        email = input("Enter receiver email: ")

                        send_email(email, filename)

                    else:
                        print("Invalid choice")
                else:
                    print("No student found.")
        case 7:
            
            print("Final report of all students:")
            cursor.execute("select * from student")
            rows=cursor.fetchall()
            print(f"{'Roll No':<10}{'Name':<15}{'grade':<10}")
            for i in rows:
                if (i[3] >= 35 and i[4] >= 35 and i[5] >= 35 and
                    i[6] >= 35 and i[7] >= 35):
                    grade = "PASS"
                else:
                    grade = "FAIL"
                print(f"{i[0]:<10}{i[1]:<15}{grade:<8}")
        case 8:
            print("Exiting....")        


