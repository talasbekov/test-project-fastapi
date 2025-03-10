from typing import Optional, List
from pydantic import BaseModel

from schemas import NamedModel, ReadNamedModel, Model


class VehicleTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(VehicleTypeBase):
    pass


class VehicleTypeRead(VehicleTypeBase, ReadNamedModel):
    pass


class VehicleTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[VehicleTypeRead]]
