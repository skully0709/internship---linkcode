"""
MODULE: Donation Management
Real-Time Pet Adoption & Rescue Management System
Access Level: Adopter (Donate & View Own History) | Admin (Record & View All History)

Run "add_donations_table.py" once before using this module - it creates
the Donations table that everything here relies on.
"""

from datetime import date
from tabulate import tabulate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from db_functions import (
    get_connection, log_activity, find_user,
    SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD,
)

PAYMENT_METHODS = ["Cash", "Card", "UPI", "Bank Transfer", "Other"]
PURPOSES = ["General Fund", "Medical Care", "Shelter Support", "Pet Sponsorship", "Other"]


# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------

def is_valid_amount(amount_str):
    try:
        amount = float(amount_str)
    except ValueError:
        return None
    if amount <= 0:
        return None
    return amount


def choose_from_list(label, options):
    print(f"\n{label}:")
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    choice = input(f"Select {label.lower()} (number, or leave blank for 'Other'): ").strip()
    if not choice:
        return "Other"
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]
    return "Other"


def insert_donation(adopter_id, donor_name, amount, payment_method, purpose, notes, recorded_by,
                     donor_email=None, status="Confirmed"):
    donation_date = str(date.today())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO Donations
           (Adopter_Id, Donor_Name, Donor_Email, Amount, Donation_Date, Payment_Method, Purpose, Notes, Recorded_By, Status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (adopter_id, donor_name, donor_email, amount, donation_date, payment_method, purpose, notes, recorded_by, status),
    )
    conn.commit()
    donation_id = cur.lastrowid
    conn.close()
    return donation_id, donation_date



# ---------------------------------------------------------------------
# INVOICE EMAIL
# ---------------------------------------------------------------------

def build_invoice_text(donation_id, donor_name, amount, donation_date, payment_method, purpose, notes):
    return f"""Pet Adoption & Rescue Management System
Donation Invoice / Receipt

Invoice No:      #{donation_id:06d}
Date:            {donation_date}
Donor:           {donor_name}

Amount Donated:  {amount:.2f}
Payment Method:  {payment_method}
Purpose:         {purpose}
Notes:           {notes or '-'}

Thank you so much for your generosity, {donor_name}. Donations like yours
directly fund shelter, food, and medical care for animals waiting for a
home, and help us find them one. Every contribution, big or small, makes
a real difference in an animal's life - we're deeply grateful you chose
to support that work.

With gratitude,
The Pet Adoption & Rescue Management Team

This is an automated receipt for your records. Please keep it for your
files - no action is required from you.
"""


