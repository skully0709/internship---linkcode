str = input("Enter a string: ")
reverse_str = ""

for i in range(len(str)-1, -1, -1):
    reverse_str += str[i]

print("Reversed string:", reverse_str)

if str == reverse_str:
    print("The string is a palindrome.")
else:
    print("The string is not a palindrome.")