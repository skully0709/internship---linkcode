tup=((1,"CAR",500),(2,"DOLL",1000),30,40,(3,"GROCERY",2000),[50,60],"at")

for i in tup:
    if type(i) == tuple:
        print(f"Item no.: {i[0]} | Item name: {i[1]} | Item price: {i[2]}")
    elif type(i) == list:
        print("List of numbers: ", end="")
        for j in i:
            print(j, end=" ")
        print()
    else:
        print(i)
  