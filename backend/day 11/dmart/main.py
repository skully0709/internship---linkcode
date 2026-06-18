from clothes import clothes
from grocery import grocery
import copy


all_clothes = [clothes(1,"Apparel", "Slim Fit Jeans", 1, 999, "Dark Denim", "32x32")]

all_grocery = [grocery(2,"Dairy & Breakfast", "Organic Whole Milk", 2, 100, "2026-06-25", "DairyFresh", "2026-06-15")]
flag=True
cart = []
total = 0

while flag:
    print("---------------------------------------------------------------------")
    print("Welcome to Dmart\n1.Clothing Section\n2.Grocery Section\n3.Generate Bill\n4.Exit")
    ch=int(input("Enter your choice: "))

    match ch:
        case 1:
            print("------------------------------------------------")
            for i in all_clothes:
                i.display()
            id = int(input("Enter the ID of the product you want to purchase: "))
            for i in all_clothes:
                if i.id == id:
                    quan = int(input("Enter the quantity: "))
                    if quan>0 and quan<=i.qty:
                        temp = i
                        i.qty-=quan
                        temp.qty = quan
                        cart.append(temp)
                        print("Item added successfully")
                    else:
                        print("Invalid quantity")
                        continue    
                else:
                    print("Item not found")

        case 2:
            print("------------------------------------------------")
            for i in all_grocery:
                i.display()
            id = int(input("Enter the ID of the product you want to purchase: "))
            for i in all_grocery:
                if i.id == id:
                    quan = int(input("Enter the quantity: "))
                    if quan>0 and quan<=i.qty:
                        temp = copy.copy(i)
                        i.qty=i.qty-quan
                        temp.qty = quan
                        
                        cart.append(temp)
                        print("Item added successfully")
                    else:
                        print("Invalid quantity")
                        continue   
                else:
                    print("Item not found")
        case 3:
            print("\n1. Add more items\n2. Checkout")
            add_choice = int(input("Enter your choice: "))
            
            if add_choice==1:
                continue
            elif add_choice==2:
                print("Your Cart: ")
                for i in cart:
                    i.display()
                    total += i.price*i.qty
                print("==============================================")
                print("Total: " , total)
                print("==============================================")

                print("1. Pay\n2. Return")
                payment_choice = int(input("Enter your choice: "))
                
                if payment_choice==1:
                    print("Payment successful...")
                    flag = False
                    cart.clear()

                elif payment_choice==2:
                    print("Back to menu...")

                else:
                    print("Invalid choice, try again")
            else:
                print("Invalid choice, try again")
                
                
                    
        case 4:
            print("Exiting...")
            flag = False
            