n = int(input("Enter a number: "))

temp = n
sum = 0
while temp>0:
    digit = temp%10
    sum = sum + digit**3
    temp = temp//10

if sum == n:
    print(n, "is an Armstrong number")
else:
    print(n, "is not an Armstrong number")