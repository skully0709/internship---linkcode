n = int(input("Enter a number: "))

flag = True

if n == 1:
    print(n, "is a unique number")
    flag = False
elif n < 1:
    print(n, "is not a prime number")
    flag = False

else:
    for i in range(2,n//2+1):
        if n%i==0:
            print(n, "is not a prime number")
            flag = False
            break

    if flag==True:
        print(n, "is a prime number")