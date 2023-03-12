from pydantic import BaseModel
from datetime import datetime
import uuid

class VehicleBase(BaseModel):
    number: str
    date_from: datetime
    name: str
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: uuid.UUID
