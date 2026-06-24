try:
    f = open("MyFile.txt","x")
    print(f)
except Exception as e:
    print(e)

with open("MyFile.txt","w") as f:
    f.write("Hello Darkness My Old Friend")

with open("MyFile.txt","r") as f:
    print(f.read())

with open("MyFile.txt","a") as f:
    f.write("\nive come to talk with you again")

with open("MyFile.txt","r") as f:
    print(f.read())