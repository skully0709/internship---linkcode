sum=0
print("Numbers divisible by 5 are")
for i in range(1,101):
    if i%5==0:
        sum+=i
        print(i)

square = sum*sum

print("Sum of number divisible by 5 are: ", sum)
print("Square of sum = ", square)