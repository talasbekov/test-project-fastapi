import datetime
import uuid
from typing import List, Optional, Union

from pydantic import BaseModel, AnyUrl


class DrivingLicenseLinkUpdate(BaseModel):
    document_link: Optional[AnyUrl]


class DrivingLicenseBase(BaseModel):
    document_number: str
    category: List[str]
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[AnyUrl]
    profile_id: str


class DrivingLicenseCreate(DrivingLicenseBase):
    category: Optional[str]


class DrivingLicenseUpdate(BaseModel):
    document_number: Optional[str]
    category: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    # profile_id: str


class DrivingLicenseRead(DrivingLicenseBase):
    id: Optional[str]
    document_number: Optional[str]
    category: Union[Optional[str], Optional[List[str]]]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[str]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
