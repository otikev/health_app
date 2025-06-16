from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    insurance = Column(String)

    appointments = relationship("Appointment", back_populates="patient")
    user = relationship("User", back_populates="patient_profile")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")
    user = relationship("User", back_populates="doctor_profile")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(SqlEnum(AppointmentStatus), default=AppointmentStatus.scheduled)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class DoctorAvailability(Base):
    __tablename__ = "doctor_availabilities"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    doctor = relationship("Doctor", backref="availabilities")

class Role(str, enum.Enum):
    doctor = "doctor"
    patient = "patient"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(Role), nullable=False)
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    patient_profile = relationship("Patient", back_populates="user", uselist=False)