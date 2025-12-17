# Mini Hospital Management System (HMS)

Django-based hospital management web app for doctor availability and patient appointment booking with serverless email notifications and Google Calendar integration.

## Features

**User Authentication**: Signup/login for doctors and patients with role-based access
**Doctor Availability**: Doctors can create and manage time slots
**Patient Booking**: Patients can view available slots and book appointments
**Atomic Booking**: Race condition prevention using database locking
**Email Notifications**: Serverless Lambda function for signup/booking emails
**Google Calendar Integration**: OAuth2-based calendar event creation for appointments
**Admin Panel**: Django admin for managing users, slots, and bookings

## Tech Stack

- **Backend**: Django 5.2+
- **Database**: PostgreSQL (Required)
- **Auth**: Session-based authentication with hashed passwords
- **Serverless**: AWS Lambda + Serverless Framework
- **Email**: SMTP (Gmail or custom)
- **Calendar**: Google Calendar API with OAuth2

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js and npm** (for Serverless Framework)
3. **PostgreSQL** installed and running
4. **Google Cloud Project** with Calendar API enabled (optional, for calendar integration)

## Setup Instructions

### 1. PostgreSQL Database Setup

```powershell
# Install PostgreSQL from https://www.postgresql.org/download/
# Create database:
psql -U postgres
CREATE DATABASE hms_db;
CREATE USER hms_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
\q
```

### 2. Django Application Setup

```powershell
# Clone repository
git clone https://github.com/AryanMishra1789/Mini-Hospital-Management-System-HMS-.git
cd Mini-Hospital-Management-System-HMS-

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and set your PostgreSQL credentials:
# DB_NAME=hms_db
# DB_USER=hms_user
# DB_PASSWORD=password123

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000`

### 3. Google Calendar Integration (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project and enable **Google Calendar API**
3. Create **OAuth 2.0 credentials** (Web application)
4. Add redirect URI: `http://localhost:8000/calendar/oauth2callback/`
5. Download credentials as `client_secrets.json` in project root
6. Users connect calendar via: `http://localhost:8000/calendar/auth/`

### 4. Serverless Email Service

```powershell
# Install Serverless Framework
npm install -g serverless

# Navigate to serverless folder
cd serverless

# Install plugin
serverless plugin install -n serverless-offline

# Set SMTP credentials
$env:SMTP_USER="your-email@gmail.com"
$env:SMTP_PASS="your-gmail-app-password"

# Run locally
serverless offline
```

Email endpoint: `http://localhost:3000/send`

## Gmail SMTP Setup

1. Enable 2FA on Gmail
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Use app password as `SMTP_PASS`

## Environment Variables

### `.env` file (Django)
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=hms_db
DB_USER=hms_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5432
SERVERLESS_EMAIL_URL=http://localhost:3000/send
```

### Serverless Function
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

## Usage Guide

### For Doctors
1. Sign up with role "Doctor"
2. Navigate to "My Slots"
3. Create availability time slots
4. (Optional) Connect Google Calendar
5. View patient bookings

### For Patients
1. Sign up with role "Patient"
2. Browse available doctors and slots
3. (Optional) Connect Google Calendar
4. Click "Book" on available slot
5. Receive email and calendar invite

## API Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/users/signup/` | GET/POST | User registration | Public |
| `/users/login/` | GET/POST | User login | Public |
| `/users/logout/` | GET | User logout | Authenticated |
| `/my-slots/` | GET | View doctor's slots | Doctor only |
| `/create-slot/` | GET/POST | Create time slot | Doctor only |
| `/bookings/create/<id>/` | POST | Book appointment | Patient only |
| `/calendar/auth/` | GET | Connect Google Calendar | Authenticated |
| `/admin/` | GET | Django admin panel | Staff only |

## Project Structure

```
Mini-Hospital-Management-System-HMS/
├── hms/                      # Django project settings
├── users/                    # Authentication & user management
├── availability/             # Doctor availability slots
├── bookings/                 # Appointment booking logic
├── calendar_integration/     # Google Calendar OAuth2
├── serverless/               # Email Lambda function
│   ├── handler.py
│   └── serverless.yml
├── templates/                # HTML templates
├── manage.py
├── requirements.txt
└── README.md
```

## Technical Implementation

### Race Condition Prevention
```python
# Atomic booking with row-level locking
@classmethod
def create_for_slot(cls, slot_id, patient):
    with transaction.atomic():
        slot = TimeSlot.objects.select_for_update().get(pk=slot_id)
        if slot.is_booked:
            raise ValueError('Slot already booked')
        slot.is_booked = True
        slot.save()
        return cls.objects.create(slot=slot, patient=patient)
```

### Email Notifications
- Serverless architecture (AWS Lambda compatible)
- Non-blocking, best-effort delivery
- Actions: `SIGNUP_WELCOME`, `BOOKING_CONFIRMATION`
- Local testing with `serverless-offline`

### Google Calendar
- OAuth2 per-user authentication
- Automatic token refresh
- Creates events for both doctor and patient
- Graceful fallback if not connected

## Troubleshooting

**PostgreSQL Connection Error**
- Check PostgreSQL is running: `pg_isready`
- Verify credentials in `.env`
- Confirm database exists: `psql -U postgres -l`

**Email Not Sending**
- Ensure `serverless offline` runs on port 3000
- Verify SMTP credentials
- Use Gmail App Password, not regular password

**Calendar Not Working**
- Check `client_secrets.json` exists in project root
- Verify OAuth redirect URI: `http://localhost:8000/calendar/oauth2callback/`
- Ensure Calendar API enabled in GCP

## Testing

```powershell
# Run Django checks
python manage.py check

# Test migrations
python manage.py makemigrations --check

# Create test data
python manage.py shell
>>> from users.models import User
>>> doctor = User.objects.create_user('doc1', 'doc@test.com', 'pass', role='doctor')
>>> patient = User.objects.create_user('pat1', 'pat@test.com', 'pass', role='patient')
```

## Future Enhancements

- [ ] REST API with Django REST Framework
- [ ] Comprehensive unit/integration tests
- [ ] Modern frontend (React/Vue)
- [ ] Production deployment (AWS Lambda + RDS)
- [ ] Patient booking history
- [ ] Doctor slot edit/delete functionality
- [ ] Appointment reminders (24h, 1h before)
- [ ] Video consultation integration
- [ ] Multiple time zone support
- [ ] Recurring availability patterns

## Security Notes

- Passwords hashed using Django's PBKDF2 algorithm
- CSRF protection enabled
- Role-based access control enforced
- OAuth2 for calendar access
- Environment variables for secrets

## Support

For issues or questions, please create an issue in the GitHub repository.
