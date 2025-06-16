from pydantic import BaseModel, EmailStr
from datetime import datetime, time
from typing import Optional, List
import enum

class Role(str, enum.Enum):
    doctor = "doctor"
    patient = "patient"
    admin = "admin"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role

    class Config:
        orm_mode = True

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: Optional[str] = None
    insurance: Optional[str] = None
    user: UserOut

    class Config:
        orm_mode = True

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    email: EmailStr
    password: str

class DoctorOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: str
    user: UserOut

    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime

class AppointmentOut(AppointmentCreate):
    id: int
    status: AppointmentStatus

    class Config:
        orm_mode = True

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime

class AvailabilityOut(AvailabilityCreate):
    id: int

    class Config:
        orm_mode = True

class TimeSlot(BaseModel):
    start: str  # e.g. "09:00"
    end: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
