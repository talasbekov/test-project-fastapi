import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel


class HospitalDataBase(BaseModel):
    code: str
    reason: str
    place: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: Optional[AnyUrl]
    profile_id: uuid.UUID


class HospitalDataCreate(HospitalDataBase):
    pass


class HospitalDataUpdate(HospitalDataBase):
    pass


class HospitalDataRead(HospitalDataBase):
    id: Optional[uuid.UUID]

    document_link: Optional[str]
    code: Optional[str]
    reason: Optional[str]
    place: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
