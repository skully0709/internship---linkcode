from Account import Account

class Saving_Account(Account):
    def __init__(self,ipsc,Bname,Acc_no,Acc_holder,bal,FD):
        super().__init__(ipsc,Bname,Acc_no,Acc_holder)
        self.bal=bal
        self.FD = FD

    def display(self):
        print("\nDetails: ")
        super().display()
        print("Balance: " , self.bal)
        print("Fixed Deposit:  " , self.FD)

sa = Saving_Account("1fa2234","SBI",4321556,"Sarthak",100000000,451115151)
sa.display()