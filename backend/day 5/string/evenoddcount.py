str = input("Enter a string: ")

even_count = 0
odd_count = 0

for ch in range(len(str)):
        if ch % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

print("Even index count:", even_count)
print("Odd index count:", odd_count)