n = int(input("Enter a number: "))

a, b = 0, 1

print("Fibonacci sequence till", n, " numbers: ")

for i in range(n):
    print(a, end=' ')
    a, b = b, a + b

