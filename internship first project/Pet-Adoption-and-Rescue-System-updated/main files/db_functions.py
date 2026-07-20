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
import re
import smtplib
import bcrypt
from datetime import datetime, timedelta
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

OTP_LENGTH = 6
OTP_VALIDITY_MINUTES = 5
OTP_MAX_ATTEMPTS = 3

BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
SPECIAL_CHAR_PATTERN = re.compile(r"[!@#$%^&*()\-_=+\[\]{}|;:'\",.<>/?`~\\]")

# Shared condition for "actually available" - a pet only counts if its
# status says Available AND its health status isn't a medical-ineligibility
# flag, so listings stay correct even if the two ever fall out of sync.
AVAILABLE_SQL = (
    "Adoption_Status = 'Available' "
    "AND (Health_Status IS NULL OR Health_Status NOT LIKE 'Medically Ineligible%')"
)


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
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password, hashed):
    if not password or not hashed:
        return False

    if hashed.startswith(BCRYPT_PREFIXES):
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except (ValueError, TypeError):
            return False

    # Legacy SHA-256 hash from before the bcrypt switch. Still verified so
    # existing accounts keep working; login() upgrades it to bcrypt on the
    # next successful sign-in.
    return hashlib.sha256(password.encode()).hexdigest() == hashed


def needs_rehash(hashed):
    return not (hashed or "").startswith(BCRYPT_PREFIXES)


def is_valid_email(email):
    return bool(email) and bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def is_strong_password(password):
    """Returns (True, "") if `password` satisfies every strength rule,
    otherwise (False, "reason for failure")."""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not SPECIAL_CHAR_PATTERN.search(password):
        return False, "Password must contain at least one special character."
    return True, ""


def is_valid_username(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,20}", username))


def is_medically_ineligible(health_status):
    return bool(health_status) and health_status.startswith("Medically Ineligible")


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field can't be empty.")


def pause():
    input("\nPress Enter to continue...")


def generate_code():
    return "".join(str(random.randint(0, 9)) for _ in range(OTP_LENGTH))


def send_verification_email(to_email, code):

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print(
            "Email not sent: SENDER_EMAIL / SENDER_PASSWORD are not set. "
            "Copy .env.example to .env and fill in your SMTP credentials."
        )
        return

    message = MIMEText(
        f"Your verification code is: {code}\n"
        f"This code expires in {OTP_VALIDITY_MINUTES} minutes."
    )
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


def verify_with_otp(email):
    """Sends a verification code to `email` and walks the user through a
    numbered menu to enter it, request a fresh one, or cancel - so a resend
    never requires retyping anything else. Returns True once the right code
    is entered, False on cancel, expiry, or too many wrong attempts."""
    code = generate_code()
    expiry_time = datetime.now() + timedelta(minutes=OTP_VALIDITY_MINUTES)
    send_verification_email(email, code)
    print(f"OTP expires in {OTP_VALIDITY_MINUTES} minutes.")
    attempts = 0

    while True:
        if datetime.now() > expiry_time:
            print("\nOTP has expired.")
            return False

        print("\n========== EMAIL VERIFICATION ==========")
        print("1. Enter OTP")
        print("2. Resend OTP")
        print("3. Cancel")
        choice = input("Enter Choice : ").strip()

        if choice == "1":
            entered = input("Enter OTP : ").strip()

            if entered == code:
                print("\nEmail Verified Successfully.\n")
                return True

            attempts += 1
            remaining = OTP_MAX_ATTEMPTS - attempts
            if remaining > 0:
                print(f"\nIncorrect OTP. Attempts Remaining : {remaining}")
            else:
                print("\nMaximum attempts exceeded.")
                return False

        elif choice == "2":
            code = generate_code()
            expiry_time = datetime.now() + timedelta(minutes=OTP_VALIDITY_MINUTES)
            send_verification_email(email, code)
            print(f"\nA new OTP has been sent. It expires in {OTP_VALIDITY_MINUTES} minutes.")

        elif choice == "3":
            print("\nVerification Cancelled.")
            return False

        else:
            print("\nInvalid Choice.")


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


def email_exists(email):
    conn = get_connection()
    cur = conn.cursor()
    for table in ("Adopters", "Administrators"):
        cur.execute(f"SELECT 1 FROM {table} WHERE Email = ?", (email,))
        if cur.fetchone():
            conn.close()
            return True
    conn.close()
    return False


def username_exists(username):
    conn = get_connection()
    cur = conn.cursor()
    for table in ("Adopters", "Administrators"):
        cur.execute(f"SELECT 1 FROM {table} WHERE Username = ?", (username,))
        if cur.fetchone():
            conn.close()
            return True
    conn.close()
    return False


def phone_exists(phone):
    conn = get_connection()
    cur = conn.cursor()
    for table in ("Adopters", "Administrators"):
        cur.execute(f"SELECT 1 FROM {table} WHERE Phone = ?", (phone,))
        if cur.fetchone():
            conn.close()
            return True
    conn.close()
    return False


def check_access(role, module_number):
    return module_number in ROLE_PERMISSIONS.get(role, [])


def get_menu(role):
    return ROLE_PERMISSIONS.get(role, [])
