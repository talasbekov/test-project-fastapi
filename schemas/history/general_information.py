import uuid
from datetime import datetime

from typing import Optional
from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import PrivelegeEmergencyRead, PersonnalReserveRead, CoolnessRead, RecommenderUserRead

class OathRead(ReadModel):
    date: Optional[datetime]
    military_id: Optional[uuid.UUID]
    military_name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date=orm_obj.date,
            military_id=orm_obj.military_unit_id,
            military_name=orm_obj.military_unit.name,
        )


class GeneralInformationRead(BaseModel):
    oath: Optional[OathRead]
    privilege_emergency_secrets: Optional[PrivelegeEmergencyRead]
    personnel_reserve: Optional[PersonnalReserveRead]
    coolness: Optional[CoolnessRead]
    is_badge_black: Optional[bool]
    researcher: Optional[dict]
    recommender: Optional[dict]
