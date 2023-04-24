import uuid
from typing import Optional
from datetime import date
from pydantic import EmailStr

from schemas import Model


class LoginForm(Model):
    email: EmailStr
    password: str


class RegistrationForm(Model):
    email: EmailStr
    password: str
    re_password: str
    first_name: str
    last_name: str
    father_name: Optional[str]
    icon: Optional[str]
    call_sign: str
    id_number: str
    phone_number: str
    address: str
    rank_id: Optional[uuid.UUID]
    staff_unit_id: uuid.UUID
    actual_staff_unit_id: uuid.UUID
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    is_military: Optional[bool]
    personal_id: Optional[str]
    iin: Optional[str]
    date_birth: date


class CandidateRegistrationForm(Model):
    iin: str
