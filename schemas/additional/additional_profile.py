import uuid
from typing import List, Optional


from schemas.additional import (AbroadTravelRead, PolygraphCheckRead,
                                PsychologicalCheckRead, SpecialCheckRead,
                                ViolationRead, ServiceHousingRead, VehicleRead,
                                PropertiesRead)
from schemas import Model, ReadModel


class AdditionalProfileBase(Model):
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AdditionalProfileCreate(AdditionalProfileBase):
    pass


class AdditionalProfileUpdate(AdditionalProfileBase):
    pass


class AdditionalProfileRead(AdditionalProfileBase, ReadModel):
    profile_id: uuid.UUID
    polygraph_checks: Optional[List[PolygraphCheckRead]]
    violations: Optional[List[ViolationRead]]
    abroad_travels: Optional[List[AbroadTravelRead]]
    psychological_checks: Optional[List[PsychologicalCheckRead]]
    special_checks: Optional[List[SpecialCheckRead]]
    service_housing: Optional[List[ServiceHousingRead]]
    user_vehicles: Optional[List[VehicleRead]]
    properties: Optional[List[PropertiesRead]]
