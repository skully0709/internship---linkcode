rcb_batting = (
    (1, "Virat Kohli", 75),
    (2, "Venkatesh Iyer", 32),
    (3, "Devdutt Padikkal", 1),
    (4, "Rajat Patidar", 15),
    (5, "Krunal Pandya", 1),
    (6, "Tim David", 24),
    (7, "Jitesh Sharma", 11)
)

print("This is the Final scorecarsorted_by_runsd of RCB batting in 2026 IPL Final")
print("\n---------------------------------\n")

for i in rcb_batting:
    print(f"Batting Position: {i[0]} | Player Name: {i[1]} | Runs: i[2]")
max = rcb_batting[0]

for i in rcb_batting:
    if max[2]<i[2]:
        max = i
        
print(f"\nMaximum runs scored by: {max[1]} - {max[2]} runs")

total = 0

for i in rcb_batting:
    total += i[2]

print("\nTotal runs scored: " , total)

#sorted_by_runs = sorted(rcb_batting,key = lambda x:x[2], reverse=True)

sorted_by_runs = list(rcb_batting)

for i in range(0,len(sorted_by_runs)-1):
    for j in range(i+1,len(sorted_by_runs)):
        if sorted_by_runs[i][2] < sorted_by_runs[j][2]:
            temp = sorted_by_runs[i]
            sorted_by_runs[i] = sorted_by_runs[j]
            sorted_by_runs[j]=temp


print("\nTop 3 performers: ")

for i in range(0,3):
    print(f"{sorted_by_runs[i][1]} : {sorted_by_runs[i][2]} runs")


