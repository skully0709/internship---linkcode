print("Enter 5 list elements:")
lst = []
squaresum = 0
for i in range(5):
    num = int(input())
    lst.append(num)
    squaresum += num ** 2
print("Sum of squares:", squaresum)
