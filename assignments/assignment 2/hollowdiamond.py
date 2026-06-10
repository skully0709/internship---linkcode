rows = int(input("Enter number of rows: "))


if rows%2==1:
    for i in range(0,rows//2):

        for j in range(0,rows-i-1):
            print(" ",end="")
        if i==0:
            print("*")
        else:
            print("*"+" "*(2*i-1)+"*")

    for i in range(rows//2,-1,-1):

        for j in range(0,rows-i-1):
            print(" ",end="")
        if i==0:
            print("*")
        else:
            print("*"+" "*(2*i-1)+"*")

else:
    for i in range(0,rows//2):

        for j in range(0,rows-i-1):
            print(" ",end="")
        if i==0:
            print("*")
        else:
            print("*"+" "*(2*i-1)+"*")

    for i in range(rows//2-1,-1,-1):

        for j in range(0,rows-i-1):
            print(" ",end="")
        if i==0:
            print("*")
        else:
            print("*"+" "*(2*i-1)+"*")