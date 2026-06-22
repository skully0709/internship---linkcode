from classB import B
from classC import C

class D(B,C):
    def __init__(self,name,age,price,contact):
        C.__init__(self,name,price)
        B.__init__(self,name,age)
        print("Class D")
        self.contact = contact
        

obj = D("Rohan", 34,99,9000000000)

print("Name: ", obj.name)
print("Age: ", obj.age)
print("Price: ",obj.price)
print("Contact:",obj.contact)