"""
MODULE 2: Pet Inventory & Listing Management
Access Level: Admin Only
Owner: Shravani
"""

from tabulate import tabulate
from db_functions import get_connection, log_activity

current_user = None


def add_pets():
    name = input("Enter Pet Name : ")
    species = input("Enter Species : ")
    breed = input("Enter Breed : ")
    age = int(input("Enter Age : "))

    print("\nHealth Status")
    print("1. Healthy")
    print("2. Needs Care")
    print("3. Special Needs")
    h = input("Choose : ")

    match h:
        case "1":
            health = "Healthy"
        case "2":
            health = "Needs Care"
        case _:
            health = "Special Needs"

    status = "Available"
    shelter = int(input("Enter Shelter ID : "))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Pets (Name, Species, Breed, Age, Health_Status, Adoption_Status, Shelter_ID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, species, breed, age, health, status, shelter))
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Added new pet '{name}'")
    print("\nPet Added Successfully")


def view_pet():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Pet_ID, Name, Species, Breed, Age, Health_Status, Adoption_Status, Shelter_ID FROM Pets")
    data = cur.fetchall()
    conn.close()

    if not data:
        print("No pets found."); return
    print(tabulate(data, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health", "Status", "Shelter"], tablefmt="grid"))


def update_age():
    while True:
        print("\n========== UPDATE PET AGE ==========")
        print("1. Update by Pet ID")
        print("2. Update by Pet Name")
        print("3. Back")
        choice = input("Enter Choice : ")

        match choice:
            case "1":
                pid = int(input("Enter Pet ID : "))
                age = int(input("Enter New Age : "))

                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Pets SET Age = ? WHERE Pet_ID = ?", (age, pid))
                conn.commit()
                updated = cur.rowcount
                conn.close()

                if updated > 0:
                    log_activity(current_user["Username"], "admin", f"Updated age for Pet ID {pid}")
                    print("Age Updated Successfully.")
                else:
                    print("Pet ID Not Found.")

            case "2":
                name = input("Enter Pet Name : ")
                age = int(input("Enter New Age : "))

                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Pets SET Age = ? WHERE Name = ?", (age, name))
                conn.commit()
                updated = cur.rowcount
                conn.close()

                if updated > 0:
                    log_activity(current_user["Username"], "admin", f"Updated age for pet '{name}'")
                    print("Age Updated Successfully.")
                else:
                    print("Pet Name Not Found.")

            case "3":
                return

            case _:
                print("Invalid Choice")


def update_health():
    while True:
        print("\n========== UPDATE HEALTH STATUS ==========")
        print("1. Update by Pet ID")
        print("2. Update by Pet Name")
        print("3. Back")
        choice = input("Enter Choice : ")

        match choice:
            case "1":
                pet_id = int(input("Enter Pet ID : "))

                print("\nSelect Health Status")
                print("1. Healthy")
                print("2. Needs Care")
                print("3. Special Needs")
                ch = input("Enter Choice : ")

                match ch:
                    case "1":
                        health = "Healthy"
                    case "2":
                        health = "Needs Care"
                    case "3":
                        health = "Special Needs"
                    case _:
                        print("Invalid Choice"); continue

                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Pets SET Health_Status = ? WHERE Pet_ID = ?", (health, pet_id))
                conn.commit()
                updated = cur.rowcount
                conn.close()

                if updated > 0:
                    log_activity(current_user["Username"], "admin", f"Updated health status for Pet ID {pet_id}")
                    print("Health Status Updated Successfully.")
                else:
                    print("Pet ID Not Found.")

            case "2":
                pet_name = input("Enter Pet Name : ")

                print("\nSelect Health Status")
                print("1. Healthy")
                print("2. Needs Care")
                print("3. Special Needs")
                ch = input("Enter Choice : ")

                match ch:
                    case "1":
                        health = "Healthy"
                    case "2":
                        health = "Needs Care"
                    case "3":
                        health = "Special Needs"
                    case _:
                        print("Invalid Choice"); continue

                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Pets SET Health_Status = ? WHERE Name = ?", (health, pet_name))
                conn.commit()
                updated = cur.rowcount
                conn.close()

                if updated > 0:
                    log_activity(current_user["Username"], "admin", f"Updated health status for '{pet_name}'")
                    print("Health Status Updated Successfully.")
                else:
                    print("Pet Name Not Found.")

            case "3":
                return

            case _:
                print("Invalid Choice")


def update_status():
    pid = int(input("Enter Pet ID : "))

    print("1. Available")
    print("2. Pending")
    print("3. Adopted")
    ch = input("Choose : ")

    match ch:
        case "1":
            status = "Available"
        case "2":
            status = "Pending"
        case _:
            status = "Adopted"

 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Pets SET Adoption_Status = ?, Requested_By = NULL WHERE Pet_ID = ?", (status, pid))
    conn.commit()
    updated = cur.rowcount
    conn.close()

    if updated > 0:
        log_activity(current_user["Username"], "admin", f"Updated status for Pet ID {pid} to {status}")
        print("Status Updated Successfully")
    else:
        print("Pet ID Not Found.")


def delete_pet():
    while True:
        print("\n========== DELETE PET ==========")
        print("1. Delete by Pet ID")
        print("2. Delete by Pet Name")
        print("3. Delete All Records")
        print("4. Back")
        choice = input("Enter Choice : ")

        match choice:
            case "1":
                pet_id = int(input("Enter Pet ID : "))
                confirm = input("Are you sure? (Y/N) : ")

                if confirm.upper() == "Y":
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Pets WHERE Pet_ID = ?", (pet_id,))
                    conn.commit()
                    deleted = cur.rowcount
                    conn.close()

                    if deleted > 0:
                        log_activity(current_user["Username"], "admin", f"Deleted Pet ID {pet_id}")
                        print("Pet Deleted Successfully.")
                    else:
                        print("Pet ID Not Found.")
                else:
                    print("Deletion Cancelled.")

            case "2":
                pet_name = input("Enter Pet Name : ")
                confirm = input("Are you sure? (Y/N) : ")

                if confirm.upper() == "Y":
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Pets WHERE Name = ?", (pet_name,))
                    conn.commit()
                    deleted = cur.rowcount
                    conn.close()

                    if deleted > 0:
                        log_activity(current_user["Username"], "admin", f"Deleted pet '{pet_name}'")
                        print("Pet Deleted Successfully.")
                    else:
                        print("Pet Name Not Found.")
                else:
                    print("Deletion Cancelled.")

            case "3":
                confirm = input("Delete ALL pet records? (YES/NO) : ")
                if confirm.upper() == "YES":
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Pets")
                    conn.commit()
                    conn.close()

                    log_activity(current_user["Username"], "admin", "Deleted ALL pet records")
                    print("All Pet Records Deleted Successfully.")
                else:
                    print("Deletion Cancelled.")

            case "4":
                return

            case _:
                print("Invalid Choice")


def pet_management_menu_admin(user):
    global current_user
    current_user = user

    while True:
        print("\n========= PET INVENTORY =========")
        print("1. Add New Pet")
        print("2. View All Pets")
        print("3. Update Pet Age")
        print("4. Update Health Status")
        print("5. Update Adoption Status")
        print("6. Delete Pet")
        print("7. Back")
        ch = input("Enter Choice : ")

        match ch:
            case "1":
                add_pets()
            case "2":
                view_pet()
            case "3":
                update_age()
            case "4":
                update_health()
            case "5":
                update_status()
            case "6":
                delete_pet()
            case "7":
                return
            case _:
                print("Invalid Choice")
