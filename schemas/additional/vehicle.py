import uuid
from datetime import datetime
from typing import Optional


from schemas import NamedModel, ReadNamedModel


class VehicleBase(NamedModel):
    number: Optional[str]
    date_from: datetime
    profile_id: str
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
