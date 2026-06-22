from classA import A

class B(A):
    def __init__(self,name,age):
        print("Class B")
        self.age = age
        A.__init__(self,name)