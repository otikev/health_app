# Healthcare Scheduling System

A full-stack web application built with **FastAPI** and **React** that supports:

- Role-based login (admin, doctor, patient)
- Managing patients and doctors (admin only)
- Doctor availability scheduling
- Appointment booking with slot conflict detection
- Secure JWT-based authentication

---

## Features

| Role     | Permissions |
|----------|-------------|
| Admin    | Register users, add doctors/patients, schedule appointments |
| Doctor   | Set availability |
| Patient  | (coming soon) Book appointments |

---

## Tech Stack

- Backend: [FastAPI](https://fastapi.tiangolo.com/), SQLAlchemy, Alembic, PostgreSQL
- Auth: OAuth2 Password Flow + JWT
- Frontend: [React](https://reactjs.org/) with Axios
- Styling: Custom CSS

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/healthcare-app.git
cd healthcare-app
```

### 2. Backend setup
Install requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Update database.py with your Postgres URI

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/healthcare_db
```

Run database migrations
```bash
alembic upgrade head
```

Start the server

```bash
uvicorn app.main:app --reload
```
Swagger UI:  http://localhost:8000/docs

### 3. Frontend setup
```bash
cd frontend
npm install
npm start
```
Frontend runs at http://localhost:3000

### 5. Authentication
An admin record exists with credentials:
```
admin@test.com
admin123
```

### 6. Database schema
![Database Schema](docs/database.png)

### API documentation

All protected endpoints require the Authorization header
```
Authorization: Bearer <access_token>
```

## POST /login

Authenticate a user and retrieve a JWT access token.

Form Data (x-www-form-urlencoded):
- username: Email
- password: Password

Response
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}
```

## POST /register

Register a new user.

Request Body:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "admin" | "doctor" | "patient"
}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "admin"
}
```

## POST /patients

Create a new patient. Requires admin role.

Request Body:
```json
{
  "first_name": "Anna",
  "last_name": "Lee",
  "email": "anna@example.com",
  "phone": "123456789",
  "insurance": "NHIF",
  "password": "securepass"
}
```

Response:
```json
{
  "id": 1,
  "first_name": "Anna",
  "last_name": "Lee",
  "email": "anna@example.com",
  "phone": "123456789",
  "insurance": "NHIF"
}
```

## GET /patients

List all patients. Requires admin role.

Response:
```json
[
  {
    "id": 1,
    "first_name": "Anna",
    "last_name": "Lee",
    "email": "anna@example.com",
    "phone": "123456789",
    "insurance": "NHIF"
  }
]
```

## POST /doctors

Create a new doctor. Requires admin role.

Request Body:
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "specialization": "Cardiology",
  "password": "securepass"
}
```

Response:
```json
{
  "id": 1,
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "specialization": "Cardiology"
}
```

## GET /doctors

List all doctors. Requires admin role.

```json
[
  {
    "id": 1,
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "specialization": "Cardiology"
  }
]
```

## POST /availabilities

Add available time slots for a doctor. Requires doctor role.

Request Body:
```json
{
  "start_time": "2025-06-18T09:00:00",
  "end_time": "2025-06-18T12:00:00"
}
```

Response:
```json
{
  "id": 1,
  "doctor_id": 1,
  "start_time": "2025-06-18T09:00:00",
  "end_time": "2025-06-18T12:00:00"
}
```

## GET /doctors/{doctor_id}/available-slots

Get available slots for a doctor on a given day. Requires admin or doctor role.

Query Parameters:
- date: Date in YYYY-MM-DD format
- duration_minutes: Duration of appointment (5–240 mins, default is 30)

Response:
```json
[
  {
    "start": "2025-06-18T09:00:00",
    "end": "2025-06-18T09:30:00"
  },
  ...
]
```

## POST /appointments

Create an appointment between a doctor and a patient. Requires admin role.

Request Body:
```json
{
  "doctor_id": 1,
  "patient_id": 2,
  "start_time": "2025-06-18T09:00:00",
  "end_time": "2025-06-18T09:30:00"
}
```

Response:
```json
{
  "id": 1,
  "doctor_id": 1,
  "patient_id": 2,
  "start_time": "2025-06-18T09:00:00",
  "end_time": "2025-06-18T09:30:00",
  "status": "scheduled"
}
```

### 7. Future Enhancements

- Patient appointment booking UI
- View appointment history per role
- Slot selection UI from availability
- Calendar-based views
- Notification/email integration

