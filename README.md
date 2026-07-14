# TrekSphere - Trekking Management Application

This is a web application built for the **Modern Application Development 2 (MAD-2)** project in the **BS in Data Science and Applications** degree from **IIT Madras**. 

It helps manage trekking trips by connecting three types of users: Admin, Trek Guides (Staff), and Trekkers (Users).

---

## What the App Does

The application has three main roles, each with different permissions:

1. **Admin (Administrator)**:
   - Sees a dashboard with system-wide numbers (total users, bookings, staff guides).
   - Can view all registered users and guides, and deactivate accounts if needed.
   - Approves new treks created by staff or adds new treks directly.
   - Assigns staff guides to specific treks.
   - Accesses system analytics and reports with charts showing bookings and difficulties.

2. **Trek Staff (Guides)**:
   - Can create new treks (which start as "Pending" until an admin approves them).
   - Manages treks assigned to them (change slots, close bookings, mark as completed).
   - Views lists of trekkers who have registered for their treks.
   - Downloads participant lists.

3. **Trekkers (General Users)**:
   - Public Landing page shows trekking statistics (difficulty split, popular treks, trends).
   - Can browse approved and open treks.
   - Can book a trek (reserving slots) and view active bookings.
   - Simulates payment to confirm the booking (updates status from Pending to Paid).
   - Can export their booking history to a CSV file.
   - Receives daily email reminders before a trek starts.

---

## Tech Stack Used

- **Frontend**: Vue.js 3, Bootstrap 5 (for dark-themed UI styling), Chart.js (for analytics graphs).
- **Backend**: Flask (Python), SQLite (database), SQLAlchemy (ORM).
- **Caching & Background Jobs**: Redis (broker and cache store), Celery (asynchronous task runner and Celery Beat scheduler).
- **Email Alerts**: Python SMTP (configured to write mail logs locally or send actual emails).

---

## Key Technical Features

### 1. Redis Caching
To speed up the app, frequently visited endpoints are cached using Redis. A custom caching decorator hashes URL parameters so that searches and dashboard summaries load instantly. The cache is automatically cleared (invalidated) whenever a write action happens (like booking a trek or updating a status) so users always see correct data.

### 2. Celery Background Jobs
Long-running and automated tasks are offloaded to Celery workers:
- **Async CSV Export**: When a trekker requests their booking history, a background job creates the CSV file and sends it to the user.
- **Daily Reminders**: A cron job (Celery Beat) runs every morning at 8:00 AM, checks for treks starting the next day, and sends email alerts to participants.
- **Monthly Progress Reports**: Runs on the first day of every month to compile stats and email an HTML report to all administrators.

### 3. Progressive Web App (PWA) Features
- Includes a service worker (`sw.js`) and a web app manifest (`manifest.json`).
- Users can "Add to Home Screen" on mobile devices.
- Caches core static files so the interface can load offline.

---

## How to Set Up and Run

### Prerequisites
You need to have the following installed:
- Python 3.10+
- Node.js (with npm)
- Redis Server (either running locally or via Docker on port `6379`)

---

### Step 1: Set Up Backend

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment variables (copy `.env.example` to `.env` and fill in SMTP details if you want real emails).

5. Start the backend Flask server:
   ```bash
   python run.py
   ```
   *Note: This will automatically seed a default admin (`admin@trek.com` / `admin123`), staff (`staff@trek.com` / `staff123`), and trekker (`trekker@trek.com` / `trekker123`) for testing.*

---

### Step 2: Start Background Tasks

Open separate terminals, activate the virtual environment in the `backend` folder for each, and run:

1. **Celery Worker**:
   ```bash
   celery -A celery_worker.celery_app worker --loglevel=info
   ```

2. **Celery Beat (Scheduler)**:
   ```bash
   celery -A celery_worker.celery_app beat --loglevel=info
   ```

---

### Step 3: Set Up Frontend

1. Navigate to the frontend folder:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and go to: `http://localhost:5173`

---

## Default Login Credentials for Testing

- **Admin**: `admin@trek.com` / password: `admin123`
- **Staff Guide**: `staff@trek.com` / password: `staff123`
- **Trekker**: `trekker@trek.com` / password: `trekker123`