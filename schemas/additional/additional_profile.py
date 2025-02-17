import uuid
from typing import List, Optional, Union


from schemas.additional import (AbroadTravelRead, PolygraphCheckRead,
                                PsychologicalCheckRead, SpecialCheckRead,
                                ViolationRead, ServiceHousingRead, VehicleRead,
                                PropertiesRead)
from schemas import Model, ReadModel
from pydantic import validator

class AdditionalProfileBase(Model):
    profile_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AdditionalProfileCreate(AdditionalProfileBase):
    pass


class AdditionalProfileUpdate(AdditionalProfileBase):
    pass


class AdditionalProfileRead(AdditionalProfileBase, ReadModel):
    profile_id: str
    polygraph_checks: Union[Optional[List[PolygraphCheckRead]], str]
    violations: Union[Optional[List[ViolationRead]], str]
    abroad_travels: Optional[List[AbroadTravelRead]]
    psychological_checks: Union[Optional[List[PsychologicalCheckRead]], str]
    special_checks: Union[Optional[List[SpecialCheckRead]], str]
    service_housing: Optional[List[ServiceHousingRead]]
    user_vehicles: Optional[List[VehicleRead]]
    properties: Optional[List[PropertiesRead]]

    # @validator("special_checks")
    # def set_to_none(cls, v):
    #     if v[0]=='no permission':
    #         return None
    #     return v 
