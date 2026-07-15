# TrekSphere - Trekking Management Application V2

A full-stack Trekking Management System developed as part of the **Modern Application Development II (MAD-II)** course at IIT Madras.

The application helps manage trekking events through three different roles:

- Admin
- Trek Staff
- Trekker (User)

The system allows administrators to manage treks and staff, staff members to manage assigned treks, and users to browse and book trekking events.

---

# Features

## Authentication

- JWT based authentication
- Role Based Access Control
- User Registration
- Admin Login
- Trek Staff Login

## Admin

- Dashboard with statistics
- Manage Treks
- Manage Trek Staff
- Assign Staff to Treks
- Manage Users
- View Bookings
- Search Users, Staff and Treks
- Reports and Analytics

## Trek Staff

- View Assigned Treks
- Update Trek Status
- Update Available Slots
- View Participants
- Manage Assigned Treks

## Trekker

- Register and Login
- Browse Treks
- Search and Filter Treks
- Book Treks
- Cancel Bookings
- View Trek History
- Export Booking History (CSV)

## Background Jobs

- Daily Trek Reminder Emails
- Monthly Activity Report
- Asynchronous CSV Export using Celery

## Performance

- Redis Caching
- Cached Trek Listings

---

# Technology Stack

## Backend

- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask Mail
- Celery
- Redis
- SQLite

## Frontend

- Vue 3
- Vue Router
- Axios
- Bootstrap 5
- Chart.js

---

# Project Structure

```
trek-app-mad2-main/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── tasks/
│   │   ├── utils/
│   │   └── templates/
│   ├── run.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Requirements

- Python 3.10+
- Node.js 20+
- Redis
- npm

---


## Running the Application

Start the services in the following order:

1. Redis
2. Backend (Flask)
3. Celery Worker
4. Celery Beat
5. Frontend (Vue)

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Activate the virtual environment

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows (Command Prompt)

```cmd
venv\Scripts\activate
```

#### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend

```bash
python run.py
```

Backend runs on

```
http://localhost:5000
```

---

## Redis

Ensure your system has redis server installed.
Open terminal.
Start the Redis server.

### Linux / macOS

```bash
redis-server
```

### Windows

If Redis is installed as a Windows Service:

```cmd
redis-server
```

---

## Celery Worker

Start the worker:

```bash
celery -A celery_worker:celery_app worker --loglevel=info
```

## Celery Beat

Open another terminal.

```bash
cd backend
```

Run:

```bash
celery -A celery_worker:celery_app beat --loglevel=info
```


---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

Open another terminal and navigate to the backend folder:

```bash
cd backend
```

---

## Backend API

```
http://localhost:5000/api
```

## Frontend (Vue)

```
http://localhost:5173
```

---

# Default Admin Account

```
Email:
admin@trek.com

Password:
admin123
```

# Demo Accounts

```
Trek Staff: 
Email: aarav@trek.com
Password: staff123

Trekker: 
Email: rahul.sharma@trek.com
Password: password123
```

---

# Roles

## Admin

- Manage Users
- Manage Staff
- Manage Treks
- View Reports

## Trek Staff

- Manage Assigned Treks
- Update Trek Status
- View Participants

## Trekker

- Register
- Book Treks
- View Trek History

---

# Project Highlights

- JWT Authentication
- Role Based Access Control
- Celery Background Jobs
- Redis Caching
- CSV Export
- Monthly Reports
- Responsive UI
- Charts and Analytics

---

# Developed For

Modern Application Development II (MAD-II)

Indian Institute of Technology Madras

Project: Trekking Management Application V2

---

# Author

Devendra Chouhan

IIT Madras BS Degree Programme


## License

This project was developed for academic purposes as part of the IIT Madras BS Degree Programme (MAD-II course).