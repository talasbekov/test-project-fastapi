import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class PassportBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: str
    profile_id: uuid.UUID


class PassportCreate(PassportBase):
    pass


class PassportUpdate(BaseModel):
    document_link: Optional[str]


class PassportRead(PassportBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
