from pydantic import BaseModel
from datetime import datetime
import uuid

from models import DestinationCountry

class AbroadTravelBase(BaseModel):
    vehicle_type: str
    destination_country: DestinationCountry
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
    id: int 
