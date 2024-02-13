import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel


class PassportBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[AnyUrl]
    profile_id: str
    issued_by: str


class PassportCreate(PassportBase):
    pass


class PassportUpdate(BaseModel):
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    profile_id: Optional[str]
    issued_by: Optional[str]


class PassportRead(PassportBase):
    id: Optional[str]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    issued_by: Optional[str]
    profile_id: Optional[str]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
