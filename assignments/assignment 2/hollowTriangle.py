rows = int(input("Enter number of rows: "))

for i in range(1,rows+1):

        for j in range(0,rows-i):
            print(" ",end="")
        
        if i==rows or i==1:
            print("*"*(2*i-1),end="")
            # for k in range(2*i-1):
            #     print("*",end="")
            print()
            continue

        print("* "+"  "*(i-2)+"*")

        # print("*", end="")
        # for j in range(0,2*i-3):
        #     print(" ",end="")
        # print("*")
