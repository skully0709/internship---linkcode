str = input("Enter a string: ")

vowel = "aeiouAEIOU"

for ch in str:
    if ch in vowel:
        print(ch)