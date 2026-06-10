x = [[1,"CAR",500],
    [2,"DOLL",1000],
    [3,"GROCERY",2000],
    [4,"SUNGLASSES",5000]]

ch = 0

def view():
    print("\n------------------------------\n")
    for i in x:
        print(f"Item no.: {i[0]} | Item name: {i[1]} | Item price: {i[2]}")
    print("\n------------------------------\n")

while ch != 7:
    print("1.View Elements")
    print("2.Add Element")
    print("3.Update Element")
    print("4.Delete Element")
    print("5.Search Element")
    print("6.Buy items")
    print("7.Exit")
    ch = int(input("Enter your choice: "))

    match ch:
        case 1:
            view()
        case 2:
            print("\n------------------------------\n")

            count = int(input("How many items do you want to add? "))
            for i in range(count):
                item_no = int(input("Enter item number: "))
                item_name = input("Enter item name: ")
                item_price = int(input("Enter item price: "))
                x.append([item_no, item_name, item_price])
                print("\n------------------------------\n")

            print("Items added successfully!")
            view()
        
        case 3:
            print("\n------------------------------\n")
            view()
            item_no = int(input("Enter item number to Update: "))
            for i in x:
                if i[0]==item_no:
                    print(f"Item no.: {i[0]} | Item name: {i[1]} | Item price: {i[2]}")
                    while True:
                        print("What do you want to update?")
                        print("1.Item name")
                        print("2.Item price")   
                        print("3.Item number")
                        print("4.All")
                        print("Enter your choice: ")
                        choice = int(input())
                        if choice == 1:
                            i[1] = input("Enter new item name: ")
                            print("Item name updated successfully!")
                            break
                        elif choice == 2:
                            i[2] = int(input("Enter new item price: "))
                            print("Item price updated successfully!")
                            break
                        elif choice == 3:
                            i[0] = int(input("Enter new item number: "))
                            print("Item number updated successfully!")
                            break
                        elif choice == 4:
                            i[0] = int(input("Enter new item number: "))
                            i[1] = input("Enter new item name: ")
                            i[2] = int(input("Enter new item price: "))
                            print("Item updated successfully!")
                            break
                        else:
                            print("Invalid Choice! Try again")
                else:
                    print("Item not Found")
                
                view()
            
        case 4:
            print("\n------------------------------\n")
            view()
            while True:
                print("What do you want to delete?")
                print("1.Item")
                print("2.All")
                print("Enter your choice: ")
                choice = int(input())
            
                if choice == 2:
                    x.clear()
                    print("All items deleted successfully!")
                    view()
                    break

                elif choice == 1:
                    item_no = int(input("Enter item number to delete: "))
                    for i in range(len(x)):
                        if x[i][0] == item_no:
                            x.pop(i)
                            print("Item deleted successfully!")
                            break
                        else:
                            print("Item not found!")
                    break
                else:
                    print("Item not found")

            view()
        case 5:
            print("\n------------------------------\n")
            print("Search by id or name?")
            search_by = input("Enter your choice: ")
            if search_by == "id":
                item_no = int(input("Enter item number to search: "))
                for i in x: 
                    if i[0] == item_no:
                        print(f"Item no.: {i[0]} | Item name: {i[1]} | Item price: {i[2]}")
                        break
            elif search_by == "name":
                item_name = input("Enter item name to search: ")
                for i in x:
                    if i[1] == item_name:
                        print(f"Item no.: {i[0]} | Item name: {i[1]} | Item price: {i[2]}")
                        break
            else:
                print("Item not found!")
        case 6:
            print("\n------------------------------\n")
            total = 0
            gst = 0
            for i in x:
                if i[2] > 1000:
                    gst += i[2] * 0.18
                if i[2] <= 1000:
                    gst += i[2] * 0.12
                total += i[2]
            print(f"Total price: {total}")
        case 7:
            print("Exiting...")
            