def build_invoice_html(donation_id, donor_name, amount, donation_date, payment_method, purpose, notes):
    return f"""\
<html>
  <body style="margin:0; padding:0; background-color:#f2f4f3; font-family:Segoe UI, Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f2f4f3; padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="560" cellpadding="0" cellspacing="0"
                 style="background-color:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,0.08);">

            <tr>
              <td style="background-color:#2f6f4f; padding:28px 32px;">
                <div style="color:#ffffff; font-size:20px; font-weight:600;">🐾 Pet Adoption &amp; Rescue Management System</div>
                <div style="color:#dcefe3; font-size:13px; margin-top:4px;">Donation Invoice / Receipt</div>
              </td>
            </tr>

            <tr>
              <td style="padding:28px 32px 8px 32px;">
                <p style="font-size:15px; color:#222222; margin:0 0 4px 0;">Dear {donor_name},</p>
                <p style="font-size:14px; color:#555555; line-height:1.5; margin:0 0 20px 0;">
                  Thank you for your donation. Here is your official receipt.
                </p>
              </td>
            </tr>

            <tr>
              <td style="padding:0 32px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                       style="border:1px solid #e6e6e6; border-radius:8px; overflow:hidden;">
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888; border-bottom:1px solid #f0f0f0;">Invoice No.</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; border-bottom:1px solid #f0f0f0; text-align:right;">#{donation_id:06d}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888; border-bottom:1px solid #f0f0f0;">Date</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; border-bottom:1px solid #f0f0f0; text-align:right;">{donation_date}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888; border-bottom:1px solid #f0f0f0;">Donor</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; border-bottom:1px solid #f0f0f0; text-align:right;">{donor_name}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888; border-bottom:1px solid #f0f0f0;">Payment Method</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; border-bottom:1px solid #f0f0f0; text-align:right;">{payment_method}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888; border-bottom:1px solid #f0f0f0;">Purpose</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; border-bottom:1px solid #f0f0f0; text-align:right;">{purpose}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 16px; font-size:13px; color:#888888;">Notes</td>
                    <td style="padding:10px 16px; font-size:13px; color:#222222; text-align:right;">{notes or '-'}</td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding:20px 32px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                       style="background-color:#eef7f1; border-radius:8px;">
                  <tr>
                    <td style="padding:16px 20px; font-size:13px; color:#2f6f4f; font-weight:600;">Total Donated</td>
                    <td style="padding:16px 20px; font-size:22px; color:#2f6f4f; font-weight:700; text-align:right;">{amount:.2f}</td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding:4px 32px 28px 32px;">
                <p style="font-size:14px; color:#333333; line-height:1.6; margin:0;">
                  <strong>Thank you so much for your generosity, {donor_name}.</strong> Donations like
                  yours directly fund shelter, food, and medical care for animals waiting for a home,
                  and help us find them one. Every contribution, big or small, makes a real difference
                  in an animal's life &mdash; we're deeply grateful you chose to support that work.
                </p>
                <p style="font-size:14px; color:#333333; line-height:1.6; margin:16px 0 0 0;">
                  With gratitude,<br/>
                  <strong>The Pet Adoption &amp; Rescue Management Team</strong>
                </p>
              </td>
            </tr>

            <tr>
              <td style="background-color:#fafafa; padding:16px 32px; border-top:1px solid #eeeeee;">
                <p style="font-size:11px; color:#999999; margin:0;">
                  This is an automated receipt for your records. Please keep it for your files &mdash;
                  no action is required from you.
                </p>
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def send_donation_invoice(to_email, donation_id, donor_name, amount, donation_date, payment_method, purpose, notes):
    """Emails a formatted invoice + thank-you note for a donation.
    Returns True if the email was sent, False otherwise (missing SMTP
    config or missing/invalid recipient address are both non-fatal -
    the donation itself is already saved either way)."""

    if not to_email:
        print("No email on file for this donor - invoice not sent.")
        return False

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print(
            "Invoice not sent: SENDER_EMAIL / SENDER_PASSWORD are not set. "
            "Copy .env.example to .env and fill in your SMTP credentials."
        )
        return False

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Donation Receipt #{donation_id:06d} - Thank You!"
    message["From"] = SENDER_EMAIL
    message["To"] = to_email

    message.attach(MIMEText(
        build_invoice_text(donation_id, donor_name, amount, donation_date, payment_method, purpose, notes),
        "plain",
    ))
    message.attach(MIMEText(
        build_invoice_html(donation_id, donor_name, amount, donation_date, payment_method, purpose, notes),
        "html",
    ))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        print(f"Invoice emailed to {to_email}.")
        return True
    except Exception as e:
        print(f"Could not send invoice email ({e}).")
        return False


# ---------------------------------------------------------------------
# ADOPTER SIDE - MAKE A DONATION
# ---------------------------------------------------------------------

def pending_instructions(payment_method, amount):
    if payment_method == "Cash":
        return (
            f"Please hand {amount:.2f} in cash to a shelter admin/staff member. "
            "Your donation will show as Confirmed, and you'll get an emailed receipt, "
            "once they've received it and confirm it in the system."
        )
    return (
        f"Please complete your {amount:.2f} payment via {payment_method} on your end. "
        "An admin will confirm receipt once it reflects, and you'll get an emailed "
        "receipt at that point."
    )


def make_donation(user):
    print("\n-- Make a Donation --")
    amount = is_valid_amount(input("Donation Amount: ").strip())
    if amount is None:
        print("Invalid amount. Enter a number greater than 0."); return

    payment_method = choose_from_list("Payment Method", PAYMENT_METHODS)
    purpose = choose_from_list("Purpose", PURPOSES)
    notes = input("Notes (optional): ").strip() or None

    # Self-reported by the adopter, so it can't be treated as money already
    # received - it stays Pending until an admin confirms it actually
    # arrived (cash in hand, checked the bank/UPI app, etc.). No invoice
    # goes out yet, because it isn't true yet that a donation happened.
    donation_id, donation_date = insert_donation(
        adopter_id=user["Adopter_Id"],
        donor_name=user["Full_Name"],
        amount=amount,
        payment_method=payment_method,
        purpose=purpose,
        notes=notes,
        recorded_by=user["Username"],
        donor_email=user["Email"],
        status="Pending",
    )

    log_activity(user["Username"], "adopter", f"Logged a pending donation of {amount:.2f} (Donation ID {donation_id})")
    print(f"\nYour donation of {amount:.2f} has been logged as PENDING (Donation ID {donation_id}).")
    print(pending_instructions(payment_method, amount))


# ---------------------------------------------------------------------
# ADOPTER SIDE - VIEW MY DONATION HISTORY
# ---------------------------------------------------------------------

def view_my_donation_history(user):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT Donation_ID, Donation_Date, Amount, Payment_Method, Purpose, COALESCE(Notes, '-'), Status
           FROM Donations
           WHERE Adopter_Id = ?
           ORDER BY Donation_ID DESC""",
        (user["Adopter_Id"],),
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("You haven't made any donations yet."); return

    display = [[r[0], r[1], f"{r[2]:.2f}", r[3], r[4], r[5], r[6]] for r in rows]
    print(tabulate(
        display,
        headers=["Donation ID", "Date", "Amount", "Payment Method", "Purpose", "Notes", "Status"],
        tablefmt="grid",
    ))
    confirmed_total = sum(r[2] for r in rows if r[6] == "Confirmed")
    pending_total = sum(r[2] for r in rows if r[6] == "Pending")
    print(f"Confirmed total: {confirmed_total:.2f}" + (f"  |  Pending confirmation: {pending_total:.2f}" if pending_total else ""))


