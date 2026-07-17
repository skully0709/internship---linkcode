"""
MODULE 5: Adoption Transaction Management
Real-Time Pet Adoption & Rescue Management System
Access Level: Admin (Process & Approve) | Adopter (Request & View History)
Owner: Nishtha

"""

from datetime import date
from tabulate import tabulate

from db_functions import get_connection, log_activity

# Set once when a dashboard opens; every other function reads from this.
current_user = None


# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------

def pet_exists(pet_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Pet_ID, Name, Adoption_Status FROM Pets WHERE Pet_ID = ?", (pet_id,))
    row = cur.fetchone()
    conn.close()
    return row


def list_available_pets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Pet_ID, Name, Species, Breed, Adoption_Status FROM Pets WHERE Adoption_Status = 'Available'")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No pets are currently available."); return
    print(tabulate(rows, headers=["Pet ID", "Name", "Species", "Breed", "Status"], tablefmt="grid"))


def list_pending_pets():
 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.Pet_ID, p.Name, p.Species, p.Breed, p.Adoption_Status,
               a.Username, a.Full_Name
        FROM Pets p
        LEFT JOIN Adopters a ON p.Requested_By = a.Adopter_Id
        WHERE p.Adoption_Status = 'Pending'
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No pending adoption requests."); return None

    display = [[r[0], r[1], r[2], r[3], r[4], r[6] or "(no requester on file)"] for r in rows]
    print(tabulate(display, headers=["Pet ID", "Name", "Species", "Breed", "Status", "Requested By"], tablefmt="grid"))
    return rows


def find_adopter_by_username(username):
    conn = get_connection()
    conn.row_factory = None
    cur = conn.cursor()
    cur.execute("SELECT Adopter_Id, Full_Name, Username FROM Adopters WHERE Username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def has_active_transaction(pet_id):
    """True if this pet already has an un-returned (active) adoption."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM Adoption_Transactions WHERE Pet_ID = ? AND Return_Date IS NULL",
        (pet_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row is not None


# ---------------------------------------------------------------------
# 5.1 / 5.2  ADOPTER SIDE - REQUEST ADOPTION
# ---------------------------------------------------------------------

def request_adoption():
    print("\n-- Request Adoption --")
    list_available_pets()
    pet_id = input("Enter Pet ID you'd like to adopt: ").strip()

    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return

    # 5.2.1 Availability Check
    if pet[2] != "Available":
        print(f"{pet[1]} is not currently available (status: {pet[2]})."); return

    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "UPDATE Pets SET Adoption_Status = 'Pending', Requested_By = ? WHERE Pet_ID = ?",
        (current_user["Adopter_Id"], pet_id),
    )
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "adopter", f"Requested adoption for Pet ID {pet_id}")
    print(f"Adoption request submitted for {pet[1]}. An administrator will review it shortly.")


# ---------------------------------------------------------------------
# ADOPTER SIDE - VIEW HISTORY
# ---------------------------------------------------------------------

def view_my_adoption_history():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.Transaction_ID, p.Name, t.Adoption_Date, t.Return_Date
        FROM Adoption_Transactions t
        LEFT JOIN Pets p ON t.Pet_ID = p.Pet_ID
        WHERE t.Adopter_Id = ?
        ORDER BY t.Transaction_ID DESC
    """, (current_user["Adopter_Id"],))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("You have no adoption history yet."); return

    display = [[r[0], r[1], r[2], r[3] or "-", "Returned" if r[3] else "Active"] for r in rows]
    print(tabulate(display, headers=["Transaction ID", "Pet", "Adoption Date", "Return Date", "Status"], tablefmt="grid"))


