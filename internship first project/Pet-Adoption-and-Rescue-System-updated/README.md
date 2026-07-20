# Pet Adoption & Rescue Management System

## Bug Fixes in This Version

This version fixes the issue where the adoption-transaction table and
pending-request list weren't updating correctly. Root causes found and fixed:

1. **No link between a request and the adopter who made it.** `request_adoption()`
   only flipped a pet's status to `Pending` - it never recorded which adopter asked
   for it. When an admin later processed the request, they had to manually type an
   adopter's username from memory, with nothing to check it against. A typo or a
   wrong guess would silently create the adoption transaction for the *wrong*
   adopter, or leave the real requester with nothing in their history.
   **Fix:** added `Pets.Requested_By`, filled in automatically by
   `request_adoption()`, shown in the pending-requests list, and used automatically
   (with a confirmation prompt) by `process_adoption()`.

2. **"Pending" meant two different things.** Flagging a pet as medically
   ineligible (Module 4) also set its `Adoption_Status` to `Pending` - the exact
   same status used for a genuine adoption request. That meant pets nobody had
   ever asked to adopt could show up in the pending-requests queue, and could be
   accidentally "approved" into a bogus transaction.
   **Fix:** medically-ineligible pets now get a distinct `Unavailable` status
   instead, so they never enter the adoption-request queue.

3. **No way to reject a request.** Once a pet was `Pending`, the only path forward
   was `Adopted` - there was no way to decline a request and free the pet back up.
   **Fix:** added a "Reject Adoption Request" option for admins.

4. **Database path depended on the current working directory.** `db_functions.py`
   used the bare relative path `"petadoption.db"`, so running the app from a
   different folder (e.g. from inside `main files/`, or from an IDE's "Run" button)
   silently created/used a second, empty database - updates would "disappear"
   because they were being written somewhere else entirely.
   **Fix:** the path is now anchored to the project folder regardless of where the
   app is launched from.

5. **Manual status overrides left stale request links behind.** Manually setting a
   pet's status in Module 2 didn't clear `Requested_By`, which could leave a stale
   adopter linked to a pet after an admin bypassed the normal workflow.
   **Fix:** manual status changes now clear `Requested_By`.

Run `python "main files/db_setup.py"` once before starting the app - it creates any
missing tables and adds the new `Requested_By` column to an existing database
without touching your data. It's safe to run more than once.


A console-based, menu-driven Python application for managing pet adoption and rescue operations. Built with SQLite and featuring role-based access control (Admin vs. Adopter), the system streamlines pet inventory management, adoption workflows, vaccination tracking, and provides analytics dashboards for rescue shelters.

## Key Features

### Module 1: Authentication & User Management
- User registration and login with role-based access (Admin/Adopter)
- Profile management and password reset functionality
- Email verification code sending via SMTP
- Admin privilege elevation capabilities
- Role-based dashboards with menu-driven navigation (match-case)

### Module 2: Pet Management
- Full pet inventory CRUD operations (Admin only)
- Track pet details: name, species, breed, age, health status, adoption status
- Manage pets across multiple shelters
- Update health and adoption status

### Module 3: Pet Search & Discovery
- Search pets by name, breed, species, age, health status, or shelter location
- View detailed pet information and availability
- Browse complete pet catalog

### Module 4: Vaccination & Medical Records
- Track vaccination history and medical records for each pet
- Due-date alerts for upcoming vaccinations
- Flag medically ineligible pets
- Admin: full access | Adopters: read-only view

### Module 5: Adoption Transactions
- Submit adoption requests
- Admin approval workflow
- Duplicate application and availability validation
- Pet return processing
- Complete adoption history tracking

### Module 6: Analytics Dashboard
- Admin-only analytics and reporting
- Tabular reports: available pets, overdue vaccinations
- Matplotlib visualizations:
  - Adoption trends (line chart)
  - Species distribution (pie chart)
  - Shelter occupancy (bar chart)

## Tech Stack

- **Language:** Python 3.10+
- **Database:** SQLite3
- **UI:** Console-based (menu-driven terminal interface)
- **Dependencies:**
  - `tabulate` — formatted table output
  - `matplotlib` — data visualization and analytics charts
  - `smtplib` — email verification codes
  - `hashlib` — SHA-256 password hashing

## Project Structure

```
Pet-Adoption-and-Rescue-System/
├── main files/
│   ├── run.py                    # Entry point — run this to start the app
│   ├── main_file.py              # Module 1: authentication & role management
│   ├── db_functions.py           # Shared SQLite connection, password hashing, email, logging
│   ├── pet_management.py         # Module 2: pet inventory CRUD (admin only)
│   ├── search_menu.py            # Module 3: pet search & discovery
│   ├── vaccinations.py           # Module 4: vaccination & medical records
│   ├── adoption_transaction.py   # Module 5: adoption request/approval workflow
│   └── module6_analytics.py      # Module 6: analytics dashboard & visualizations
├── documentation/               # Project documentation
└── README.md                     # This file
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/skully0709/Pet-Adoption-and-Rescue-System.git
   cd Pet-Adoption-and-Rescue-System
   ```

2. **Install required dependencies:**
   ```bash
   pip install tabulate matplotlib python-dotenv
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Fill in `SENDER_EMAIL` and `SENDER_PASSWORD` (a Gmail App Password, not your login password)
   - `.env` is excluded from Git by `.gitignore`, so your credentials stay local

4. **Initialize the database:**
   - The SQLite database schema must be created before running the application
   - See the [Database Schema](#database-schema) section below for the SQL script

5. **Run the application:**
   ```bash
   python main\ files/run.py
   ```

## Database Schema

The system uses SQLite with 7 tables:

- **Administrators** — admin user accounts and permissions
- **Adopters** — adopter user profiles and preferences
- **Activity_log** — audit trail of all system activities
- **Shelters** — shelter/location information
- **Pets** — pet inventory (linked to Shelters via foreign key)
- **Vaccinations** — vaccination and medical records (linked to Pets)
- **Adoption_Transactions** — adoption history (linked to both Pets and Adopters)

Foreign key relationships:
- Pets → Shelters
- Vaccinations → Pets
- Adoption_Transactions → Pets, Adopters

**To create the database schema:**
```sql
-- Paste your SQL seed script here
```

## Usage Flow

### For New Users
1. Run `python main\ files/run.py` to start the application
2. Select **Register** from the main menu
3. Enter email, password, and personal information
4. Choose your role: **Adopter** or request **Admin** access
5. Check your email for verification code if applicable

### For Adopters
1. Log in with your credentials
2. Access the Adopter Dashboard:
   - **Browse Pets** — search and filter available pets (Module 3)
   - **View Pet Details** — see full information and vaccination records
   - **Submit Adoption Request** — apply to adopt a pet (Module 5)
   - **View My Applications** — track adoption request status
   - **Profile** — manage your account and preferences

### For Administrators
1. Log in with admin credentials
2. Access the Admin Dashboard:
   - **Pet Management** — add, update, delete, and manage pet inventory (Module 2)
   - **Vaccination Management** — track medical records and flag ineligible pets (Module 4)
   - **Adoption Approvals** — review and approve/reject adoption requests (Module 5)
   - **Analytics** — view reports and visualizations (Module 6)
   - **User Management** — manage accounts and permissions
   - **Activity Logs** — audit system activities

## Contributors

- [Add contributors here]

## License

[Add license information here]

## Questions or Support

For issues or questions, please open a GitHub issue or contact the project maintainers.
