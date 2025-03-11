import datetime
from typing import List, Optional

from .family_relation import FamilyRelationRead
from schemas import ViolationRead, AbroadTravelRead, Model
from schemas.personal import BirthplaceRead


class FamilyBase(Model):
    relation_id: str
    first_name: str
    last_name: str
    father_name: Optional[str]
    IIN: Optional[str]
    birthday: datetime.datetime
    death_day: Optional[datetime.datetime]
    address: Optional[str]
    workplace: Optional[str]
    birthplace_id: Optional[str]
    document_link: Optional[str]

    profile_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyCreate(Model):
    relation_id: str
    first_name: str
    last_name: str
    father_name: Optional[str]
    IIN: Optional[str]
    document_link: Optional[str]
    birthday: datetime.datetime
    death_day: Optional[datetime.datetime]
    address: Optional[str]
    workplace: Optional[str]
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]

    profile_id: str


class FamilyUpdate(Model):
    relation_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    IIN: Optional[str]
    birthday: Optional[datetime.datetime]
    death_day: Optional[datetime.datetime]
    address: Optional[str]
    workplace: Optional[str]
    city_id: Optional[str]
    region_id: Optional[str]
    country_id: Optional[str]
    document_link: Optional[str]

    profile_id: Optional[str]


class FamilyRead(FamilyBase):

    id: Optional[str]
    relation_id: Optional[str]
    relation: Optional[FamilyRelationRead]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    IIN: Optional[str]
    birthday: Optional[datetime.datetime]
    address: Optional[str]
    workplace: Optional[str]
    profile_id: Optional[str]
    birthplace_id: Optional[str]
    document_link: Optional[str]
    families_profile_id: Optional[str]

    birthplace: Optional["BirthplaceRead"]
    violation: Optional[List[ViolationRead]]
    abroad_travels: Optional[List[AbroadTravelRead]]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            relation_id=orm_obj.relation_id,
            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            father_name=orm_obj.father_name,
            IIN=orm_obj.IIN,
            birthday=orm_obj.birthday,
            death_day=orm_obj.death_day,
            address=orm_obj.address,
            workplace=orm_obj.workplace,
            profile_id=orm_obj.profile_id,
            violation=orm_obj.violation if orm_obj.violation else [],
            abroad_travel=orm_obj.abroad_travels if orm_obj.abroad_travels else [],  # исправлено
            birthplace=orm_obj.birthplace if orm_obj.birthplace else {},
            birthplace_id=orm_obj.birthplace_id if orm_obj.birthplace_id else orm_obj.id,
            document_link=orm_obj.document_link,
        )
