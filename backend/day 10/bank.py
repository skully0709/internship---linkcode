class Bank:
    def __init__(self,ipsc,Bname):
        self.ipsc = ipsc
        self.BName =  Bname

    def display(self):
        print("IPSC code: " , self.ipsc)
        print("Bank Name: " , self.BName)


class Saving_Account(Account):
    def __init__(self,ipsc,Bname,Acc_no,Acc_holder,bal,FD):
        super().__init__(ipsc,Bname,Acc_no,Acc_holder)
        self.bal=bal
        self.FD = FD

    def display(self):
        super().display()
        print("Balance: " , self.bal)
        print("Fixed Deposit:  " , self.FD)