# ---------------------------------------------------------------------
# ADMIN SIDE - RECORD A DONATION
# ---------------------------------------------------------------------

def record_donation_admin(admin_user):
    print("\n-- Record a Donation --")
    print("1. On behalf of a registered Adopter")
    print("2. From a walk-in / offline donor (not in the system)")
    choice = input("Select an option: ").strip()

    adopter_id = None
    donor_name = None
    donor_email = None

    if choice == "1":
        username = input("Adopter's Username: ").strip()
        adopter = find_user(username, "adopter")
        if not adopter:
            print("No adopter found with that username."); return
        adopter_id = adopter["Adopter_Id"]
        donor_name = adopter["Full_Name"]
        donor_email = adopter["Email"]
        print(f"Recording donation for: {donor_name} ({adopter['Username']})")
    elif choice == "2":
        donor_name = input("Donor's Name: ").strip()
        if not donor_name:
            print("Donor name is required."); return
        donor_email = input("Donor's Email (optional, leave blank to skip invoice email): ").strip() or None
    else:
        print("Invalid option."); return

    amount = is_valid_amount(input("Donation Amount: ").strip())
    if amount is None:
        print("Invalid amount. Enter a number greater than 0."); return

    payment_method = choose_from_list("Payment Method", PAYMENT_METHODS)
    purpose = choose_from_list("Purpose", PURPOSES)
    notes = input("Notes (optional): ").strip() or None

    donation_id, donation_date = insert_donation(
        adopter_id=adopter_id,
        donor_name=donor_name,
        amount=amount,
        payment_method=payment_method,
        purpose=purpose,
        notes=notes,
        recorded_by=admin_user["Username"],
        donor_email=donor_email,
    )

    log_activity(
        admin_user["Username"], "admin",
        f"Recorded donation of {amount:.2f} from {donor_name} (Donation ID {donation_id})",
    )
    print(f"Donation of {amount:.2f} from {donor_name} recorded on {donation_date}.")

    send_donation_invoice(
        to_email=donor_email,
        donation_id=donation_id,
        donor_name=donor_name,
        amount=amount,
        donation_date=donation_date,
        payment_method=payment_method,
        purpose=purpose,
        notes=notes,
    )



# ---------------------------------------------------------------------
# ADMIN SIDE - VIEW ENTIRE DONATION HISTORY
# ---------------------------------------------------------------------

