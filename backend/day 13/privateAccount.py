class Account:
    def __init__(self,bal):
        self.__bal=bal

    def getBal(self):
        return self.__bal

    def setBal(self,amt):
        self.__bal=amt

    def __withdraw(self,amt):
        if amt>self.getBal():
            print("Insufficient Balance, try again")
        elif amt<0:
            print("Invalid amount")
        else:
            self.__bal -= amt
            print(amt, " withdrawn")
            print("Remaining Balance: ",self.getBal())
    
    def canWithdraw(self,pin,amt):
        if pin==1234:
            self.__withdraw(amt)
        else:
            print("Incorrect pin")
    
    def deposit(self,amt):
        self.__bal += amt
        print("Amount Deposited")
        print("Total Amount: ",self.getBal())

    
a = Account(500)

print("Balance: ", a.getBal())
amt = int(input("Enter amount to withdraw: "))
pin = int(input("Enter pin: "))
a.canWithdraw(pin,amt)

amt = int(input("Enter amount to deposit: "))
a.deposit(amt)



