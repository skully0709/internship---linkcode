user = input("Enter username: ")
password = input("Enter password: ")

if user == "ADMIN":

    if password=="PASS":
        print("Login successful")
    else:
        print("Password incorrect")

else:
    print("Username not found")
    