from classA import A

class C(A):
    def __init__(self,name,price):
        print("Class C")
        self.price = price
        A.__init__(self,name)