import uuid
from typing import Optional
from datetime import date
from pydantic import EmailStr, validator

from schemas import Model


class LoginForm(Model):
    email: EmailStr
    password: str

class EcpLoginForm(Model):
    certificate_blob: str


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
    rank_id: Optional[str]
    staff_unit_id: str
    actual_staff_unit_id: str
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    is_military: Optional[bool]
    personal_id: Optional[str]
    iin: Optional[str]
    date_birth: date


class CandidateRegistrationForm(Model):
    iin: str

    @validator('iin')
    def validate_iin(cls, v):
        if not v.isdigit():
            raise ValueError('iin must contain only digits')
        if len(v) != 12:
            raise ValueError('iin must be exactly 12 digits')
        return v
