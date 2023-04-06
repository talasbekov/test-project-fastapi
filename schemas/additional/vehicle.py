import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VehicleBase(BaseModel):
    number: str
    date_from: datetime
    name: str
    profile_id: uuid.UUID
    document_link: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: uuid.UUID
