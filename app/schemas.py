from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import enum

class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientOut(PatientCreate):
    id: int

    class Config:
        orm_mode = True

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: str

class DoctorOut(DoctorCreate):
    id: int

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
    doctor_id: int
    start_time: datetime
    end_time: datetime

class AvailabilityOut(AvailabilityCreate):
    id: int

    class Config:
        orm_mode = True
