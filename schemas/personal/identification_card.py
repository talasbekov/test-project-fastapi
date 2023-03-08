import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class IdentificationCardBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    issued_by: str
    document_link: str
    profile_id: uuid.UUID


class IdentificationCardCreate(IdentificationCardBase):
    pass


class IdentificationCardUpdate(IdentificationCardBase):
    pass


class IdentificationCardRead(IdentificationCardBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    issued_by: Optional[str]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True