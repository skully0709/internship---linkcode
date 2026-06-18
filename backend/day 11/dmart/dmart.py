class Dmart:
    S_Name = "Dmart"
    
    def __init__(self, id, category, product_name, qty, price):
        self.id = id
        self.category = category
        self.product_name = product_name
        self.qty = qty
        self.price = price

    def display(self):
        print("--- Product Details ---")
        print(f"ID:           {self.id}")
        print(f"Category:     {self.category}")
        print(f"Product Name: {self.product_name}")
        print(f"Quantity:     {self.qty}")
        print(f"Price:        ₹{self.price:.2f}")
        print(f"Total Value:  ₹{self.qty * self.price:.2f}")

    @classmethod
    def display_store_details(cls):
        print("--- Store Details ---")
        print(f"Store Name: {cls.S_Name}")
        print("------------------------------------------")