rows = int(input("Enter number of rows: "))

if rows%2==1:
    for i in range(0,rows//2+1):
        for j in range(0,rows-i):
            print(" ",end="")

        for j in range(0,2*i-1):
            print("*",end="")
        print()

    for i in range(rows//2+1,0,-1):
        for j in range(0,rows-i):
            print(" ",end="")

        for j in range(0,2*i-1):
            print("*",end="")
        print()
else:
    for i in range(0,rows//2+1):
        for j in range(0,rows-i):
            print(" ",end="")

        for j in range(0,2*i-1):
            print("*",end="")
        print()

    for i in range(rows//2,0,-1):
        for j in range(0,rows-i):
            print(" ",end="")

        for j in range(0,2*i-1):
            print("*",end="")
        print()