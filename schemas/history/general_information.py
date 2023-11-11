import uuid
from datetime import datetime

from typing import Optional, List
from pydantic import BaseModel

from schemas import ReadModel
from schemas import PrivelegeEmergencyRead, PersonnalReserveRead, CoolnessRead


class OathRead(ReadModel):
    date: Optional[datetime]
    military_id: Optional[str]
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
        
class BlackBeretRead(BaseModel):
    id: Optional[str]
    badge_id: Optional[str]
    date_from: Optional[datetime]
    document_number: Optional[str]


class GeneralInformationRead(BaseModel):
    oath: Optional[OathRead]
    privilege_emergency_secrets: Optional[PrivelegeEmergencyRead]
    personnel_reserve: Optional[PersonnalReserveRead]
    coolness: Optional[List[CoolnessRead]]
    black_beret: Optional[BlackBeretRead]
    researcher: Optional[dict]
    recommender: Optional[dict]
