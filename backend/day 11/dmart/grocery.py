from dmart import Dmart

class grocery(Dmart):
    
    def __init__(self, id,category, product_name, qty, price, expiry, BName, manufacturing_date):
        super().__init__(id,category, product_name, qty, price)
        self.expiry = expiry
        self.BName = BName
        self.manufacturing_date = manufacturing_date
        
    def display(self):
        self.display_store_details()
        super().display()
        print(f"Brand Name:   {self.BName}")
        print(f"Mfg Date:     {self.manufacturing_date}")
        print(f"Expiry Date:  {self.expiry}")
        print("-----------------------")