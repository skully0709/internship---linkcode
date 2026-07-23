import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#atharvad@322",
    database="linkcode"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resume(
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(200),
    file LONGBLOB,
    filetype VARCHAR(20)
)
""")

conn.commit()

print("1. Upload your resume\n2. Read data from resume\n3. Update your resume\n4. Delete your resume\n")

ch = int(input("Enter your choice: "))

match ch:

    case 1:
        path = input("Enter file path: ")

        with open(path, "rb") as file:
            data = file.read()

        filename = path.split("\\")[-1]
        extension = filename.split(".")[-1]

        cursor.execute(
            "INSERT INTO resume(filename, file, filetype) VALUES(%s, %s, %s)",
            (filename, data, extension)
        )

        conn.commit()
        print("Resume uploaded successfully.")

    case 2:
        id = int(input("Enter your id: "))

        cursor.execute(
            "SELECT filename, file, filetype FROM resume WHERE id=%s",
            (id,)
        )

        row = cursor.fetchone()

        if row:
            filename = row[0]
            filedata = row[1]
            filetype = row[2]

            with open(filename, "wb") as file:
                file.write(filedata)

            print("Resume downloaded successfully.")
            print("Filename :", filename)
            print("File Type :", filetype)

        else:
            print("ID not found.")

    case 3:
        id = int(input("Enter your id: "))
        path = input("Enter new file path: ")

        with open(path, "rb") as file:
            data = file.read()

        filename = path.split("\\")[-1]
        extension = filename.split(".")[-1]

        cursor.execute(
            "UPDATE resume SET filename=%s, file=%s, filetype=%s WHERE id=%s",
            (filename, data, extension, id)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Resume updated successfully.")
        else:
            print("ID not found.")

    case 4:
        id = int(input("Enter your id: "))

        cursor.execute(
            "DELETE FROM resume WHERE id=%s",
            (id,)
        )

        conn.commit()

        if cursor.rowcount > 0:
            print("Resume deleted successfully.")
        else:
            print("ID not found.")

    case _:
        print("Invalid choice.")

cursor.close()
conn.close()