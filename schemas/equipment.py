import uuid
from typing import Optional

from pydantic import BaseModel


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
