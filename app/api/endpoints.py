from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/patients", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@router.post("/doctors", response_model=schemas.DoctorOut)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)

@router.post("/appointments", response_model=schemas.AppointmentOut)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    if not crud.is_doctor_available(db, appt.doctor_id, appt.appointment_time):
        raise HTTPException(status_code=400, detail="Doctor not available at that time.")
    
    return crud.create_appointment(db, appt)

@router.post("/availabilities", response_model=schemas.AvailabilityOut)
def create_availability(availability: schemas.AvailabilityCreate, db: Session = Depends(get_db)):
    return crud.create_availability(db, availability)
