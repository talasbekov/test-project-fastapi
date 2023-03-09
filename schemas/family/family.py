import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class FamilyBase(BaseModel):
    relation: str
    first_name: str
    last_name: str
    father_name: str
    IIN: str
    birthday: datetime.datetime
    death_day: Optional[datetime.datetime]
    birthplace: str
    address: str
    workplace: str
    
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyCreate(FamilyBase):
    pass


class FamilyUpdate(FamilyBase):
    pass


class FamilyRead(FamilyBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
