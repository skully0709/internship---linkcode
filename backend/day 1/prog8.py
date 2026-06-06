n = int(input("Enter a number:"))

a=0
b=1
print("Fibonacci series is: ", end = " ")
for i in range(0,n):
    print(a)
    sum = a + b
    a,b = b,sum
