import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel

from .country import CountryRead


class AbroadTravelBase(Model):
    vehicle_type: str
    destination_country_id: uuid.UUID
    date_from: datetime
    date_to: datetime
    reason: str
    document_link: AnyUrl
    profile_id: Optional[uuid.UUID]

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
