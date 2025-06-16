import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.database import Base, get_db, SessionLocal
from app.security import get_password_hash, create_access_token
from app.models import User, Role
from datetime import datetime, timedelta, date

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Create admin user
    db = TestingSessionLocal()
    admin = User(email="admin@example.com", hashed_password=get_password_hash("adminpass"), role="admin")
    db.add(admin)
    db.commit()
    db.close()

@pytest.fixture
def admin_token(db: Session):
    admin = User(email="admin@example.com", hashed_password=get_password_hash("adminpass"), role=Role.admin)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return create_access_token({"sub": admin.email})

def get_admin_token():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(email="admin@example.com", hashed_password=get_password_hash("adminpass"), role=Role.admin)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    db.close()
    return create_access_token({"sub": admin.email})

def test_register():
    response = client.post("/register", json={
        "email": "user1@example.com",
        "password": "password123",
        "role": "patient"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "user1@example.com"

def test_login():
    response = client.post("/login", data={"username": "user1@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_patient():
    token = get_admin_token()
    response = client.post("/patients", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "123456",
        "insurance": "NHIF",
        "password": "userpass"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "john@example.com"


def test_list_patients():
    token = get_admin_token()
    response = client.get("/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_doctor():
    token = get_admin_token()
    response = client.post("/doctors", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "specialization": "Cardiology",
        "email": "jane@example.com",
        "password": "docpass"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "jane@example.com"


def test_list_doctors():
    token = get_admin_token()
    response = client.get("/doctors", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_available_slots():
    admin_token = get_admin_token()

    # Create a doctor
    doctor_response = client.post("/doctors", json={
        "first_name": "Doc",
        "last_name": "Tor",
        "specialization": "Cardiology",
        "email": "doctor@example.com",
        "password": "docpass"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert doctor_response.status_code == 200
    doctor_id = doctor_response.json()["id"]

    # Generate token for doctor (for availability creation)
    doctor_token = create_access_token({"sub": "doctor@example.com"})

    # Add availability
    start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=4)
    availability_response = client.post("/availabilities", json={
        "start_time": start.isoformat(),
        "end_time": end.isoformat()
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    assert availability_response.status_code == 200

    # Get available slots
    slot_response = client.get(f"/doctors/{doctor_id}/available-slots", params={
        "date": date.today().isoformat(),
        "duration_minutes": 30
    }, headers={"Authorization": f"Bearer {admin_token}"})

    assert slot_response.status_code == 200
    assert isinstance(slot_response.json(), list)


def test_create_appointment():
    token = get_admin_token()

    # Create doctor
    doctor_response = client.post("/doctors", json={
        "first_name": "Jane",
        "last_name": "Smith",
        "specialization": "Dermatology",
        "email": "derm@example.com",
        "password": "dermpass"
    }, headers={"Authorization": f"Bearer {token}"})
    doctor_id = doctor_response.json()["id"]

    # Create patient
    patient_response = client.post("/patients", json={
        "first_name": "Anna",
        "last_name": "Lee",
        "email": "anna@example.com",
        "password": "dermpass",
        "phone": "123456789",
        "insurance": "NHIF"
    }, headers={"Authorization": f"Bearer {token}"})
    patient_id = patient_response.json()["id"]

    doctor_token = create_access_token({"sub": "derm@example.com"})

    # Add doctor availability
    start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end = start + timedelta(minutes=60)
    availabilities_response = client.post("/availabilities", json={
        "start_time": start.isoformat(),
        "end_time": end.isoformat()
    }, headers={"Authorization": f"Bearer {doctor_token}"})
    print("Status:", availabilities_response.status_code)
    print("Response:", availabilities_response.json())
    assert availabilities_response.status_code == 200, availabilities_response.json()

    # Create appointment
    appointment_response = client.post("/appointments", json={
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "start_time": start.isoformat(),
        "end_time": (start + timedelta(minutes=30)).isoformat()
    }, headers={"Authorization": f"Bearer {token}"})
    print("Status:", appointment_response.status_code)
    print("Response:", appointment_response.json())

    assert appointment_response.status_code == 200
    data = appointment_response.json()
    assert data["doctor_id"] == doctor_id
    assert data["patient_id"] == patient_id