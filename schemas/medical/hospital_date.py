import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel, validator
from .illness_type import IllnessTypeRead


class HospitalDataBase(BaseModel):
    code: str
    place: str
    placeKZ: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: Optional[str]
    profile_id: str
    illness_type_id: Optional[str]

    @validator("document_link")
    def validate_document_link(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")
        return v


class HospitalDataCreate(HospitalDataBase):
    pass


class HospitalDataUpdate(HospitalDataBase):
    pass


class HospitalDataRead(HospitalDataBase):
    id: Optional[str]
    document_link: Optional[str]
    code: Optional[str]
    place: Optional[str]
    placeKZ: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]
    medical_profile_id: Optional[str]
    illness_type: Optional[IllnessTypeRead]

    @validator("placeKZ", "illness_type_id", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else " "

    class Config:
        orm_mode = True
