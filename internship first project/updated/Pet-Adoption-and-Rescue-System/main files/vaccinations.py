"""
MODULE 4: Vaccination & Medical Tracking
Real-Time Pet Adoption & Rescue Management System
Access Level: Admin (Full Access) | Adopter (Read-Only Access)
Owner: Avishkar


"""

from datetime import date, timedelta
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
    cur.execute("SELECT Pet_ID, Name FROM Pets WHERE Pet_ID = ?", (pet_id,))
    row = cur.fetchone()
    conn.close()
    return row


def list_pets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Pet_ID, Name, Species, Health_Status, Adoption_Status FROM Pets")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No pets found in the system yet."); return
    print(tabulate(rows, headers=["Pet ID", "Name", "Species", "Health Status", "Adoption Status"], tablefmt="grid"))


def view_all_vaccinations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT v.Vaccination_ID, p.Name, v.Vaccine_Name, v.Date_Administered,
               v.Next_Due_Date, v.Veterinarian
        FROM Vaccinations v
        LEFT JOIN Pets p ON v.Pet_ID = p.Pet_ID
        ORDER BY v.Vaccination_ID
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No vaccination records yet."); return
    print(tabulate(rows, headers=["Vacc. ID", "Pet Name", "Vaccine", "Administered", "Next Due", "Veterinarian"], tablefmt="grid"))


def view_vaccinations_for_pet():
    list_pets()
    pet_id = input("Enter Pet ID: ").strip()
    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Vaccine_Name, Date_Administered, Next_Due_Date, Veterinarian
        FROM Vaccinations WHERE Pet_ID = ?
        ORDER BY Date_Administered DESC
    """, (pet_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"No vaccination records found for {pet[1]}."); return
    print(f"\nVaccination history for {pet[1]}:")
    print(tabulate(rows, headers=["Vaccine", "Administered", "Next Due", "Veterinarian"], tablefmt="grid"))


# ---------------------------------------------------------------------
# 4.1  MEDICAL RECORD ENTRY  (Admin only)
# ---------------------------------------------------------------------

def record_vaccination():
    print("\n-- Record New Vaccination --")
    list_pets()
    pet_id = input("Enter Pet ID: ").strip()

    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return

    vaccine_name = input("Vaccine Name: ").strip()
    if not vaccine_name:
        print("Vaccine name is required."); return

    date_administered = input(f"Administration Date [YYYY-MM-DD, blank = today ({date.today()})]: ").strip()
    if not date_administered:
        date_administered = str(date.today())

    next_due_date = input("Next Due Date [YYYY-MM-DD]: ").strip()
    veterinarian = input("Veterinarian: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Vaccinations (Pet_ID, Vaccine_Name, Date_Administered, Next_Due_Date, Veterinarian)
           VALUES (?, ?, ?, ?, ?)""",
        (pet_id, vaccine_name, date_administered, next_due_date, veterinarian),
    )
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Recorded vaccination '{vaccine_name}' for Pet ID {pet_id}")
    print(f"Vaccination record added for {pet[1]} (Pet ID {pet_id}).")


# ---------------------------------------------------------------------
# 4.2  MEDICAL HISTORY MANAGEMENT  (Admin only)
# ---------------------------------------------------------------------

def edit_vaccination():
    print("\n-- Edit Vaccination Record --")
    view_all_vaccinations()
    vacc_id = input("Enter Vaccination ID to edit: ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Vaccinations WHERE Vaccination_ID = ?", (vacc_id,))
    record = cur.fetchone()
    if not record:
        print("No vaccination record found with that ID."); conn.close(); return

    _, pet_id, vaccine_name, date_administered, next_due_date, veterinarian = record

    print("\n-- Edit (leave blank to keep current value) --")
    new_vaccine = input(f"Vaccine Name [{vaccine_name}]: ").strip() or vaccine_name
    new_date_admin = input(f"Administration Date [{date_administered}]: ").strip() or date_administered
    new_next_due = input(f"Next Due Date [{next_due_date}]: ").strip() or next_due_date
    new_vet = input(f"Veterinarian [{veterinarian}]: ").strip() or veterinarian

    cur.execute(
        """UPDATE Vaccinations
           SET Vaccine_Name=?, Date_Administered=?, Next_Due_Date=?, Veterinarian=?
           WHERE Vaccination_ID=?""",
        (new_vaccine, new_date_admin, new_next_due, new_vet, vacc_id),
    )
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Edited vaccination record {vacc_id}")
    print("Vaccination record updated successfully.")


