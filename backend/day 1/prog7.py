n = int(input("Enter a number:"))

temp = n
arm = 0

while temp>0:
    div = temp% 10
    arm = arm + div**3
    temp = temp//10

if arm == n:
    print("Number is an Armstrong number")
else:
    print("Number is not an Armstrong number")