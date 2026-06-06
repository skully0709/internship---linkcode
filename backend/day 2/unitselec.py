unit = int(input("Enter the number of units: "))

if unit<=100:
    bill = 2*unit
elif unit>100 and unit<=200:
    bill = 200 + (unit-100)*3
elif unit>200:
    bill = 500 + (unit-200)*5

print("Bill: " , bill)
