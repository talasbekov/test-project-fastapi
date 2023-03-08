from pydantic import BaseModel
from .polygraph_check import PolygraphCheckRead
from .violation import ViolationRead
from .abroad_travel import AbroadTravelRead
from .psychological_check import PsychologicalCheckRead
import uuid
from typing import Optional, List

class AdditionalProfileBase(BaseModel):
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AdditionalProfileCreate(AdditionalProfileBase):
    pass


class AdditionalProfileUpdate(AdditionalProfileBase):
    pass


class AdditionalProfileRead(AdditionalProfileBase):
    id: uuid.UUID
    profile_id: uuid.UUID
    polygraph_checks: Optional[List[PolygraphCheckRead]] = []
    violations: Optional[List[ViolationRead]] = []
    abroad_travels: Optional[List[AbroadTravelRead]] = []
    psychological_checks: Optional[List[PsychologicalCheckRead]] = []

    

