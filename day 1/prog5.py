a = int(input("Enter a number: "))

print("Factors of the number are: ", end = " ")

for i in range(1, a//2+1):
    if a % i == 0:
        print(i, end = " ")