import datetime
import uuid
from typing import List, Optional

from pydantic import AnyUrl, BaseModel


class SportDegreeBase(BaseModel):
    name: str
    assignment_date: datetime.date
    document_link: AnyUrl
    profile_id: uuid.UUID


class SportDegreeCreate(SportDegreeBase):
    pass


class SportDegreeUpdate(SportDegreeBase):
    pass


class SportDegreeRead(SportDegreeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    assignment_date: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
