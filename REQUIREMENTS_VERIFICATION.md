# Trekking Management Application V2 - Requirements Verification

This checklist maps the project specification to the implemented Flask, Vue, SQLite, Redis, and Celery codebase.

## Framework and Storage Requirements

| Requirement | Verification |
| --- | --- |
| Flask API | Implemented under `backend/app` with blueprints registered from `backend/app/routes`. |
| VueJS UI | Implemented under `frontend/src` using Vue components and Vue Router. |
| Bootstrap styling | Bootstrap is imported in `frontend/src/main.js` and used by Vue views/components. |
| SQLite database | SQLAlchemy models are defined programmatically in `backend/app/models`; tables are created with `db.create_all()` during app startup. |
| Redis caching | Redis-backed cache helpers are implemented in `backend/app/utils/cache.py` and applied to frequently accessed APIs. |
| Redis and Celery batch jobs | Celery app integration and worker entry points are present in `backend/app/utils/celery.py`, `backend/celery_worker.py`, and `backend/app/tasks`. |

## Role and Authentication Requirements

| Requirement | Verification |
| --- | --- |
| Unified user model | `backend/app/models/user.py` defines one `User` model with `admin`, `trek_staff`, and `trekker` roles. |
| Programmatic admin creation | `backend/app/__init__.py` creates the default admin on startup after database creation. |
| No admin registration | Public registration always creates users with the trekker role in `backend/app/routes/auth.py`. |
| Staff login only after admin creation | Staff are created through admin-only staff endpoints in `backend/app/routes/admin.py`. |
| JWT/token role protection | `backend/app/utils/decorators.py` provides token and role guards used by admin, staff, user, booking, and export routes. |
| Deactivation/blacklisting | Admin status endpoints toggle `is_active` for users and staff; inactive accounts cannot log in or access token-protected APIs. |

## Admin Requirements

| Requirement | Verification |
| --- | --- |
| Dashboard counts | Admin dashboard summary returns total treks, trekkers, staff, bookings, and recent bookings. |
| Create/update/remove treks | Admin trek CRUD routes are implemented in `backend/app/routes/admin.py`. |
| Add/manage trek staff | Admin staff list/create/update/status routes are implemented in `backend/app/routes/admin.py`. |
| Assign staff to treks | Admin trek create/update routes validate and persist `assigned_staff_id`. |
| View bookings | Admin booking list and booking status endpoints are implemented. |
| Search users, staff, treks | Admin list endpoints accept search/filter parameters. |
| Reports/statistics | Admin report stats endpoint aggregates difficulty, status, booking, top trek, and trend metrics. |

## Trek Staff Requirements

| Requirement | Verification |
| --- | --- |
| Assigned trek dashboard | Staff dashboard returns only treks assigned to the authenticated staff user. |
| Manage slots and status | Staff endpoints update trek slot capacity and status. |
| View participant list | Staff dashboard includes participants for assigned treks. |
| Only assigned staff manage a trek | Staff management routes reject requests for treks not assigned to the current staff user. |
| Mark started/completed | Staff status route supports lifecycle status updates, including completion. |

## Trekker Requirements

| Requirement | Verification |
| --- | --- |
| Self-register and login | Auth routes support trekker registration and unified login. |
| Dashboard available/booked/history data | User dashboard summary returns upcoming treks, active bookings, history, and recommendations. |
| Search/filter treks | Public trek listing supports search, difficulty, location, and duration filters. |
| View approved/open treks | Public trek listing is limited to `Approved` and `Open` treks. |
| Book treks | Booking API creates trekker bookings only for open treks. |
| View booking status/history | User dashboard and booking-related views consume booking status/history data. |
| Edit profile | User profile get/update routes are implemented. |

## Booking and Data Integrity Requirements

| Requirement | Verification |
| --- | --- |
| Prevent overbooking | Booking creation verifies available slots before incrementing participants. |
| Allow booking only when trek status is Open | Booking creation rejects non-open treks. |
| Prevent duplicate active bookings | Booking creation checks existing user/trek bookings and blocks duplicates unless cancelled. |
| Maintain trek history | Booking records preserve statuses and completed/cancelled bookings are shown in user history. |
| Booking statuses | Booking model defines `Booked`, `Cancelled`, and `Completed`. |
| Trek lifecycle statuses | Trek routes validate `Pending`, `Approved`, `Open`, `Closed`, and `Completed`. |

## Background Jobs and Reports

| Requirement | Verification |
| --- | --- |
| Daily reminders | `backend/app/tasks/reminder.py` contains the scheduled reminder task. |
| Monthly activity report | `backend/app/tasks/reports.py`, `backend/app/services/report_service.py`, and `backend/app/templates/monthly_report.html` implement report generation and email delivery. |
| User-triggered CSV export | Export API triggers `export_user_history_csv`, tracks status, and lets users download their own generated CSV. |

## Notes

- `Trek.booking_close_time` is nullable so staff/admin can reopen treks by setting status to `Open` without violating database constraints.
- Public trek browsing intentionally exposes only approved/open treks; admin routes remain available for full historical trek management.
