from bank import Bank

class Account(Bank):
    def __init__(self,ipsc,Bname,Acc_no,Acc_holder):
        super().__init__(ipsc,Bname)
        self.Acc_no=Acc_no
        self.Acc_holder = Acc_holder

    def display(self):
        super().display()
        print("Account Number: " , self.Acc_no)
        print("Account Holder:  " , self.Acc_holder)