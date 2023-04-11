
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid
from schemas import PrivelegeEmergencyRead, PersonnalReserveRead, CoolnessRead

class OathRead(BaseModel):
    date: Optional[datetime]
    military_name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date=orm_obj.date,
            military_name=orm_obj.military_unit.name,
        )

class GeneralInformationRead(BaseModel):
    oath: Optional[OathRead]
    privilege_emergency_secrets: Optional[PrivelegeEmergencyRead]
    personnel_reserve: Optional[PersonnalReserveRead]
    coolness: Optional[CoolnessRead]
    is_badge_black: Optional[bool]
    researcher: Optional[str]
    recommendation: Optional[str]
