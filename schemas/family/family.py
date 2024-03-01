import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel

from .family_relation import FamilyRelationRead
from schemas import ViolationRead, AbroadTravelRead


class FamilyBase(BaseModel):
    relation_id: str
    first_name: str
    last_name: str
    father_name: Optional[str]
    IIN: str
    birthday: datetime.datetime
    death_day: Optional[datetime.datetime]
    birthplace: str
    address: Optional[str]
    workplace: Optional[str]

    profile_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyCreate(FamilyBase):
    pass


class FamilyUpdate(FamilyBase):
    pass


class FamilyRead(FamilyBase):

    id: Optional[str]
    relation_id: Optional[str]
    relation: Optional[FamilyRelationRead]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    IIN: Optional[str]
    birthday: Optional[datetime.datetime]
    birthplace: Optional[str]
    address: Optional[str]
    workplace: Optional[str]
    profile_id: Optional[str]

    birthplace: Optional[str]
    violation: Optional[List[ViolationRead]]
    abroad_travel: Optional[List[AbroadTravelRead]]
