ch=1

while ch!=5:

    print("1. Addition\n2. Subtraction \n3. Multiplication \n4. Division \n5. Exit")

    ch = int(input("\nEnter your choice: "))

    if(ch>5 or ch<1):
        print("Invalid choice, Try again")
        continue
    
    elif(ch==5):
        print("Exiting... ")
        break

    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))

    print("")
    match ch:
        case 1:
            print("Addition: ",(a+b))
        case 2:
            print("Subtraction: ",(a-b))
        case 3:
            print("Multiplication: ",(a*b))
        case 4:
            print("Division: ",(a/b))
        case 5:
            print("Exiting... ")

    print("\n------------------------------------\n")
