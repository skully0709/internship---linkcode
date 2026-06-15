def add(a,b):
    return a+b

try:

    a = int(input("Enter number 1: "))
    b = int(input("Enter number 2: "))

except Exception as e:
    print(e)
else:
    print("Sum: ",add(a,b))


