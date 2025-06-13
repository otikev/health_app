from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime, timedelta
from sqlalchemy import func
from passlib.hash import bcrypt

# Patient
def create_patient(db: Session, patient: schemas.PatientCreate):
    user = models.User(
        email=patient.email,
        hashed_password=bcrypt.hash(patient.password),
        role=models.Role.patient
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db_patient = models.Patient(
        user_id=user.id,
        first_name=patient.first_name,
        last_name=patient.last_name,
        insurance=patient.insurance,
        phone=patient.phone
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# Doctor
def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    user = models.User(
        email=doctor.email,
        hashed_password=bcrypt.hash(doctor.password),
        role=models.Role.doctor
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db_doctor = models.Doctor(
        user_id=user.id,
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        specialization=doctor.specialization
    )
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

def create_availability(db: Session, doctor_id: int, availability: schemas.AvailabilityCreate):
    db_avail = models.DoctorAvailability(
        doctor_id=doctor_id,
        start_time=availability.start_time,
        end_time=availability.end_time
    )
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

def generate_open_slots(db: Session, doctor_id: int, date: datetime.date, slot_minutes: int):
    availabilities = db.query(models.DoctorAvailability).filter(
        models.DoctorAvailability.doctor_id == doctor_id,
        func.date(models.DoctorAvailability.start_time) <= date,
        func.date(models.DoctorAvailability.end_time) >= date
    ).all()

    if not availabilities:
        return []

    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        func.date(models.Appointment.start_time) == date,
        models.Appointment.status == models.AppointmentStatus.scheduled
    ).all()

    taken_slots = [(a.start_time, a.end_time) for a in appointments]
    open_slots = []

    for avail in availabilities:
        current = max(avail.start_time, datetime.combine(date, avail.start_time.time()))
        end = min(avail.end_time, datetime.combine(date, avail.end_time.time()))

        while current + timedelta(minutes=slot_minutes) <= end:
            slot_end = current + timedelta(minutes=slot_minutes)
            overlap = any(
                s < slot_end and e > current for s, e in taken_slots
            )

            if not overlap:
                open_slots.append({
                    "start": current.strftime("%H:%M"),
                    "end": slot_end.strftime("%H:%M")
                })

            current += timedelta(minutes=5)  # slide window in 5-min increments

    return open_slots