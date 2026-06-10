rows = int(input("Enter number of rows: "))
n = rows //2
if rows%2==1:
    for i in range(n+1,1,-1):
        for j in range(0,rows-i-1):
            print(" ",end="")

        if i==n+1:
            for j in range(i):
                print("* ",end="")
            print()
            continue
        
        print("*"+"  "*(i-2)+" *")

    for i in range(1,n+2):
        for j in range(0,rows-i-1):
            print(" ",end="")

        if i==n+1 or i==1:
            for j in range(i):
                print("* ",end="")
            print()
            continue
        
        print("*"+"  "*(i-2)+" *")






else:
    for i in range(n,0,-1):
        for j in range(0,rows-i-1):
            print(" ",end="")

        if i==n or i==1:
            for j in range(i):
                print("* ",end="")
            print()
            continue
        
        print("*"+"  "*(i-2)+" *")

    for i in range(1,n+1):
        for j in range(0,rows-i-1):
            print(" ",end="")

        if i==n or i==1:
            for j in range(i):
                print("* ",end="")
            print()
            continue
        
        print("*"+"  "*(i-2)+" *")
    
