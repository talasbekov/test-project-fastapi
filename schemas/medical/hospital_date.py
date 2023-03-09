import datetime
import uuid

from pydantic import BaseModel


class HospitalDataBase(BaseModel):
    code: str
    reason: str
    place: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: str
    profile_id: uuid.UUID


class HospitalDataCreate(HospitalDataBase):
    pass


class HospitalDataUpdate(HospitalDataBase):
    pass


class HospitalDataRead(HospitalDataBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
