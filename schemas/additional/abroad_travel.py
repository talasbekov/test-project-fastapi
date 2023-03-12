from pydantic import BaseModel, validator
from datetime import datetime
import uuid

from typing import Optional

from .country import CountryRead

class AbroadTravelBase(BaseModel):
    vehicle_type: str
    destination_country_id: uuid.UUID
    date_from: datetime
    date_to: datetime
    reason: str
    document_link: str
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AbroadTravelCreate(AbroadTravelBase):
    pass


class AbroadTravelUpdate(AbroadTravelBase):
    pass


class AbroadTravelRead(AbroadTravelBase):
    id: Optional[uuid.UUID]

    destination_country: Optional[CountryRead]
