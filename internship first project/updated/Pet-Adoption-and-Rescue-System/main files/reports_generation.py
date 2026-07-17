"""
MODULE 6: Administrative Dashboard & Analytics
Access Level: Admin Only
Owner: Shaun
"""

from datetime import date
from tabulate import tabulate
import matplotlib.pyplot as plt

from db_functions import get_connection


# ---------------------------------------------------------------------
# 6.1  SYSTEM MONITORING
# ---------------------------------------------------------------------

def view_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT Adopter_Id, Full_Name, Email, Username, Status FROM Adopters")
    adopters = cur.fetchall()
    cur.execute("SELECT Admin_Id, Full_Name, Email, Username, Status FROM Administrators")
    admins = cur.fetchall()
    conn.close()

    print("\n-- Adopters --")
    print(tabulate(adopters, headers=["ID", "Full Name", "Email", "Username", "Status"], tablefmt="grid") if adopters else "No adopters found.")
    print("\n-- Administrators --")
    print(tabulate(admins, headers=["ID", "Full Name", "Email", "Username", "Status"], tablefmt="grid") if admins else "No administrators found.")


def view_transactions():
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
        print("No transactions yet."); return
    display = [[r[0], r[1], r[2], r[3], r[4] or "-", "Returned" if r[4] else "Active"] for r in rows]
    print(tabulate(display, headers=["Txn ID", "Pet", "Adopter", "Adoption Date", "Return Date", "Status"], tablefmt="grid"))


# ---------------------------------------------------------------------
# 6.2  REPORT GENERATION
# ---------------------------------------------------------------------

def available_pets_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Pet_ID, Name, Species, Breed, Age, Health_Status
        FROM Pets WHERE Adoption_Status = 'Available'
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No pets currently available."); return
    print(tabulate(rows, headers=["Pet ID", "Name", "Species", "Breed", "Age", "Health"], tablefmt="grid"))


def overdue_vaccinations_report():
    today = str(date.today())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.Name, v.Vaccine_Name, v.Next_Due_Date, v.Veterinarian
        FROM Vaccinations v
        LEFT JOIN Pets p ON v.Pet_ID = p.Pet_ID
        WHERE v.Next_Due_Date IS NOT NULL AND v.Next_Due_Date < ?
        ORDER BY v.Next_Due_Date ASC
    """, (today,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No overdue vaccinations."); return
    print(tabulate(rows, headers=["Pet Name", "Vaccine", "Due Date", "Veterinarian"], tablefmt="grid"))


# ---------------------------------------------------------------------
# 6.3  GRAPHICAL ANALYTICS (Matplotlib)
# ---------------------------------------------------------------------

def plot_adoption_trends():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT strftime('%Y-%m', Adoption_Date) AS Month, COUNT(*)
        FROM Adoption_Transactions
        GROUP BY Month ORDER BY Month
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No adoption data to plot."); return

    months = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(8, 5))
    plt.plot(months, counts, marker="o")
    plt.title("Monthly Adoption Trends")
    plt.xlabel("Month")
    plt.ylabel("Adoptions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_species_distribution():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Species, COUNT(*) FROM Pets GROUP BY Species")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No pet data to plot."); return

    species = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=species, autopct="%1.1f%%")
    plt.title("Pet Species Distribution")
    plt.tight_layout()
    plt.show()


def plot_shelter_occupancy():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.Shelter_Name, s.Capacity, COUNT(p.Pet_ID)
        FROM Shelters s LEFT JOIN Pets p ON s.Shelter_ID = p.Shelter_ID
        GROUP BY s.Shelter_ID
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No shelter data to plot."); return

    names = [r[0] for r in rows]
    capacity = [r[1] for r in rows]
    occupancy = [r[2] for r in rows]

    x = range(len(names))
    plt.figure(figsize=(8, 5))
    plt.bar(x, capacity, width=0.4, label="Capacity", align="center")
    plt.bar([i + 0.4 for i in x], occupancy, width=0.4, label="Occupancy", align="center")
    plt.xticks([i + 0.2 for i in x], names, rotation=45)
    plt.title("Shelter Capacity vs Occupancy")
    plt.ylabel("Pets")
    plt.legend()
    plt.tight_layout()
    plt.show()


# =======================================================================
# ADMIN DASHBOARD
# =======================================================================

def open_dashboard(user):
    while True:
        print(f"\n--- Analytics Dashboard ({user['Full_Name']}) ---")
        print("1. View All Users               (6.1)")
        print("2. View All Transactions         (6.1)")
        print("3. Available Pets Report         (6.2)")
        print("4. Overdue Vaccinations Report   (6.2)")
        print("5. Plot Adoption Trends          (6.3)")
        print("6. Plot Species Distribution     (6.3)")
        print("7. Plot Shelter Occupancy        (6.3)")
        print("8. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                view_all_users()
            case "2":
                view_transactions()
            case "3":
                available_pets_report()
            case "4":
                overdue_vaccinations_report()
            case "5":
                plot_adoption_trends()
            case "6":
                plot_species_distribution()
            case "7":
                plot_shelter_occupancy()
            case "8":
                return
            case _:
                print("Invalid option.")
