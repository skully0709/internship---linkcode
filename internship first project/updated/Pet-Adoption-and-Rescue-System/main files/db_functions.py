"""
Shared DB connection, auth helpers, and activity logging.
Every module (pet_management, search_menu, vaccinations, adoption_transaction,
module6_analytics, main_file) imports from HERE, never from main_file.
This is what breaks the old circular import.
"""

import sqlite3
import hashlib
import os
import random
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# import mysql.connector   # pip install mysql-connector-python

# Loads variables from a local .env file (never committed to Git) into the
# environment, so SENDER_EMAIL / SENDER_PASSWORD below can be read with
# os.getenv() instead of being hardcoded in this file.
load_dotenv()


DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "petadoption.db")
DB_NAME = os.path.normpath(DB_NAME)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

ROLE_PERMISSIONS = {
    "admin": [1, 2, 3, 4, 5, 6],
    "adopter": [1, 2, 3, 4, 5],
}


def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------------------------------------------------------------
# MYSQL SWITCH
# To move the whole system to MySQL: comment out the sqlite3 get_connection
# above, uncomment this one, uncomment the mysql.connector import at the
# top, and fill in your host/user/password/database.
#
# IMPORTANT: every query in every module uses "?" as the placeholder
# (sqlite3 style). mysql.connector needs "%s" instead, so every
# cur.execute("... WHERE X=?", (val,)) across all files would need its
# "?" changed to "%s". The connection/cursor object itself is used the
# same way after that (cur.execute, cur.fetchone, cur.fetchall,
# cur.rowcount, conn.commit, conn.close) so nothing else changes.
# ---------------------------------------------------------------------

# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="your_mysql_password",
#         database="petadoption",
#     )


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed):
    return hash_password(password) == hashed


def is_valid_email(email):
    return "@" in email and "." in email


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def is_strong_password(password):
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return len(password) >= 8 and has_letter and has_digit


def generate_code():
    return str(random.randint(1000, 9999))


def send_verification_email(to_email, code):

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print(
            "Email not sent: SENDER_EMAIL / SENDER_PASSWORD are not set. "
            "Copy .env.example to .env and fill in your SMTP credentials."
        )
        return

    message = MIMEText(f"Your verification code is: {code}")
    message["Subject"] = "Pet Adoption System - Verification Code"
    message["From"] = SENDER_EMAIL
    message["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        print(f"Verification code sent to {to_email}.")
    except Exception as e:
        print(f"Could not send email ({e}).")


def log_activity(username, role, action):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Activity_log (Username, Role, Action) VALUES (?, ?, ?)",
        (username, role, action),
    )
    conn.commit()
    conn.close()


def table_name(role):
    return "Administrators" if role == "admin" else "Adopters"


def id_column(role):
    return "Admin_Id" if role == "admin" else "Adopter_Id"


def find_user(identifier, role):

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table_name(role)} WHERE Username = ? OR Email = ?",
        (identifier, identifier),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def username_or_email_exists(username, email):
    conn = get_connection()
    cur = conn.cursor()
    for table in ("Adopters", "Administrators"):
        cur.execute(
            f"SELECT 1 FROM {table} WHERE Username = ? OR Email = ?",
            (username, email),
        )
        if cur.fetchone():
            conn.close()
            return True
    conn.close()
    return False


def check_access(role, module_number):
    return module_number in ROLE_PERMISSIONS.get(role, [])


def get_menu(role):
    return ROLE_PERMISSIONS.get(role, [])
