# 🏨 HostelMate — Integrated Student Hostel Assistance & Service Portal

HostelMate is a modern, web-based integrated platform designed for college campus hostel residents and administration. It bridges communication, facilities management, meal scheduling, resource sharing, and campus recovery on a unified digital portal.

---

## 🚀 Technology Stack

- **Backend:** Python 3.13 / Flask 3.1
- **Database ORM:** SQLAlchemy 2.x via Flask-SQLAlchemy
- **Database Support:** PostgreSQL (Supabase) in production / SQLite for local development
- **Migrations:** Flask-Migrate / Alembic
- **Authentication & Security:** Flask-Login, Werkzeug password hashing, Flask-WTF CSRF protection
- **Frontend / Presentation:** Jinja2 Templates, Vanilla CSS & JavaScript, Bootstrap Icons

---

## 🏛️ Application Architecture & Structure

```
HotelMate/
│
├── app/
│   ├── __init__.py          # Flask app factory, extension init, context processors, CLI hooks
│   ├── extensions.py        # Shared extension instances (db, migrate, login_manager, csrf)
│   ├── commands.py          # Custom CLI commands (e.g. `flask seed`)
│   │
│   ├── models/              # SQLAlchemy Domain Models
│   │   ├── __init__.py
│   │   ├── user.py          # User & UserProfile (Roles: student / admin)
│   │   ├── announcement.py  # Announcements & Notice Categories
│   │   ├── complaint.py     # Helpdesk Tickets & Lifecycle Statuses
│   │   ├── mess.py          # MessMenu (Day-wise) & MessReview (1-5 Star Ratings)
│   │   └── community.py     # Peer Resource Lending & LostAndFound Items
│   │
│   ├── forms/               # Flask-WTF Form Definitions & Validations
│   │   ├── __init__.py
│   │   ├── auth.py          # UserRegisterForm, LoginForm, ProfileUpdateForm
│   │   ├── announcement.py  # AnnouncementForm
│   │   ├── complaint.py     # ComplaintForm, ComplaintStatusForm
│   │   ├── mess.py          # MessMenuForm, MessReviewForm
│   │   ├── community.py     # ResourceForm, LostAndFoundForm
│   │   └── admin.py         # AdminStudentEditForm
│   │
│   ├── routes/              # Modular Blueprints & Route Handlers
│   │   ├── __init__.py      # Blueprint registration helper
│   │   ├── main.py          # / and /dashboard (Dual Student/Warden Dispatcher)
│   │   ├── auth.py          # /login, /register, /logout, /profile
│   │   ├── announcements.py # /announcements, /announcements/create, /announcements/delete/<pk>
│   │   ├── complaints.py    # /complaints, /complaints/create, /complaints/<pk>, /complaints/<pk>/status
│   │   ├── mess.py          # /mess, /mess/update, /mess/review
│   │   ├── resources.py     # /resources, /resources/create, /resources/<pk>/toggle, /resources/<pk>/delete
│   │   ├── lost_found.py    # /lost-found, /lost-found/create, /lost-found/<pk>/toggle, /lost-found/<pk>/delete
│   │   └── admin.py         # /admin-students, /admin-students/<pk>/edit
│   │
│   ├── utils/               # Utilities & Helpers
│   │   ├── __init__.py
│   │   ├── decorators.py    # @admin_required, @login_required guards
│   │   ├── helpers.py       # get_or_create_profile()
│   │   └── filters.py       # Custom Jinja filters (date, truncatewords, slice, make_list)
│   │
│   ├── static/              # Static Assets
│   │   ├── css/style.css    # Premium CSS design system
│   │   └── js/main.js       # Toast notifications & modal handlers
│   │
│   └── templates/           # Jinja2 HTML Templates
│       ├── base.html        # Master responsive layout with sidebar & topbar
│       └── core/            # 13 Screen templates (Dashboards, Auth, Forms, Details)
│
├── migrations/              # Alembic Database Migration History
├── tests/                   # Automated Unit & Integration Tests
│   └── test_app.py          # Comprehensive test suite covering all modules
│
├── config.py                # App Configuration (Dev, Prod, Testing, Supabase Normalizer)
├── run.py                   # Development Server Entrypoint & Shell Context
├── requirements.txt         # Production & Development Python Dependencies
├── .env                     # Local Environment Config (Git-Ignored)
├── .env.example             # Environment Configuration Template
└── README.md                # Documentation & Developer Guide
```

---

## 🛠️ Quick Start & Installation

### 1. Prerequisites
- Python 3.11+ (Python 3.13 supported)
- Git

### 2. Create Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` to configure your environment variables:

```ini
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here

# Supabase / PostgreSQL Connection String
# Example: postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
# Leave empty for local development (will use instance/hostelmate.db automatically)
DATABASE_URL=

SESSION_COOKIE_SECURE=False
```

> **Note on Supabase:** If using Supabase connection strings starting with `postgres://`, HostelMate automatically normalizes them to `postgresql+psycopg2://` for SQLAlchemy 2.0 compatibility.

---

## 🗄️ Database Setup & Migrations

Initialize and apply migrations:

```bash
# Apply migrations to database (SQLite or Supabase PostgreSQL)
flask db upgrade

# Populate database with demo admin, students, announcements, mess menu, & tickets
flask seed
```

---

## 🏃 Running the Application

### Development Server:
```bash
python run.py
```
Or with Flask CLI:
```bash
flask run --port=5000 --debug
```

Open your browser at: **`http://127.0.0.1:5000`**

---

## 🔑 Demo Login Accounts

After running `flask seed`, use these credentials to explore both personas:

| Role | Username | Password | Key Features Accessible |
| :--- | :--- | :--- | :--- |
| **Warden / Admin** | `admin` | `admin123` | Analytics dashboard, student directory & room allocation, ticket triage & resolution remarks, mess menu publishing, notice broadcasting |
| **Student 1** | `student1` | `student123` | Student dashboard, file complaints, review daily meals, share books/notes, report lost items |
| **Student 2** | `student2` | `student123` | Room 104 Block B resident |
| **Student 3** | `student3` | `student123` | Room 215 Block A resident |

---

## 🧪 Running Automated Tests

HostelMate includes a comprehensive automated test suite testing authentication, role-based protection, complaints lifecycle, mess reviews, resource sharing, and admin edits:

```bash
python -m unittest tests/test_app.py
```

---

## 👥 Team Development Workflow

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```
2. **Apply any new database migrations:**
   ```bash
   flask db upgrade
   ```
3. **If you modify any SQLAlchemy model in `app/models/`:**
   ```bash
   flask db migrate -m "Description of model change"
   flask db upgrade
   ```
4. **Run tests before committing:**
   ```bash
   python -m unittest tests/test_app.py
   ```