def view_all_donations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.Donation_ID, d.Donation_Date,
               COALESCE(a.Full_Name, d.Donor_Name) AS Donor,
               d.Amount, d.Payment_Method, d.Purpose, d.Recorded_By, d.Status
        FROM Donations d
        LEFT JOIN Adopters a ON d.Adopter_Id = a.Adopter_Id
        ORDER BY d.Donation_ID DESC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No donations have been recorded yet."); return

    display = [[r[0], r[1], r[2], f"{r[3]:.2f}", r[4], r[5], r[6], r[7]] for r in rows]
    print(tabulate(
        display,
        headers=["Donation ID", "Date", "Donor", "Amount", "Payment Method", "Purpose", "Recorded By", "Status"],
        tablefmt="grid",
    ))
    confirmed = [r for r in rows if r[7] == "Confirmed"]
    pending = [r for r in rows if r[7] == "Pending"]
    confirmed_total = sum(r[3] for r in confirmed)
    print(f"Confirmed total received: {confirmed_total:.2f} across {len(confirmed)} donation(s).")
    if pending:
        pending_total = sum(r[3] for r in pending)
        print(f"Awaiting confirmation: {pending_total:.2f} across {len(pending)} donation(s). Use 'Confirm a Pending Donation' to review.")


def donation_search(admin_user):
    print("\n-- Search Donations --")
    print("1. By Donor / Adopter Username")
    print("2. By Purpose")
    print("3. Back")
    choice = input("Select an option: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        username = input("Adopter Username: ").strip()
        cur.execute("""
            SELECT d.Donation_ID, d.Donation_Date, COALESCE(a.Full_Name, d.Donor_Name),
                   d.Amount, d.Payment_Method, d.Purpose
            FROM Donations d
            LEFT JOIN Adopters a ON d.Adopter_Id = a.Adopter_Id
            WHERE a.Username = ?
            ORDER BY d.Donation_ID DESC
        """, (username,))
    elif choice == "2":
        purpose = input("Purpose contains: ").strip()
        cur.execute("""
            SELECT d.Donation_ID, d.Donation_Date, COALESCE(a.Full_Name, d.Donor_Name),
                   d.Amount, d.Payment_Method, d.Purpose
            FROM Donations d
            LEFT JOIN Adopters a ON d.Adopter_Id = a.Adopter_Id
            WHERE d.Purpose LIKE ?
            ORDER BY d.Donation_ID DESC
        """, (f"%{purpose}%",))
    else:
        conn.close()
        return

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No matching donations found."); return

    display = [[r[0], r[1], r[2], f"{r[3]:.2f}", r[4], r[5]] for r in rows]
    print(tabulate(
        display,
        headers=["Donation ID", "Date", "Donor", "Amount", "Payment Method", "Purpose"],
        tablefmt="grid",
    ))


# ---------------------------------------------------------------------
# ADMIN SIDE - CONFIRM / REJECT PENDING (SELF-REPORTED) DONATIONS
# ---------------------------------------------------------------------

def view_pending_donations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.Donation_ID, d.Donation_Date, COALESCE(a.Full_Name, d.Donor_Name),
               d.Amount, d.Payment_Method, d.Purpose
        FROM Donations d
        LEFT JOIN Adopters a ON d.Adopter_Id = a.Adopter_Id
        WHERE d.Status = 'Pending'
        ORDER BY d.Donation_ID ASC
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No donations awaiting confirmation."); return None

    display = [[r[0], r[1], r[2], f"{r[3]:.2f}", r[4], r[5]] for r in rows]
    print(tabulate(
        display,
        headers=["Donation ID", "Date", "Donor", "Amount", "Payment Method", "Purpose"],
        tablefmt="grid",
    ))
    return rows


def get_donation(donation_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.Donation_ID, d.Donation_Date, COALESCE(a.Full_Name, d.Donor_Name),
               COALESCE(a.Email, d.Donor_Email), d.Amount, d.Payment_Method, d.Purpose, d.Notes, d.Status
        FROM Donations d
        LEFT JOIN Adopters a ON d.Adopter_Id = a.Adopter_Id
        WHERE d.Donation_ID = ?
    """, (donation_id,))
    row = cur.fetchone()
    conn.close()
    return row


def confirm_pending_donation(admin_user):
    print("\n-- Confirm a Pending Donation --")
    print("Only confirm a donation once the money has actually been verified received -")
    print("cash physically handed over, or the transfer checked in your bank/UPI app.")
    pending = view_pending_donations()
    if not pending:
        return

    donation_id = input("Enter the Donation ID to confirm: ").strip()
    if not donation_id.isdigit():
        print("Enter a valid numeric Donation ID."); return

    row = get_donation(donation_id)
    if not row:
        print("No donation found with that ID."); return
    _, donation_date, donor_name, donor_email, amount, payment_method, purpose, notes, status = row
    if status != "Pending":
        print(f"That donation is already marked {status}."); return

    confirm = input(
        f"Confirm you have verified {amount:.2f} ({payment_method}) from {donor_name} was received? (Y/N): "
    ).strip().upper()
    if confirm != "Y":
        print("Not confirmed - donation remains Pending."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Donations SET Status = 'Confirmed' WHERE Donation_ID = ?", (donation_id,))
    conn.commit()
    conn.close()

    log_activity(admin_user["Username"], "admin", f"Confirmed Donation ID {donation_id} ({amount:.2f} from {donor_name})")
    print(f"Donation ID {donation_id} is now Confirmed.")

    send_donation_invoice(
        to_email=donor_email,
        donation_id=int(donation_id),
        donor_name=donor_name,
        amount=amount,
        donation_date=donation_date,
        payment_method=payment_method,
        purpose=purpose,
        notes=notes,
    )


def reject_pending_donation(admin_user):
    print("\n-- Reject a Pending Donation --")
    print("Use this if the donor never actually completed the payment they logged.")
    pending = view_pending_donations()
    if not pending:
        return

    donation_id = input("Enter the Donation ID to reject: ").strip()
    if not donation_id.isdigit():
        print("Enter a valid numeric Donation ID."); return

    row = get_donation(donation_id)
    if not row:
        print("No donation found with that ID."); return
    _, _, donor_name, _, amount, payment_method, _, _, status = row
    if status != "Pending":
        print(f"That donation is already marked {status}."); return

    confirm = input(f"Reject the {amount:.2f} ({payment_method}) donation from {donor_name}? (Y/N): ").strip().upper()
    if confirm != "Y":
        print("Cancelled - donation remains Pending."); return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Donations SET Status = 'Rejected' WHERE Donation_ID = ?", (donation_id,))
    conn.commit()
    conn.close()

    log_activity(admin_user["Username"], "admin", f"Rejected Donation ID {donation_id} ({amount:.2f} from {donor_name})")
    print(f"Donation ID {donation_id} has been marked Rejected and won't count toward totals.")



def resend_invoice(admin_user):
    print("\n-- Resend Invoice --")
    donation_id = input("Donation ID: ").strip()
    if not donation_id.isdigit():
        print("Enter a valid numeric Donation ID."); return

    row = get_donation(donation_id)
    if not row:
        print("No donation found with that ID."); return

    _, donation_date, donor_name, donor_email, amount, payment_method, purpose, notes, status = row

    if status != "Confirmed":
        print(f"Donation ID {donation_id} is {status}, not Confirmed - no invoice to resend."); return

    if not donor_email:
        donor_email = input(
            f"No email on file for {donor_name}. Enter one to send to (blank to cancel): "
        ).strip() or None
        if not donor_email:
            print("No email provided - invoice not sent."); return

    sent = send_donation_invoice(
        to_email=donor_email,
        donation_id=row[0],
        donor_name=donor_name,
        amount=amount,
        donation_date=donation_date,
        payment_method=payment_method,
        purpose=purpose,
        notes=notes,
    )
    if sent:
        log_activity(admin_user["Username"], "admin", f"Resent invoice for Donation ID {donation_id}")


# =======================================================================
# ADOPTER DASHBOARD
# =======================================================================

def adopter_donation_dashboard(user):
    while True:
        print(f"\n--- Donations ({user['Full_Name']}) ---")
        print("1. Log a Donation (Pending until admin confirms receipt)")
        print("2. View My Donation History")
        print("3. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                make_donation(user)
            case "2":
                view_my_donation_history(user)
            case "3":
                return
            case _:
                print("Invalid option.")


# =======================================================================
# ADMIN DASHBOARD
# =======================================================================

def admin_donation_dashboard(user):
    while True:
        print(f"\n--- Manage Donations ({user['Full_Name']}) ---")
        print("1. Record a Donation (already-received payment)")
        print("2. View Entire Donation History")
        print("3. Search Donations")
        print("4. View Pending Donations (self-reported, unconfirmed)")
        print("5. Confirm a Pending Donation")
        print("6. Reject a Pending Donation")
        print("7. Resend an Invoice")
        print("8. Back")
        choice = input("Select an option: ").strip()

        match choice:
            case "1":
                record_donation_admin(user)
            case "2":
                view_all_donations()
            case "3":
                donation_search(user)
            case "4":
                view_pending_donations()
            case "5":
                confirm_pending_donation(user)
            case "6":
                reject_pending_donation(user)
            case "7":
                resend_invoice(user)
            case "8":
                return
            case _:
                print("Invalid option.")
