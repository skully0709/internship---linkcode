rows = int(input("Enter number of rows: "))

for i in range(0,rows):
    if i == 0 or i==rows-1:
        print(" * "*rows)
        continue
    else:
        print(" * ","  "*(rows-2),"  * ")
