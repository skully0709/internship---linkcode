import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="#atharvad@322",
    database="linkcode"
)

print("db connected")
cursor=conn.cursor()

# cursor.execute('''
#     CREATE TABLE images (
#         id INTEGER PRIMARY KEY,
#         filename VARCHAR(20),
#         filedata BLOB
#     )
# ''')

# file=open("img.webp","rb")
# data=file.read()
# print(data)
# file.close()
# query="INSERT INTO images(id,filename,filedata) values(%s,%s,%s)"
# values=(1,"img.png",data)
# cursor.execute(query,values)
# conn.commit()

cursor.execute("SELECT * FROM images where id=%s",(1,))
row=cursor.fetchone()

if row:
    filename=row[1]
    filedata=row[2]

    file=open(filename,"wb")
    file.write(filedata)
    print("Downloaded..")
    file.close()
else:
    print("image does't exists")