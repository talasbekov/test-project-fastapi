import uuid

from pydantic import BaseModel
from typing import Optional


class EquipmentBase(BaseModel):
    name: str
    quantity: int


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    quantity: Optional[int]

    class Config:
        orm_mode = True
