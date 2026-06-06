a = int(input("Enter number 1: "))
b = int(input("Enter number 2: "))

if a>=b:
    for i in range(b,a,4):
            print(i)
else:
    for i in range(a,b,4):
            print(i)