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

### Authentication
An admin record exists with credentials:
```
admin@test.com
admin123
```

### 4 Database schema
![Database Schema](docs/database.png)

### 5. Future Enhancements

- Patient appointment booking UI
- View appointment history per role
- Slot selection UI from availability
- Calendar-based views
- Notification/email integration

