"""
MODULE 1: System Access & User Management
Real-Time Pet Adoption & Rescue Management System
Owner: Sarthak

Contains all functions: registration, login, profile, dashboards.
Run the system with run.py, not this file.
"""

from tabulate import tabulate

from db_functions import (
    get_connection, hash_password, verify_password, needs_rehash, is_valid_email,
    is_valid_phone, is_strong_password, is_valid_username, generate_code,
    send_verification_email, verify_with_otp, get_non_empty_input, pause,
    log_activity, table_name, id_column, find_user, username_or_email_exists,
    email_exists, username_exists, phone_exists,
)

from pet_management import pet_management_menu_admin
from search_menu import search_menu
from vaccinations import admin_vaccination_dashboard, adopter_vaccination_dashboard
from adoption_transaction import adopter_adoption_dashboard, admin_adoption_dashboard
from donations import adopter_donation_dashboard, admin_donation_dashboard
from reports_generation import open_dashboard


# ---------------------------------------------------------------------
# 1.1  SYSTEM ENTRY & ROLE SELECTION
# ---------------------------------------------------------------------

def main_menu():
    print("\n===== PET ADOPTION & RESCUE MANAGEMENT SYSTEM =====")
    print("1. Login as Adopter")
    print("2. Login as Administrator")
    print("3. Create Account")
    print("4. Forgot Password")
    print("5. Exit")
    choice = input("Select an option: ").strip()

    try:
        match choice:
            case "1":
                login("adopter")
            case "2":
                login("admin")
            case "3":
                register_adopter()
            case "4":
                role = input("Reset password for (adopter/admin): ").strip().lower()
                forgot_password(role)
            case "5":
                print("Goodbye.")
                return
            case _:
                print("Invalid option.")
    except KeyboardInterrupt:
        print("\n\nInterrupted. Returning to the main menu...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    main_menu()


# ---------------------------------------------------------------------
# 1.2  ADOPTER REGISTRATION
# ---------------------------------------------------------------------

def register_adopter():
    print("\n-- Adopter Registration --")
    full_name = get_non_empty_input("Full Name: ")

    while True:
        email = get_non_empty_input("Email Address: ")
        if not is_valid_email(email):
            print("Invalid email format."); continue
        if email_exists(email):
            print("An account with this email already exists."); continue
        break

    while True:
        phone = get_non_empty_input("Phone Number (10 digits): ")
        if not is_valid_phone(phone):
            print("Invalid phone number. It must be exactly 10 digits."); continue
        if phone_exists(phone):
            print("An account with this phone number already exists."); continue
        break

    location = input("Location/Address: ").strip()

    while True:
        username = get_non_empty_input("Choose a Username: ")
        if not is_valid_username(username):
            print("Usernames must be 3-20 characters: letters, numbers, or underscores only."); continue
        if username_exists(username):
            print("That username is already taken."); continue
        break

    while True:
        password = get_non_empty_input("Set a Password: ")
        strong, reason = is_strong_password(password)
        if not strong:
            print(reason); continue
        confirm = get_non_empty_input("Confirm Password: ")
        if password != confirm:
            print("Passwords do not match."); continue
        break

    if not verify_with_otp(email):
        print("Verification failed. Registration cancelled."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Adopters (Full_Name, Email, Phone, Location, Username, Password_Hash)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (full_name, email, phone, location, username, hash_password(password)),
    )
    conn.commit()
    conn.close()

    log_activity(username, "adopter", "Account registered")
    print(f"Registration successful! Welcome, {full_name}.")


# ---------------------------------------------------------------------
# 1.3  LOGIN
# ---------------------------------------------------------------------

def login(role):
    print(f"\n-- {role.capitalize()} Login --")
    identifier = get_non_empty_input("Username or Email: ")
    password = get_non_empty_input("Password: ")

    user = find_user(identifier, role)
    if not user:
        print("Account not found."); return
    if user["Status"] == "inactive":
        print("This account is deactivated."); return
    if not verify_password(password, user["Password_Hash"]):
        print("Incorrect password."); return

    if needs_rehash(user["Password_Hash"]):
        new_hash = hash_password(password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"UPDATE {table_name(role)} SET Password_Hash=? WHERE Username=?", (new_hash, user["Username"]))
        conn.commit()
        conn.close()
        user["Password_Hash"] = new_hash

    if not verify_with_otp(user["Email"]):
        print("Verification failed. Login cancelled."); return

    log_activity(user["Username"], role, "Logged in")
    print(f"\nLogin successful. Welcome, {user['Full_Name']}!")

    if role == "admin":
        admin_dashboard(user)
    else:
        adopter_dashboard(user)


# ---------------------------------------------------------------------
# 1.4  PROFILE MANAGEMENT (shared helpers)
# ---------------------------------------------------------------------

def view_profile(user):
    rows = [
        ["Full Name", user["Full_Name"]],
        ["Email", user["Email"]],
        ["Phone", user["Phone"]],
        ["Location", user.get("Location", "-")],
        ["Username", user["Username"]],
        ["Status", user["Status"]],
    ]
    print(tabulate(rows, headers=["Field", "Value"], tablefmt="grid"))


def edit_profile(user, role):
    print("\n-- Edit Profile (leave blank to keep current value) --")
    full_name = input(f"Full Name [{user['Full_Name']}]: ").strip() or user["Full_Name"]

    while True:
        email = input(f"Email [{user['Email']}]: ").strip() or user["Email"]
        if not is_valid_email(email):
            print("Invalid email format."); continue
        if email != user["Email"] and email_exists(email):
            print("That email is already in use by another account."); continue
        break

    while True:
        phone = input(f"Phone [{user['Phone']}]: ").strip() or user["Phone"]
        if not is_valid_phone(phone):
            print("Invalid phone number. It must be exactly 10 digits."); continue
        if phone != user["Phone"] and phone_exists(phone):
            print("That phone number is already in use by another account."); continue
        break

    location = input(f"Location [{user.get('Location', '-')}]: ").strip() or user.get("Location", "")

    conn = get_connection()
    cur = conn.cursor()
    if role == "adopter":
        cur.execute(
            "UPDATE Adopters SET Full_Name=?, Email=?, Phone=?, Location=? WHERE Username=?",
            (full_name, email, phone, location, user["Username"]),
        )
    else:
        cur.execute(
            "UPDATE Administrators SET Full_Name=?, Email=?, Phone=? WHERE Username=?",
            (full_name, email, phone, user["Username"]),
        )
    conn.commit()
    conn.close()

    user.update({"Full_Name": full_name, "Email": email, "Phone": phone, "Location": location})
    log_activity(user["Username"], role, "Profile updated")
    print("Profile updated successfully.")
    return user


# ---------------------------------------------------------------------
# 1.5  PASSWORD & SECURITY
# ---------------------------------------------------------------------

def change_password(user, role):
    current = get_non_empty_input("Current Password: ")
    if not verify_password(current, user["Password_Hash"]):
        print("Current password is incorrect."); return

    while True:
        new_pw = get_non_empty_input("New Password: ")
        strong, reason = is_strong_password(new_pw)
        if not strong:
            print(reason); continue
        confirm = get_non_empty_input("Confirm New Password: ")
        if new_pw != confirm:
            print("Passwords do not match."); continue
        break

    new_hash = hash_password(new_pw)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE {table_name(role)} SET Password_Hash=? WHERE Username=?",
        (new_hash, user["Username"]),
    )
    conn.commit()
    conn.close()

    user["Password_Hash"] = new_hash
    log_activity(user["Username"], role, "Password changed")
    print("Password changed successfully.")


