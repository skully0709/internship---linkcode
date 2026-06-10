rows = int(input("Enter number of rows: "))

if rows%2==1:
    for i in range(1,rows+1):
        if i==rows or i==1 or i == rows//2+1:
            print("*"*rows)
        elif i>rows//2+1:
            print(" "*(rows-1)+"*")
        else:
            print("*")
else:
    for i in range(1,rows+1):
        if i==rows or i==1 or i == rows//2:
            print("*"*rows)
        elif i>rows//2:
            print(" "*(rows-1)+"*")
        else:
            print("*")
