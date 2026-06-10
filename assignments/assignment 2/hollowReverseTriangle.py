rows = int(input("Enter number of rows: "))

for i in range(rows,0,-1):
    for j in range(0,rows-i):
        print(" ",end="")
    
    if i==rows or i==1:
        print("* "*i)
    else:
        print("*"+ "  "*(i-2)+" *")

