import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel


class HospitalDataBase(BaseModel):
    code: str
    reason: str
    reasonKZ: str
    place: str
    placeKZ: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: Optional[AnyUrl]
    profile_id: str


class HospitalDataCreate(HospitalDataBase):
    pass


class HospitalDataUpdate(HospitalDataBase):
    pass


class HospitalDataRead(HospitalDataBase):
    id: Optional[str]

    document_link: Optional[str]
    code: Optional[str]
    reason: Optional[str]
    reasonKZ: Optional[str]
    place: Optional[str]
    placeKZ: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]

    class Config:
        orm_mode = True
