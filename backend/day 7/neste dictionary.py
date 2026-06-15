stud={
    101:{"Name":"Ram",
          "Age":18,
          "Subjects":["Python","Java","Mern_stack"],
          "Marks":[30,89,78]
        },
    102:{"Name":"Sita",
          "Age":19,
          "Subjects":["Python","Java","Mern_stack"],
          "Marks":[70,80,90]
        },
     103:{"Name":"Rahul",
          "Age":20,
          "Subjects":["Python","Java","Mern_stack"],
          "Marks":[90,100,90]
        },
     104:{"Name":"Gita",
          "Age":11,
          "Subjects":["Python","Java","Mern_stack"],
          "Marks":[89,97,100]
        }
}

print("-------------------------------------------------------------------------")
print("List of all students with total marks:")
print("-------------------------------------------------------------------------")

m=0
for k , v in stud.items():
  sum = 0
  
  for l in v.values():
    if type(v)==list and type[v[0]] == int:
      sum += l
        
  print(f"{k} : ")

  for value in v.values():
    if type(value)==list and type(value[0]) == int:
      for n in value:
        sum += n

  if m < sum:
     m = k   

  v.update({"Total":sum})

  for key,value in v.items():
    print(f"{key} - {value}")

  print("-------------------------------------------------------------------------")


print("Topper from the above list of students is:")

for key,value in stud[m].items():
    print(f"{key} - {value}")

print("-------------------------------------------------------------------------")
python_topper_id = max(stud, key=lambda sid: stud[sid]["Marks"][0])
print(f"\nName of the student who has Highest score in Python: {stud[python_topper_id]['Name']} (Score: {stud[python_topper_id]['Marks'][0]})\n")


print("-------------------------------------------------------------------------")

print("Name of the students having marks between 70-90 in MERN Stack are:")

print("-------------------------------------------------------------------------")
for key,value in stud.items():
  if value["Marks"][2]>=70 and value["Marks"][2]<=90:
    for k,v in value.items():
      print(f"{k} - {v}")
    print("-------------------------------------------------------------------------")


print("Name of the students who has ag greater that 19 are:")

print("-------------------------------------------------------------------------")
for key,value in stud.items():
  if value["Age"]>19:
    for k,v in value.items():
      print(f"{k} - {v}")
    print("-------------------------------------------------------------------------")



