import uuid

from pydantic import BaseModel


class EquipmentBase(BaseModel):
    name: str
    quantity: int


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
