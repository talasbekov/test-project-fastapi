import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel


class IdentificationCardBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    issued_by: str
    document_link: Optional[AnyUrl]
    profile_id: str


class IdentificationCardCreate(IdentificationCardBase):
    pass


class IdentificationCardUpdate(BaseModel):
    document_link: Optional[AnyUrl]


class IdentificationCardRead(IdentificationCardBase):
    id: Optional[str]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    issued_by: Optional[str]
    document_link: Optional[str]
    profile_id: Optional[str]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
