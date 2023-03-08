import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class DrivingLicenceBase(BaseModel):
    document_number: str
    category: List[str]
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: str
    profile_id: uuid.UUID


class DrivingLicenceCreate(DrivingLicenceBase):
    pass


class DrivingLicenceUpdate(DrivingLicenceBase):
    pass


class DrivingLicenceRead(DrivingLicenceBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    category: Optional[List[str]]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
