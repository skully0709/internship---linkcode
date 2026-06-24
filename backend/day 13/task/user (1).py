from login import Login

class user(Login):
    def __init__(self,username,pwd):
        self.username=username
        self.pwd=pwd

    def authentication(self):
        self.user=input("Enter your username:")
        self.pas=int(input("Enter your password:"))
        if self.username==self.user and self.pwd ==self.pas:
            print("Login Successfull")
        else:
            print("Login Unsuccessfull")

obj=user("Atharva",123)
obj.authentication()