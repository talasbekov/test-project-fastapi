import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel


class DrivingLicenseBase(BaseModel):
    document_number: str
    category: List[str]
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: str
    profile_id: uuid.UUID


class DrivingLicenseCreate(DrivingLicenseBase):
    pass


class DrivingLicenseUpdate(DrivingLicenseBase):
    pass


class DrivingLicenseRead(DrivingLicenseBase):
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
