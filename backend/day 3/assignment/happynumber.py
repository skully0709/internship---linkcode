n = int(input("Enter a number: "))

l = []
temp = n
sum = 0
flag = True

while sum != 1:
	sum = 0
	
	while temp>0:
		digit = temp%10
		sum = sum + (digit**2)
		temp = temp//10
	if sum in l:
		flag = False
		break
	else:
		l.append(sum)
	temp = sum

if flag==True:
	print(n , " is an happy number")
else:
	print(n , " is an unhappy number")

