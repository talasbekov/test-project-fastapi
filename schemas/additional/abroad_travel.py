import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl

from schemas import Model, ReadModel

from .country import CountryRead


class AbroadTravelBase(Model):
    vehicle_type: str
    vehicle_typeKZ: str
    destination_country_id: str
    date_from: datetime
    date_to: Optional[datetime]
    reason: str
    reasonKZ: str
    document_link: Optional[AnyUrl]
    profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AbroadTravelCreate(AbroadTravelBase):
    pass


class AbroadTravelUpdate(AbroadTravelBase):
    pass


class AbroadTravelRead(AbroadTravelBase, ReadModel):
    document_link: Optional[str]
    destination_country: Optional[CountryRead]
    vehicle_typeKZ: Optional[str]
    reasonKZ: Optional[str]