def forgot_password(role):
    identifier = get_non_empty_input("Enter your registered Username or Email: ")
    user = find_user(identifier, role)
    if not user:
        print("No matching account found."); return

    if not verify_with_otp(user["Email"]):
        print("Verification failed."); return

    while True:
        new_pw = get_non_empty_input("Enter New Password: ")
        strong, reason = is_strong_password(new_pw)
        if not strong:
            print(reason); continue
        confirm = get_non_empty_input("Confirm New Password: ")
        if new_pw != confirm:
            print("Passwords do not match."); continue
        break

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE {table_name(role)} SET Password_Hash=? WHERE Username=?",
        (hash_password(new_pw), user["Username"]),
    )
    conn.commit()
    conn.close()

    log_activity(user["Username"], role, "Password reset via recovery")
    print("Password reset successful. You can now log in.")


# ---------------------------------------------------------------------
# 1.6  ADMINISTRATOR PRIVILEGE MANAGEMENT
# ---------------------------------------------------------------------

def elevate_to_admin(admin_user):
    username = input("Enter the username of the Adopter to elevate: ").strip()
    target = find_user(username, "adopter")
    if not target:
        print("Adopter not found."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Adopters WHERE Username=?", (username,))
    cur.execute(
        """INSERT INTO Administrators (Full_Name, Email, Phone, Username, Password_Hash, Granted_By)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (target["Full_Name"], target["Email"], target["Phone"],
         target["Username"], target["Password_Hash"], admin_user["Username"]),
    )
    conn.commit()
    conn.close()

    log_activity(admin_user["Username"], "admin", f"Elevated {username} to Admin")
    print(f"{target['Full_Name']} has been elevated to Administrator.")


def create_admin_directly(admin_user):
    print("\n-- Register New Administrator --")
    full_name = get_non_empty_input("Full Name: ")

    while True:
        email = get_non_empty_input("Email Address: ")
        if not is_valid_email(email):
            print("Invalid email format."); continue
        if email_exists(email):
            print("An account with this email already exists."); continue
        break

    while True:
        phone = get_non_empty_input("Phone Number (10 digits): ")
        if not is_valid_phone(phone):
            print("Invalid phone number. It must be exactly 10 digits."); continue
        if phone_exists(phone):
            print("An account with this phone number already exists."); continue
        break

    while True:
        username = get_non_empty_input("Username: ")
        if not is_valid_username(username):
            print("Usernames must be 3-20 characters: letters, numbers, or underscores only."); continue
        if username_exists(username):
            print("That username is already taken."); continue
        break

    while True:
        password = get_non_empty_input("Password: ")
        strong, reason = is_strong_password(password)
        if strong:
            break
        print(reason)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Administrators (Full_Name, Email, Phone, Username, Password_Hash, Granted_By)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (full_name, email, phone, username, hash_password(password), admin_user["Username"]),
    )
    conn.commit()
    conn.close()

    log_activity(admin_user["Username"], "admin", f"Created new admin {username}")
    print(f"Administrator '{full_name}' created successfully.")


# ---------------------------------------------------------------------
# 1.8  ACCOUNT STATUS & ACTIVITY
# ---------------------------------------------------------------------

def set_account_status(username, role, new_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE {table_name(role)} SET Status=? WHERE Username=?",
        (new_status, username),
    )
    conn.commit()
    conn.close()
    log_activity(username, role, f"Account set to {new_status}")
    print(f"Account '{username}' is now {new_status}.")


def delete_account(user, role):
    confirm = input(f"Type 'DELETE' to permanently delete account '{user['Username']}': ").strip()
    if confirm != "DELETE":
        print("Deletion cancelled."); return False

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name(role)} WHERE Username=?", (user["Username"],))
    conn.commit()
    conn.close()

    log_activity(user["Username"], role, "Account deleted")
    print("Account deleted successfully.")
    return True


def view_activity_log(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT Log_Time, Action FROM Activity_log WHERE Username=? ORDER BY Log_Time DESC",
        (username,),
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No activity recorded yet."); return
    print(tabulate(rows, headers=["Timestamp", "Action"], tablefmt="grid"))


def list_users(role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT {id_column(role)}, Full_Name, Email, Username, Status FROM {table_name(role)}")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"No {role}s found."); return
    print(tabulate(rows, headers=["ID", "Full Name", "Email", "Username", "Status"], tablefmt="grid"))


# =======================================================================
# ADOPTER DASHBOARD
# =======================================================================

def adopter_dashboard(user):
    while True:
        print(f"\n===== ADOPTER DASHBOARD ({user['Full_Name']}) =====")
        print("1. My Account")
        print("2. Pets & Adoption")
        print("3. Donations")
        print("4. Logout")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    if adopter_account_menu(user) == "deleted":
                        return
                case "2":
                    adopter_pets_menu(user)
                case "3":
                    adopter_donation_dashboard(user)
                case "4":
                    print("Logged out.")
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


def adopter_account_menu(user):
    while True:
        print(f"\n--- My Account ({user['Full_Name']}) ---")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. Change Password")
        print("4. View My Activity Log")
        print("5. Deactivate My Account")
        print("6. Delete My Account")
        print("7. Back")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    view_profile(user)
                case "2":
                    user = edit_profile(user, "adopter")
                case "3":
                    change_password(user, "adopter")
                case "4":
                    view_activity_log(user["Username"])
                case "5":
                    set_account_status(user["Username"], "adopter", "inactive")
                    return "deleted"
                case "6":
                    if delete_account(user, "adopter"):
                        return "deleted"
                case "7":
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


def adopter_pets_menu(user):
    while True:
        print(f"\n--- Pets & Adoption ---")
        print("1. Browse / Search Available Pets ")
        print("2. View Pet Vaccination Records ")
        print("3. Request Adoption / My History ")
        print("4. Back")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    search_menu(user)
                case "2":
                    adopter_vaccination_dashboard(user)
                case "3":
                    adopter_adoption_dashboard(user)
                case "4":
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


# =======================================================================
# ADMIN DASHBOARD
# =======================================================================

def admin_dashboard(user):
    while True:
        print(f"\n===== ADMIN DASHBOARD ({user['Full_Name']}) =====")
        print("1. My Account")
        print("2. User Management")
        print("3. Pets, Medical & Adoptions")
        print("4. Donation Management")
        print("5. Analytics Dashboard")
        print("6. Logout")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    user = admin_account_menu(user)
                case "2":
                    admin_user_management_menu(user)
                case "3":
                    admin_pets_menu(user)
                case "4":
                    admin_donation_dashboard(user)
                case "5":
                    open_dashboard(user)
                case "6":
                    print("Logged out.")
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


def admin_account_menu(user):
    while True:
        print(f"\n--- My Account ({user['Full_Name']}) ---")
        print("1. View Profile")
        print("2. Edit Profile")
        print("3. Change Password")
        print("4. View My Activity Log")
        print("5. Back")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    view_profile(user)
                case "2":
                    user = edit_profile(user, "admin")
                case "3":
                    change_password(user, "admin")
                case "4":
                    view_activity_log(user["Username"])
                case "5":
                    return user
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


def admin_user_management_menu(user):
    while True:
        print(f"\n--- User Management ({user['Full_Name']}) ---")
        print("1. Elevate Adopter to Admin")
        print("2. Register New Admin Directly")
        print("3. View All Adopters")
        print("4. View All Admins")
        print("5. Activate/Deactivate a User")
        print("6. Back")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    elevate_to_admin(user)
                case "2":
                    create_admin_directly(user)
                case "3":
                    list_users("adopter")
                case "4":
                    list_users("admin")
                case "5":
                    target = get_non_empty_input("Username to update: ")
                    target_role = input("Role (adopter/admin): ").strip().lower()
                    action = input("Activate or Deactivate? (a/d): ").strip().lower()
                    set_account_status(target, target_role, "active" if action == "a" else "inactive")
                case "6":
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()


def admin_pets_menu(user):
    while True:
        print(f"\n--- Pets, Medical & Adoptions ({user['Full_Name']}) ---")
        print("1. Manage Pet Inventory  ")
        print("2. Search Pets    ")
        print("3. Manage Vaccination Records ")
        print("4. Process Adoption Requests  ")
        print("5. Back")
        choice = input("Select an option: ").strip()

        try:
            match choice:
                case "1":
                    pet_management_menu_admin(user)
                case "2":
                    search_menu(user)
                case "3":
                    admin_vaccination_dashboard(user)
                case "4":
                    admin_adoption_dashboard(user)
                case "5":
                    return
                case _:
                    print("Invalid option.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        pause()
