from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


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


class VehicleTypeReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[VehicleTypeRead]]
