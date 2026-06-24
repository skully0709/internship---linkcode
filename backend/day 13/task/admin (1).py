from login import Login

class admin(Login):
    def __init__(self,Email,pwd):
        self.email=Email
        self.pwd=pwd

    def authentication(self,email_id,pas):
        if self.email==email_id and self.pwd==pas:
            print("Login Successfull")
        else:
            print("Login Unsuccessfull")

obj=admin("atharva@gmail.com",123)
email=input("Enter your Email id:")
pas=int(input("Enter your Password:"))
obj.authentication(email,pas)
