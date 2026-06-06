i = 1
sum =0
print("Even numbers between 1 to 50: ")
while i<=50:
    if i%2==0:
        print(i)
        sum+=i
    i+=1

print("Sum of all even numbers: " , sum)