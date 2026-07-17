"""
Migration script: adds the Donations table to the database.

Run this once before using the new donations feature. It's safe to run
multiple times - the table is only created if it doesn't already exist,
so it will never touch or duplicate any existing data.

Usage:
    cd "main files"
    python add_donations_table.py
"""

import sqlite3
from db_functions import DB_NAME

SCHEMA = """
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

    cur.executescript(SCHEMA)

    # Migrate a Donations table created before Donor_Email existed - adds
    # the column without touching any existing rows.
    if not column_exists(cur, "Donations", "Donor_Email"):
        print("Migrating: adding Donations.Donor_Email ...")
        cur.execute("ALTER TABLE Donations ADD COLUMN Donor_Email TEXT")
    else:
        print("Donations.Donor_Email already present, nothing to migrate.")

    # Migrate a Donations table created before Status existed. Existing
    # rows predate the Pending/Confirmed workflow, so they're marked
    # Confirmed (they were already treated as real donations).
    if not column_exists(cur, "Donations", "Status"):
        print("Migrating: adding Donations.Status ...")
        cur.execute("ALTER TABLE Donations ADD COLUMN Status TEXT NOT NULL DEFAULT 'Confirmed'")
    else:
        print("Donations.Status already present, nothing to migrate.")

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' is ready - Donations table is in place.")


if __name__ == "__main__":
    main()
