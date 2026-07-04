import sqlite3
from generate_pdf import generate_pdf
from send_email import send_email

conn = sqlite3.connect("E:\\SARTHAK\\assignment\\internship - linkcode\\backend\\day 16\\student management system\\smdb.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        roll_No integer PRIMARY KEY,
        name text not null,
        age integer,
        dCN_marks integer,
        jpr_marks integer,
        mic_marks integer,
        pwp_marks integer,
        uid_marks integer
    )
''')
conn.commit()

try:
    cursor.executemany(
        "insert into student values (?, ?, ?, ?, ?, ?, ?, ?)",
            [(1, 'Pranav', 17, 82, 79, 85, 88, 81),
            (2, 'Myra', 19, 94, 91, 96, 93, 95),
            (3, 'Shaurya', 15, 67, 72, 70, 65, 68),
            (4, 'Anika', 18, 88, 85, 89, 91, 87),
            (5, 'Aravind', 21, 75, 78, 73, 76, 74),
            (6, 'Riya', 16, 91, 93, 90, 94, 92),
            (7, 'Karan', 20, 62, 59, 65, 61, 64),
            (8, 'Tanvi', 14, 85, 87, 83, 86, 89),
            (9, 'Vivaan', 22, 79, 81, 77, 80, 78),
            (10, 'Ipshita', 19, 95, 97, 94, 96, 98)]
    )
except Exception as e:
    print(e)
conn.commit()

ch = 0
while ch != 8:
    print("---------------------------------------")
    print("1. Add Student\n2. Update Existing Students\n3. View Entire List of Students\n4. Search the Student\n5. Delete the Student\n6. View Result of the Student\n7. View Final Report\n8. Exit")
    print("---------------------------------------")
    ch = int(input("Enter your choice: "))
    print("---------------------------------------")
    
    match ch:
        case 1:
            print("Enter the details of the student:")
            roll_no = int(input("Enter Roll No: "))
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            dcn_marks = int(input("Enter DCN Marks: "))
            jpr_marks = int(input("Enter JPR Marks: "))
            mic_marks = int(input("Enter MIC Marks: "))
            pwp_marks = int(input("Enter PWP Marks: "))
            uid_marks = int(input("Enter UID Marks: "))
            
            cursor.execute(
                "insert into student(Roll_No, Name, Age, DCN_marks, JPR_marks, MIC_marks, PWP_marks, UID_marks) values (?, ?, ?, ?, ?, ?, ?, ?)",
                (roll_no, name, age, dcn_marks, jpr_marks, mic_marks, pwp_marks, uid_marks)
            )
            conn.commit()
            print("---------------------------------------")
            print("Student added successfully!")
            print("---------------------------------------")
            
        case 2:
            print("\n1. Update any column of a single student")
            print("2. Update same column for multiple students")
            print("3. Update entire column of database")
            
            choice = int(input("Enter your choice: "))
            columns = ["name", "age", "dcn_marks", "jpr_marks", "mic_marks", "pwp_marks", "uid_marks"]

            if choice == 1:
                roll = input("Enter Roll No: ")
                cursor.execute("select * from student where Roll_No=?", (roll,))
                
                if cursor.fetchone():
                    col = input("Enter column name: ").lower()
                    if col in columns:
                        value = input(f"Enter new value for {col.capitalize()}: ")
                        cursor.execute(f"update student set {col}=? where Roll_No=?", (value, roll))
                        conn.commit()
                        print("Record updated successfully!")
                    else:
                        print("Invalid column name")
                else:
                    print("Student not found")

            elif choice == 2:
                col = input("Enter column name: ").lower()
                if col in columns:
                    n = int(input("How many students do you want to update: "))
                    for i in range(n):
                        roll = input(f"Enter Roll No of student {i+1}: ")
                        cursor.execute("select * from student where Roll_No=?", (roll,))
                        
                        if cursor.fetchone():
                            value = input(f"Enter new value for {col.capitalize()}: ")
                            cursor.execute(f"update student set {col}=? where Roll_No=?", (value, roll))
                        else:
                            print(f"Student with Roll No {roll} not found")
                    conn.commit()
                    print("Records updated successfully!")
                else:
                    print("Invalid column name")

            elif choice == 3:
                col = input("Enter column name: ").lower()
                if col in columns:
                    value = input(f"Enter new value for all students in {col.capitalize()}: ")
                    confirm = input("Are you sure? (y/n): ")
                    if confirm.lower() == "y":
                        cursor.execute(f"update student set {col}=?", (value,))
                        conn.commit()
                        print(f"All values of {col.capitalize()} updated successfully!")
                    else:
                        print("Update cancelled")
                else:
                    print("Invalid column name")
            else:
                print("Invalid choice")
            
        case 3:
            cursor.execute("select * from student")
            row = cursor.fetchall()
            print("\nEntire List of Students")
            print("-" * 95)
            print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'DCN':<10}{'JPR':<10}{'MIC':<10}{'PWP':<10}{'UID':<10}")
            print("-" * 95)
            for i in row:
                print(f"{i[0]:<10}{i[1]:<15}{i[2]:<8}{i[3]:<10}{i[4]:<10}{i[5]:<10}{i[6]:<10}{i[7]:<10}")
            print("-" * 95)
            
        case 4:
            search = input("Enter Roll No or Name of the student to search: ")
            cursor.execute("select * from student where Roll_No=? or Name=?", (search, search))
            row = cursor.fetchall()

            if row:
                print("\nStudent Found")
                print("-" * 95)
                print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'DCN':<10}{'JPR':<10}{'MIC':<10}{'PWP':<10}{'UID':<10}")
                print("-" * 95)
                for i in row:
                    print(f"{i[0]:<10}{i[1]:<15}{i[2]:<8}{i[3]:<10}{i[4]:<10}{i[5]:<10}{i[6]:<10}{i[7]:<10}")
                print("-" * 95)
            else:
                print("No student found.")
                
        case 5:
            ch_del = int(input("Enter how many students do you want to delete: "))
            for i in range(ch_del):
                search = input(f"Enter Roll No or Name of student {i+1} to delete: ")
                cursor.execute("select * from student where Roll_No=? or Name=?", (search, search))
                row = cursor.fetchone()

                if row:
                    cursor.execute("DELETE FROM student WHERE Roll_No = ? OR Name = ?", (search, search))
                    print(f"Student '{search}' deleted successfully!")
                else:
                    print(f"Student '{search}' not found!")
            conn.commit()
            
        case 6:
            ch_rep = int(input("How many reports of students do you want to see: "))
            for i in range(ch_rep):
                search = input(f"Enter Roll No or Name of student {i+1} to view his/her report: ")
                cursor.execute("select * from student where Roll_No=? or Name=?", (search, search))
                row = cursor.fetchone()

                if row:
                    print("-" * 95)
                    print(f"{'Roll No':<10}{'Name':<15}{'Age':<8}{'DCN':<10}{'JPR':<10}{'MIC':<10}{'PWP':<10}{'UID':<10}")
                    print("-" * 95)
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<8}{row[3]:<10}{row[4]:<10}{row[5]:<10}{row[6]:<10}{row[7]:<10}")

                    total = row[3] + row[4] + row[5] + row[6] + row[7]
                    percentage = total / 5

                    if (row[3] >= 35 and row[4] >= 35 and row[5] >= 35 and row[6] >= 35 and row[7] >= 35):
                        result = "PASS"
                    else:
                        result = "FAIL"

                    print("-" * 95)
                    print(f"Total Marks : {total}/500")
                    print(f"Percentage  : {percentage:.2f}%")
                    print(f"Result      : {result}")
                    print("-" * 95)

                    print("1. Download this report\n2. Send to an Email")
                    ch_opt = int(input("Enter your choice: "))
                    if ch_opt == 1: 
                        generate_pdf(row, total, percentage, result)
                    elif ch_opt == 2:
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
            rows = cursor.fetchall()
            print(f"{'Roll No':<10}{'Name':<15}{'Grade':<10}")
            for i in rows:
                if (i[3] >= 35 and i[4] >= 35 and i[5] >= 35 and i[6] >= 35 and i[7] >= 35):
                    grade = "PASS"
                else:
                    grade = "FAIL"
                print(f"{i[0]:<10}{i[1]:<15}{grade:<8}")
                
        case 8:
            print("Exiting....")

conn.close()