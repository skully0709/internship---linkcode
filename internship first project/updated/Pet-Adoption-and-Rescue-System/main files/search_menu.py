"""
MODULE 3: Pet Search & Discovery
Access Level: Admin (Full Access) | Adopter (Available Pets Only)
Owner: Kadambari
"""

from tabulate import tabulate
from db_functions import get_connection


def search_menu(user=None):
    conn = get_connection()
    cur = conn.cursor()

    while True:
        print("\n========== PET SEARCH & DISCOVERY ==========")
        print("1. Display All Available Pets")
        print("2. Search by Name")
        print("3. Search by Breed")
        print("4. Search by Species")
        print("5. Search by Age")
        print("6. Search by Health Status")
        print("7. Search by Shelter Location")
        print("8. View Pet Details")
        print("9. Back")
        choice = input("\nEnter Choice : ")

        match choice:
            case "1":
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Adoption_Status = 'Available'
                """)
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("No pets available.")

            case "2":
                name = input("Enter Pet Name : ")
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Name LIKE ? AND Adoption_Status = 'Available'
                """, ('%' + name + '%',))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("Pet not found.")

            case "3":
                breed = input("Enter Breed : ")
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Breed LIKE ? AND Adoption_Status = 'Available'
                """, ('%' + breed + '%',))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("No matching pets.")

            case "4":
                species = input("Enter Species : ")
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Species = ? AND Adoption_Status = 'Available'
                """, (species,))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("No pets found.")

            case "5":
                age = int(input("Enter Age : "))
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Age = ? AND Adoption_Status = 'Available'
                """, (age,))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("No pets found.")

            case "6":
                health = input("Enter Health Status : ")
                cur.execute("""
                    SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
                    FROM Pets WHERE Health_Status = ? AND Adoption_Status = 'Available'
                """, (health,))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))
                else:
                    print("No pets found.")

            case "7":
                location = input("Enter Location : ")
                cur.execute("""
                    SELECT Pets.Pet_ID, Pets.Name, Pets.Species, Pets.Breed, Pets.Age,
                           Shelters.Shelter_Name, Shelters.Location
                    FROM Pets JOIN Shelters ON Pets.Shelter_ID = Shelters.Shelter_ID
                    WHERE Shelters.Location LIKE ? AND Pets.Adoption_Status = 'Available'
                """, ('%' + location + '%',))
                data = cur.fetchall()
                if data:
                    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Shelter", "Location"], tablefmt="grid"))
                else:
                    print("No Available pets found in this location.")

            case "8":
                petid = int(input("Enter Pet ID : "))
                cur.execute("""
                    SELECT Pets.Pet_ID, Pets.Name, Pets.Species, Pets.Breed, Pets.Age,
                           Pets.Health_Status, Pets.Adoption_Status,
                           Shelters.Shelter_Name, Shelters.Location,
                           Vaccinations.Vaccine_Name, Vaccinations.Date_Administered,
                           Vaccinations.Next_Due_Date, Vaccinations.Veterinarian
                    FROM Pets
                    JOIN Shelters ON Pets.Shelter_ID = Shelters.Shelter_ID
                    LEFT JOIN Vaccinations ON Pets.Pet_ID = Vaccinations.Pet_ID
                    WHERE Pets.Pet_ID = ?
                """, (petid,))
                row = cur.fetchone()

                if row:
                    details = [
                        ["Pet ID", row[0]], ["Name", row[1]], ["Species", row[2]],
                        ["Breed", row[3]], ["Age", row[4]], ["Health Status", row[5]],
                        ["Adoption Status", row[6]], ["Shelter", row[7]], ["Location", row[8]],
                        ["Vaccine", row[9]], ["Vaccinated On", row[10]],
                        ["Next Due", row[11]], ["Veterinarian", row[12]],
                    ]
                    print(tabulate(details, tablefmt="grid"))
                else:
                    print("Pet not found.")

            case "9":
                conn.close()
                return

            case _:
                print("Invalid Choice")
