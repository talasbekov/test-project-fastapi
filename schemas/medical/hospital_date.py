import datetime

from typing import Optional

from pydantic import validator
from pydantic.networks import AnyUrl

from .illness_type import IllnessTypeRead
from .. import CustomBaseModel


class HospitalDataBase(CustomBaseModel):
    code: str
    place: str
    placeKZ: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: Optional[AnyUrl]
    profile_id: str
    illness_type_id: Optional[str]

    @validator("document_link", pre=True, always=True)
    def validate_url(cls, v):
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("Invalid URL format")
        return v or "https://default.link"


class HospitalDataCreate(HospitalDataBase):
    pass


class HospitalDataUpdate(HospitalDataBase):
    pass


class HospitalDataRead(HospitalDataBase):
    id: Optional[str]
    document_link: Optional[AnyUrl]
    code: Optional[str]
    place: Optional[str]
    placeKZ: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]
    medical_profile_id: Optional[str]
    illness_type: Optional[IllnessTypeRead]

    # @validator("placeKZ", "illness_type_id", pre=True, always=True)
    # def default_empty_string(cls, v):
    #     return v if v is not None else " "

    class Config:
        orm_mode = True