def return_my_pet():
    """Lets an adopter return one of their own currently-adopted pets.
    Scoped to their own Adopter_Id only - they can't return anyone else's."""
    print("\n-- Return a Pet --")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.Transaction_ID, p.Pet_ID, p.Name
        FROM Adoption_Transactions t
        LEFT JOIN Pets p ON t.Pet_ID = p.Pet_ID
        WHERE t.Adopter_Id = ? AND t.Return_Date IS NULL
    """, (current_user["Adopter_Id"],))
    active = cur.fetchall()
    conn.close()

    if not active:
        print("You have no active adoptions to return."); return

    print(tabulate(active, headers=["Transaction ID", "Pet ID", "Pet Name"], tablefmt="grid"))
    transaction_id = input("Enter the Transaction ID for the pet you're returning: ").strip()

    match = next((row for row in active if str(row[0]) == transaction_id), None)
    if not match:
        print("That transaction ID isn't one of your active adoptions."); return

    pet_id = match[1]
    return_date = str(date.today())

    conn = get_connection()
    cur = conn.cursor()
    # 5.3.2 History Tracking: fill in Return_Date, never delete the row
    cur.execute(
        "UPDATE Adoption_Transactions SET Return_Date = ? WHERE Transaction_ID = ?",
        (return_date, transaction_id),
    )
    cur.execute("UPDATE Pets SET Adoption_Status = 'Available' WHERE Pet_ID = ?", (pet_id,))
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "adopter", f"Returned Pet ID {pet_id}")
    print(f"{match[2]} has been returned and is now marked Available again.")


# ---------------------------------------------------------------------
# 5.1 / 5.2  ADMIN SIDE - PROCESS ADOPTION REQUESTS
# ---------------------------------------------------------------------

def view_pending_requests():
    print("\n-- Pending Adoption Requests --")
    list_pending_pets()


def process_adoption():
    print("\n-- Process Adoption Request --")
    pending = list_pending_pets()
    if not pending:
        return

    pet_id = input("Enter Pet ID to finalize: ").strip()
    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return

    # 5.2.1 Availability Check (must still be Pending, not already grabbed)
    if pet[2] != "Pending":
        print(f"{pet[1]} is not awaiting approval (status: {pet[2]})."); return

    # 5.2.2 Duplicate Check
    if has_active_transaction(pet_id):
        print(f"{pet[1]} already has an active adoption on record."); return

  
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Requested_By FROM Pets WHERE Pet_ID = ?", (pet_id,))
    requested_by = cur.fetchone()
    conn.close()
    requested_by = requested_by[0] if requested_by else None

    if requested_by:
        conn = get_connection()
        conn.row_factory = None
        cur = conn.cursor()
        cur.execute("SELECT Adopter_Id, Full_Name, Username FROM Adopters WHERE Adopter_Id = ?", (requested_by,))
        adopter = cur.fetchone()
        conn.close()
        if not adopter:
            print("The adopter who requested this pet no longer has an account.")
            requested_by = None

    if not requested_by:
        username = input("No requester on file - enter the Adopter's Username to link this adoption to: ").strip()
        adopter = find_adopter_by_username(username)
        if not adopter:
            print("No adopter found with that username."); return
    else:
        print(f"Linking this adoption to the adopter who requested it: {adopter[1]} ({adopter[2]})")
        confirm = input("Confirm this is correct? (Y/N): ").strip().upper()
        if confirm != "Y":
            print("Adoption not processed."); return

    adoption_date = str(date.today())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Adoption_Transactions (Pet_ID, Adopter_Id, Adoption_Date) VALUES (?, ?, ?)",
        (pet_id, adopter[0], adoption_date),
    )

    cur.execute("UPDATE Pets SET Adoption_Status = 'Adopted', Requested_By = NULL WHERE Pet_ID = ?", (pet_id,))
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Approved adoption of Pet ID {pet_id} by {adopter[2]}")
    print(f"Adoption finalized: {pet[1]} -> {adopter[1]} ({adoption_date}).")


def reject_adoption_request():

    print("\n-- Reject Adoption Request --")
    pending = list_pending_pets()
    if not pending:
        return

    pet_id = input("Enter Pet ID to reject: ").strip()
    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return
    if pet[2] != "Pending":
        print(f"{pet[1]} is not awaiting approval (status: {pet[2]})."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Pets SET Adoption_Status = 'Available', Requested_By = NULL WHERE Pet_ID = ?",
        (pet_id,),
    )
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Rejected adoption request for Pet ID {pet_id}")
    print(f"Request for {pet[1]} has been rejected. The pet is Available again.")


# ---------------------------------------------------------------------
# 5.3  ADMIN SIDE - RETURN MANAGEMENT
# ---------------------------------------------------------------------

def process_return():
    print("\n-- Process Pet Return --")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Pet_ID, Name, Species, Breed FROM Pets WHERE Adoption_Status = 'Adopted'")
    adopted = cur.fetchall()
    conn.close()

    if not adopted:
        print("No pets are currently marked as adopted."); return
    print(tabulate(adopted, headers=["Pet ID", "Name", "Species", "Breed"], tablefmt="grid"))

    pet_id = input("Enter Pet ID being returned: ").strip()
    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return
    if pet[2] != "Adopted":
        print(f"{pet[1]} is not currently marked as adopted."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT Transaction_ID FROM Adoption_Transactions WHERE Pet_ID = ? AND Return_Date IS NULL",
        (pet_id,),
    )
    active = cur.fetchone()
    if not active:
        print("No active adoption transaction found for this pet."); conn.close(); return

    return_date = str(date.today())
    # 5.3.2 History Tracking: fill in Return_Date, never delete the row
    cur.execute(
        "UPDATE Adoption_Transactions SET Return_Date = ? WHERE Transaction_ID = ?",
        (return_date, active[0]),
    )
    cur.execute("UPDATE Pets SET Adoption_Status = 'Available' WHERE Pet_ID = ?", (pet_id,))
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Processed return of Pet ID {pet_id}")
    print(f"{pet[1]} has been marked as returned and is now Available again.")


def view_all_transactions():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.Transaction_ID, p.Name, a.Full_Name, t.Adoption_Date, t.Return_Date
        FROM Adoption_Transactions t
        LEFT JOIN Pets p ON t.Pet_ID = p.Pet_ID
        LEFT JOIN Adopters a ON t.Adopter_Id = a.Adopter_Id
        ORDER BY t.Transaction_ID DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No adoption transactions yet."); return

    display = [[r[0], r[1], r[2], r[3], r[4] or "-", "Returned" if r[4] else "Active"] for r in rows]
    print(tabulate(display, headers=["Transaction ID", "Pet", "Adopter", "Adoption Date", "Return Date", "Status"], tablefmt="grid"))


# =======================================================================
# ADOPTER DASHBOARD
# =======================================================================

def adopter_adoption_dashboard(user):
    global current_user
    current_user = user

    while True:
        print(f"\n--- Adoption ({current_user['Full_Name']}) ---")
        print("1. Request Adoption                 (5.1 / 5.2)")
        print("2. View My Adoption History")
        print("3. Return a Pet                      (5.3)")
        print("4. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                request_adoption()
            case "2":
                view_my_adoption_history()
            case "3":
                return_my_pet()
            case "4":
                return
            case _:
                print("Invalid option.")


# =======================================================================
# ADMIN DASHBOARD
# =======================================================================

def admin_adoption_dashboard(user):
    global current_user
    current_user = user

    while True:
        print(f"\n--- Manage Adoptions ({current_user['Full_Name']}) ---")
        print("1. View Pending Adoption Requests")
        print("2. Process Adoption Request          (5.1 / 5.2)")
        print("3. Reject Adoption Request")
        print("4. Process Pet Return                 (5.3)")
        print("5. View All Adoption Transactions")
        print("6. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                view_pending_requests()
            case "2":
                process_adoption()
            case "3":
                reject_adoption_request()
            case "4":
                process_return()
            case "5":
                view_all_transactions()
            case "6":
                return
            case _:
                print("Invalid option.")