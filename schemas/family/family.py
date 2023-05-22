import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .family_relation import FamilyRelationRead


class FamilyBase(BaseModel):
    relation_id: uuid.UUID
    first_name: str
    last_name: str
    father_name: Optional[str]
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
    relation_id: Optional[uuid.UUID]
    relation: Optional[FamilyRelationRead]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    IIN: Optional[str]
    birthday: Optional[datetime.datetime]
    birthplace: Optional[str]
    address: Optional[str]
    workplace: Optional[str]
    profile_id: Optional[uuid.UUID]

    birthplace: Optional[str]
