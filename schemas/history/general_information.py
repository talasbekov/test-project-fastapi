from datetime import datetime
from typing import Optional, List
from pydantic import Field

from schemas import ReadModel
from schemas import PrivelegeEmergencyRead, PersonnalReserveRead, CoolnessRead, RecommenderUserRead
from schemas.base import Model


class OathRead(ReadModel):
    date: Optional[datetime]
    military_id: Optional[str]
    military_name: Optional[str]
    military_nameKZ: Optional[str]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date=orm_obj.date,
            military_id=orm_obj.military_unit_id,
            military_name=orm_obj.military_unit.name,
            military_nameKZ=orm_obj.military_unit
        )


class BlackBeretRead(Model):
    id: Optional[str]
    badge_id: Optional[str]
    date_from: Optional[datetime]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class GeneralInformationRead(Model):
    oath: Optional[OathRead]
    privilege_emergency_secrets: Optional[PrivelegeEmergencyRead]
    personnel_reserve: Optional[PersonnalReserveRead] = Field(alias='personnel_reserve', default_factory=dict)
    coolness: Optional[List[CoolnessRead]]
    black_beret: Optional[BlackBeretRead]
    recommender: Optional[RecommenderUserRead] = Field(alias='recommender', default_factory=dict)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
