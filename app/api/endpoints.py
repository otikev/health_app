from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas, database
from typing import List
from datetime import date
from app.schemas import TimeSlot, UserCreate, UserOut, Token
from app.models import User
from app.security import get_password_hash, verify_password, create_access_token, get_current_user, require_role
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/patients", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    return crud.create_patient(db, patient)

@router.post("/doctors", response_model=schemas.DoctorOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    return crud.create_doctor(db, doctor)

@router.get("/doctors/{doctor_id}/available-slots", response_model=List[TimeSlot])
def get_available_slots(
    doctor_id: int,
    date: date = Query(..., description="Date in YYYY-MM-DD format"),
    duration_minutes: int = Query(30, ge=5, le=240, description="Desired appointment duration in minutes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin","doctor"]))
):
    return crud.generate_open_slots(db, doctor_id, date, duration_minutes)

@router.post("/appointments", response_model=schemas.AppointmentOut)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if not crud.is_doctor_available(db, appt.doctor_id, appt.start_time, appt.end_time):
        raise HTTPException(status_code=400, detail="Doctor not available at that time.")
    
    return crud.create_appointment(db, appt)

@router.post("/availabilities", response_model=schemas.AvailabilityOut)
def create_availability(availability: schemas.AvailabilityCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("doctor"))):
    return crud.create_availability(db, availability)
