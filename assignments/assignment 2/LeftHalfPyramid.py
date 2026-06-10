rows = int(input("Enter number of rows: "))

for i in range(0,rows+1):
        for j in range(0,rows-i):
            print(" ",end="")

        for j in range(0,i):
            print("*",end="")
        print()

