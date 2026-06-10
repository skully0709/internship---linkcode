rows = int(input("Enter number of rows: "))
n=rows//2

# for i in range(rows):
#     if i==0 or i==n or i == rows-1:
#         print("* "*rows)

#     elif i<n:
#         print("*" + " "*(2*i-1)+"*"+" "*(2*(n-i)-1) + "*",end="")
#         print(" " * (2*(n-i)-1) + "*" + " "*(2*i-1) + "*")
#     else:
#         print("*" + " "*(2*(rows-i)-3)+"*"+" "*(2*i-rows) + "*",end="")
#         print(" " * (2*i-rows) + "*" + " "*(2*(rows-i)-3) + "*")


for i in range(rows):
    for j in range(rows):
        if j==0 or i==0 or j == rows-1 or i == rows-1:
            print("*",end=" ")
        
        elif j==n or i==n:
            print("*",end=" ")

        elif i==j or i==(rows-j-1):
            print("*", end=" ")

        else:
            print(" ", end=" ")
    print()
