a = int(input("Enter a number: "))
sum = 0
print("Factors of ", a, " are: ")

for i in range(1,a):
    if a%i==0:
        print(i)
        sum+=i

if sum==a:
    print(a, "is a perfect number") 
else:   
    print(a, "is not a perfect number")