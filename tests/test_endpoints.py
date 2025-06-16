import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models
from app.security import get_password_hash

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
    admin = models.User(email="admin@example.com", hashed_password=get_password_hash("adminpass"), role="admin")
    db.add(admin)
    db.commit()
    db.close()


def get_auth_token():
    response = client.post("/login", data={"username": "admin@example.com", "password": "adminpass"})
    return response.json()["access_token"]


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
    token = get_auth_token()
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
    token = get_auth_token()
    response = client.get("/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_doctor():
    token = get_auth_token()
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
    token = get_auth_token()
    response = client.get("/doctors", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
