import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class VehicleBase(NamedModel):
    number: str
    date_from: datetime
    profile_id: uuid.UUID
    document_link: Optional[str]
    vin_code: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(VehicleBase):
    pass


class VehicleRead(VehicleBase, ReadNamedModel):
    pass
