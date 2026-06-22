class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size


class Engine:
    def __init__(self, fuel_type):
        self.fuel_type = fuel_type

class Chassis:
    def __init__(self, wheel_count):
        self.wheel_count = wheel_count

class Vehicle(Engine, Chassis):
    def __init__(self, fuel_type, wheel_count, vehicle_type):
        Engine.__init__(self, fuel_type)
        Chassis.__init__(self, wheel_count)
        self.vehicle_type = vehicle_type


class Fabric:
    def __init__(self, material):
        self.material = material

class Clothing(Fabric):
    def __init__(self, material, size):
        super().__init__(material)
        self.size = size

class Jacket(Clothing):
    def __init__(self, material, size, has_zipper):
        super().__init__(material, size)
        self.has_zipper = has_zipper


class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.balance = balance

class SavingsAccount(BankAccount):
    def __init__(self, account_holder, balance, interest_rate):
        super().__init__(account_holder, balance)
        self.interest_rate = interest_rate

class CurrentAccount(BankAccount):
    def __init__(self, account_holder, balance, overdraft_limit):
        super().__init__(account_holder, balance)
        self.overdraft_limit = overdraft_limit


class Device:
    def __init__(self, brand):
        self.brand = brand

class Phone(Device):
    def __init__(self, brand, network_type):
        super().__init__(brand)
        self.network_type = network_type

class Camera:
    def __init__(self, megapixels):
        self.megapixels = megapixels

class Smartphone(Phone, Camera):
    def __init__(self, brand, network_type, megapixels, model_name):
        Phone.__init__(self, brand, network_type)
        Camera.__init__(self, megapixels)
        self.model_name = model_name


while True:
    print("\n==========================================")
    print("        INHERITANCE PATTERN DEMO          ")
    print("==========================================")
    print("1. Single Inheritance (Employee -> Manager)")
    print("2. Multiple Inheritance (Engine + Chassis -> Vehicle)")
    print("3. Multilevel Inheritance (Fabric -> Clothing -> Jacket)")
    print("4. Hierarchical Inheritance (Bank -> Savings / Current)")
    print("5. Hybrid Inheritance (Device -> Phone + Camera -> Smartphone)")
    print("6. Exit")
    print("==========================================")
    
    choice = input("Select an option (1-6): ").strip()
    print("------------------------------------------")
    
    match choice:
        case "1":
            print("Executing Single Inheritance:\n")
            mgr = Manager("Elena", 115000, 8)
            print(f"Manager Name: {mgr.name}")
            print(f"Salary: ${mgr.salary}")
            print(f"Team Size: {mgr.team_size} people")
            
        case "2":
            print("Executing Multiple Inheritance:\n")
            truck = Vehicle("Diesel", 6, "Cargo Truck")
            print(f"Vehicle Type: {truck.vehicle_type}")
            print(f"Fuel Type: {truck.fuel_type}")
            print(f"Wheels: {truck.wheel_count}")
            
        case "3":
            print("Executing Multilevel Inheritance:\n")
            coat = Jacket("Leather", "L", True)
            print(f"Material base: {coat.material}")
            print(f"Size: {coat.size}")
            print(f"Has Zipper: {coat.has_zipper}")
            
        case "4":
            print("Executing Hierarchical Inheritance:\n")
            savings = SavingsAccount("Marcus", 4500, 4.5)
            current = CurrentAccount("Serena", 12500, 2000)
            print(f"Savings Account -> Holder: {savings.account_holder}, Rate: {savings.interest_rate}%")
            print(f"Current Account -> Holder: {current.account_holder}, Overdraft: ${current.overdraft_limit}")
            
        case "5":
            print("Executing Hybrid Inheritance:\n")
            phone = Smartphone("Apple", "5G", 48, "iPhone 15")
            print(f"Brand: {phone.brand}")
            print(f"Model: {phone.model_name}")
            print(f"Network: {phone.network_type}")
            print(f"Camera: {phone.megapixels}MP")
            
        case "6":
            print("Closing the program. Goodbye!")
            break
            
        case _:
            print("Invalid input. Please choose a number from 1 to 6.")