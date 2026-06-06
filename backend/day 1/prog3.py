gender = (input("Enter gender[M/f]: "))
age = int(input("Enter age: "))
height = int(input("Enter height: "))

if(gender == 'M' and age >= 18 and height >= 170):
    print("You are eligible for joining the army")
else:
    print("You are not eligible for joining the army")