"""
Database setup / migration script.

Run this once before starting the app for the first time (creates every
table if it doesn't exist yet), and also any time after pulling this fix
(it safely adds the new Pets.Requested_By column to an existing database
without touching your existing data).

Usage:
    python "main files/db_setup.py"

Safe to run multiple times - every statement is guarded so it only makes
a change if that change hasn't been made yet.
"""

import sqlite3
from db_functions import DB_NAME

SCHEMA = """
CREATE TABLE IF NOT EXISTS Administrators (
    Admin_Id       INTEGER PRIMARY KEY AUTOINCREMENT,
    Full_Name      TEXT NOT NULL,
    Email          TEXT NOT NULL UNIQUE,
    Phone          TEXT,
    Username       TEXT NOT NULL UNIQUE,
    Password_Hash  TEXT NOT NULL,
    Status         TEXT NOT NULL DEFAULT 'active',
    Granted_By     TEXT,
    FOREIGN KEY (Granted_By) REFERENCES Administrators(Username)
);

CREATE TABLE IF NOT EXISTS Adopters (
    Adopter_Id     INTEGER PRIMARY KEY AUTOINCREMENT,
    Full_Name      TEXT NOT NULL,
    Email          TEXT NOT NULL UNIQUE,
    Phone          TEXT,
    Location       TEXT,
    Username       TEXT NOT NULL UNIQUE,
    Password_Hash  TEXT NOT NULL,
    Status         TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS Activity_log (
    Log_Id         INTEGER PRIMARY KEY AUTOINCREMENT,
    Username       TEXT NOT NULL,
    Role           TEXT NOT NULL,
    Action         TEXT NOT NULL,
    Log_Time       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Shelters (
    Shelter_ID     INTEGER PRIMARY KEY AUTOINCREMENT,
    Shelter_Name   TEXT NOT NULL,
    Location       TEXT NOT NULL,
    Capacity       INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Pets (
    Pet_ID          INTEGER PRIMARY KEY AUTOINCREMENT,
    Name            TEXT NOT NULL,
    Species         TEXT NOT NULL,
    Breed           TEXT,
    Age             INTEGER,
    Health_Status   TEXT,
    Adoption_Status TEXT,
    Shelter_ID      INTEGER,
    Requested_By    INTEGER,
    FOREIGN KEY (Shelter_ID) REFERENCES Shelters(Shelter_ID),
    FOREIGN KEY (Requested_By) REFERENCES Adopters(Adopter_Id)
);

CREATE TABLE IF NOT EXISTS Vaccinations (
    Vaccination_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
    Pet_ID            INTEGER,
    Vaccine_Name      TEXT NOT NULL,
    Date_Administered TEXT NOT NULL,
    Next_Due_Date     TEXT,
    Veterinarian      TEXT,
    FOREIGN KEY (Pet_ID) REFERENCES Pets(Pet_ID)
);

CREATE TABLE IF NOT EXISTS Adoption_Transactions (
    Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Pet_ID         INTEGER,
    Adopter_Id     INTEGER,
    Adoption_Date  TEXT NOT NULL,
    Return_Date    TEXT,
    FOREIGN KEY (Pet_ID) REFERENCES Pets(Pet_ID),
    FOREIGN KEY (Adopter_Id) REFERENCES Adopters(Adopter_Id)
);

CREATE TABLE IF NOT EXISTS Donations (
    Donation_ID    INTEGER PRIMARY KEY AUTOINCREMENT,
    Adopter_Id     INTEGER,
    Donor_Name     TEXT,
    Donor_Email    TEXT,
    Amount         REAL NOT NULL,
    Donation_Date  TEXT NOT NULL,
    Payment_Method TEXT,
    Purpose        TEXT,
    Notes          TEXT,
    Recorded_By    TEXT,
    Status         TEXT NOT NULL DEFAULT 'Confirmed',
    FOREIGN KEY (Adopter_Id) REFERENCES Adopters(Adopter_Id)
);
"""


def column_exists(cur, table, column):
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 1. Create any missing tables (no-ops if the DB already has them).
    cur.executescript(SCHEMA)

    # 2. Migrate an existing Pets table that predates this fix: add the
    #    Requested_By column used to link a pending request to the adopter
    #    who made it. This is what request_adoption() / process_adoption()
    #    now rely on to stop mismatching adopters and transactions.
    if not column_exists(cur, "Pets", "Requested_By"):
        print("Migrating: adding Pets.Requested_By ...")
        cur.execute("ALTER TABLE Pets ADD COLUMN Requested_By INTEGER REFERENCES Adopters(Adopter_Id)")
    else:
        print("Pets.Requested_By already present, nothing to migrate.")

    # 3. Migrate an existing Donations table that predates the invoice
    #    feature: add the Donor_Email column used to email a receipt to
    #    walk-in donors who aren't registered Adopters.
    if not column_exists(cur, "Donations", "Donor_Email"):
        print("Migrating: adding Donations.Donor_Email ...")
        cur.execute("ALTER TABLE Donations ADD COLUMN Donor_Email TEXT")
    else:
        print("Donations.Donor_Email already present, nothing to migrate.")

    # 4. Migrate an existing Donations table that predates the
    #    Pending/Confirmed workflow: add Status, defaulting existing rows
    #    to Confirmed since they were already treated as real donations.
    if not column_exists(cur, "Donations", "Status"):
        print("Migrating: adding Donations.Status ...")
        cur.execute("ALTER TABLE Donations ADD COLUMN Status TEXT NOT NULL DEFAULT 'Confirmed'")
    else:
        print("Donations.Status already present, nothing to migrate.")

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' is ready.")


if __name__ == "__main__":
    main()
