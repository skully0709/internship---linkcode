a = int(input("Enter a number: "))

is_prime = True

if a == 1:
    print("Number is unique")
    is_prime = False
elif a < 1:
    print("Number is not prime")
    is_prime = False
else:
    for i in range(2, a//2+1):
        if a % i == 0:
            print("Number is not prime")
            is_prime = False
            break

    if is_prime:
        print("Number is prime")