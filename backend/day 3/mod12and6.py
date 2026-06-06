a = int(input("Enter number 1: "))
b = int(input("Enter number 2: "))

print("Numbers that are divisible by 12 and 6 are: ")

if a>=b:
    for i in range(b,a,1):
        if i%12==0 and i%6==0:
            print(i)
else:
    for i in range(a,b,1):
        if i%12==0 and i%6==0:
            print(i)
