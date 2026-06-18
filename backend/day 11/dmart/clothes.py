from dmart import Dmart

class clothes(Dmart):
    
    def __init__(self,id, category, product_name, qty, price, color, size):
        super().__init__(id,category, product_name, qty, price)
        self.color = color
        self.size = size
        
    def display(self):
        self.display_store_details()
        super().display()
        print(f"Color:        {self.color}")
        print(f"Size:         {self.size}")
        print("-----------------------")