# ---------------------------------------------------------------------
# 4.3  ALERTS & TRACKING  (Admin only)
# ---------------------------------------------------------------------

def due_date_alerts():
    print("\n-- Vaccination Due Date Alerts --")
    days = input("Show vaccinations due within how many days? [default 30]: ").strip()
    days = int(days) if days.isdigit() else 30

    cutoff = str(date.today() + timedelta(days=days))
    today = str(date.today())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.Name, v.Vaccine_Name, v.Next_Due_Date,
               CASE WHEN v.Next_Due_Date < ? THEN 'OVERDUE' ELSE 'Upcoming' END AS Status
        FROM Vaccinations v
        LEFT JOIN Pets p ON v.Pet_ID = p.Pet_ID
        WHERE v.Next_Due_Date IS NOT NULL AND v.Next_Due_Date <= ?
        ORDER BY v.Next_Due_Date ASC
    """, (today, cutoff))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"No vaccinations due within the next {days} days."); return

    print(tabulate(rows, headers=["Pet Name", "Vaccine", "Next Due Date", "Status"], tablefmt="grid"))
    log_activity(current_user["Username"], "admin", f"Viewed vaccination due-date alerts ({days} day window)")


def flag_medically_ineligible():
    print("\n-- Flag Pet as Medically Ineligible --")
    list_pets()
    pet_id = input("Enter Pet ID to flag: ").strip()

    pet = pet_exists(pet_id)
    if not pet:
        print("No pet found with that ID."); return

    reason = input("Reason / notes (optional): ").strip()

    # BUGFIX: this used to set Adoption_Status to 'Pending' - the exact same
    # status request_adoption() uses for a real adoption request awaiting
    # admin approval. That conflation is a major source of the "pending
    # requests" bug: view_pending_requests() / list_pending_pets() filter
    # on Adoption_Status = 'Pending', so a medically-flagged pet that no
    # one ever asked to adopt would show up mixed in with genuine adoption
    # requests, with no requester on file - and an admin could accidentally
    # "process" it via process_adoption(), creating a bogus adoption
    # transaction for a pet nobody requested. Medically ineligible pets now
    # get their own distinct status so they never enter the adoption-request
    # queue.
    conn = get_connection()
    cur = conn.cursor()
    new_health = "Medically Ineligible" + (f" - {reason}" if reason else "")
    cur.execute("UPDATE Pets SET Health_Status = ? WHERE Pet_ID = ?", (new_health, pet_id))
    cur.execute(
        "UPDATE Pets SET Adoption_Status = 'Unavailable', Requested_By = NULL "
        "WHERE Pet_ID = ? AND Adoption_Status = 'Available'",
        (pet_id,),
    )
    conn.commit()
    conn.close()

    log_activity(current_user["Username"], "admin", f"Flagged Pet ID {pet_id} as medically ineligible")
    print(f"{pet[1]} (Pet ID {pet_id}) has been flagged as medically ineligible for adoption.")


# =======================================================================
# ADOPTER DASHBOARD  (read-only)
# =======================================================================

def adopter_vaccination_dashboard(user):
    global current_user
    current_user = user

    while True:
        print(f"\n--- Vaccination Records ({current_user['Full_Name']}) ---")
        print("1. View All Vaccination Records")
        print("2. View Vaccination Records for a Specific Pet")
        print("3. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                view_all_vaccinations()
            case "2":
                view_vaccinations_for_pet()
            case "3":
                return
            case _:
                print("Invalid option.")


# =======================================================================
# ADMIN DASHBOARD  (full access)
# =======================================================================

def admin_vaccination_dashboard(user):
    global current_user
    current_user = user

    while True:
        print(f"\n--- Manage Vaccination Records ({current_user['Full_Name']}) ---")
        print("1. Record New Vaccination           (4.1)")
        print("2. Edit Vaccination Record           (4.2)")
        print("3. View Vaccination Records          (read-only lookup)")
        print("4. Vaccination Due Date Alerts        (4.3)")
        print("5. Flag Pet as Medically Ineligible   (4.3)")
        print("6. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                record_vaccination()
            case "2":
                edit_vaccination()
            case "3":
                view_all_vaccinations()
            case "4":
                due_date_alerts()
            case "5":
                flag_medically_ineligible()
            case "6":
                return
            case _:
                print("Invalid option.")