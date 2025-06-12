from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

# Patient
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# Doctor
def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# Appointment
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def create_availability(db: Session, availability: schemas.AvailabilityCreate):
    db_avail = models.DoctorAvailability(**availability.dict())
    db.add(db_avail)
    db.commit()
    db.refresh(db_avail)
    return db_avail

def is_doctor_available(db: Session, doctor_id: int, start_time: datetime, end_time: datetime) -> bool:
    available = db.query(models.DoctorAvailability).filter(
        models.DoctorAvailability.doctor_id == doctor_id,
        models.DoctorAvailability.start_time <= start_time,
        models.DoctorAvailability.end_time >= end_time
    ).first()

    if not available:
        return False

    conflict = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.status == models.AppointmentStatus.scheduled,
        models.Appointment.start_time < end_time,
        models.Appointment.end_time > start_time
    ).first()

    return conflict is None

