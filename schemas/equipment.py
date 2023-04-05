import uuid
from typing import Optional

from pydantic import BaseModel


class EquipmentBase(BaseModel):
    type_of_equipment: str
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    count_of_ammo: Optional[int]
    type_of_clothing_equipment_model_id: Optional[uuid.UUID]
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: Optional[uuid.UUID] 

    class Config:
        orm_mode = True
