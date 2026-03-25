# SchoolTrack — Setup Guide

## What You're Running
- **FastAPI** backend with JWT auth
- **PostgreSQL** database with the full schema
- **HTTPS** via self-signed SSL certificate (locally secure)
- Live auto-reload during development
- **Flutter** frontend with role-based access (Admin, Teacher, Mentor, Student, Parent)


---

## Prerequisites — Install These First

### 1. Python 3.11+
```bash
python --version   # Should say 3.11 or higher
```
Download from https://python.org if needed.

### 2. PostgreSQL
**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
**Mac (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```
**Windows:** Download installer from https://postgresql.org/download/windows/

### 3. OpenSSL (for HTTPS cert generation)
- Ubuntu/Debian: `sudo apt install openssl` (usually pre-installed)
- Mac: `brew install openssl` (usually pre-installed)
- Windows: Included with Git for Windows

---

## Step 1 — Clone / Setup Project

```bash
# Navigate to wherever you keep projects
cd ~/projects

# The folder is already named schooltrack
cd schooltrack

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2 — Create PostgreSQL Database

```bash
# Open PostgreSQL shell
sudo -u postgres psql           # Linux
psql postgres                   # Mac

# Run these commands inside psql:
CREATE USER schooltrack_user WITH PASSWORD 'yourpassword';
CREATE DATABASE schooltrack_db OWNER schooltrack_user;
GRANT ALL PRIVILEGES ON DATABASE schooltrack_db TO schooltrack_user;
\q
```

---

## Step 3 — Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your actual values
nano .env       # or open in VS Code: code .env
```

Update these values in `.env`:
```
DATABASE_URL=postgresql://schooltrack_user:yourpassword@localhost:5432/schooltrack_db
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_hex(32))">
```

---

## Step 4 — Generate SSL Certificate (HTTPS)

```bash
python scripts/generate_cert.py
```
This creates `certs/cert.pem` and `certs/key.pem`.
Your browser will show a warning about "self-signed certificate" — this is expected and safe for local development. Click "Advanced" → "Proceed" to accept it.

---

## Step 5 — Run the Server

```bash
# With HTTPS (recommended):
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile certs/key.pem \
  --ssl-certfile certs/cert.pem \
  --reload

# Without HTTPS (if you hit issues):
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Step 6 — Seed Sample Data

Open a **new terminal tab** (keep the server running):

```bash
cd ~/projects/schooltrack
source venv/bin/activate
python scripts/seed_data.py
```

This creates a sample school, teachers, students, and classes so you can test immediately.

---

## Step 7 — Explore the API

Open your browser:

**Interactive API docs (Swagger UI):**
```
https://localhost:8443/docs
```

**Health check:**
```
https://localhost:8443/health
```

### Test Login via Swagger:
1. Go to `https://localhost:8443/docs`
2. Click `POST /api/v1/auth/login`
3. Click "Try it out"
4. Enter: `username=admin@dps.edu.in`, `password=admin123`
5. Copy the `access_token` from the response
6. Click the **Authorize** button (top right) and paste the token
7. Now all other endpoints are unlocked

---

## Project Structure

```
schooltrack/
├── app/
│   ├── main.py                    # FastAPI app + startup
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py        # Router registration
│   │       └── endpoints/
│   │           ├── auth.py        # Login, register
│   │           ├── schools.py     # Schools, classes, subjects
│   │           ├── students.py    # Student CRUD
│   │           └── attendance.py  # Mark + query attendance
│   ├── core/
│   │   ├── config.py              # Settings from .env
│   │   └── security.py            # JWT, password hashing
│   ├── db/
│   │   └── session.py             # SQLAlchemy engine + Base
│   └── models/
│       ├── __init__.py            # All model imports
│       ├── school.py              # School model
│       ├── user.py                # User + roles
│       ├── academic.py            # Class, Subject, Student
│       └── operations.py          # Attendance, Results, Notifications, Worksheets
├── scripts/
│   ├── generate_cert.py           # Create local SSL cert
│   └── seed_data.py               # Sample data for testing
├── certs/                         # SSL certs (gitignored)
├── .env                           # Your secrets (gitignored)
├── .env.example                   # Template to copy
└── requirements.txt
```

---

## What's Next (Build Order)

| Step | Feature | Status |
|------|---------|--------|
| ✅ 1 | Database schema + FastAPI + Auth | Done |
| ✅ 2 | Students, Attendance endpoints | Done |
| ⬜ 3 | Exam results endpoints | Next |
| ⬜ 4 | Attendance analytics + dashboard data | Next |
| ⬜ 5 | Notification engine (SMS via Twilio/MSG91) | After |
| ⬜ 6 | WhatsApp result sharing | After |
| ⬜ 7 | AI worksheet generation (OpenAI) | After |
| ⬜ 8 | React frontend dashboard | After |

---

## Common Issues

**`psycopg2` install fails:**
```bash
sudo apt install libpq-dev python3-dev   # Linux
brew install libpq                        # Mac
```

**Port 8443 already in use:**
```bash
# Change port in the uvicorn command to 8444 or any free port
```

**Database connection refused:**
```bash
sudo systemctl status postgresql   # Check if Postgres is running
sudo systemctl start postgresql    # Start it if not
```
