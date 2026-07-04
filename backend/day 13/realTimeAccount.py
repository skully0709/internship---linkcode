import random
import time

# add time module for otp generation

class Account:
    def __init__(self,name,username,password):
        self.name=name
        self.__password = password
        self.username = username
        self.__loginStatus = False
    
    def __setLoginStatus(self,status):
        self.__loginStatus = status

    def getLoginStatus(self):
        return self.__loginStatus

    def login(self,username,pwd):
        if self.username==username and self.__password==pwd:
            otp = random.randint(1000,9999)
            print("Your OTP: ", otp)



            if self.__getOtp(otp):
                print("Login successful.")
                self.__setLoginStatus(True)
            else:
                print("Invalid otp")
            
        else:
            print("Invalid Credentials")

    def __getOtp(self,otp):
        temp = int(input("Enter the Otp: "))
        
        if temp==otp:
            return True
        else: return False

a = Account("Ram","Ram123",12345)

a.login("Ram123",12345)
    