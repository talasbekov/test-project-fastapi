import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class EquipmentBase(BaseModel):
    type_of_equipment: str
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    count_of_ammo: Optional[int]
    type_of_clothing_equipment_model_id: Optional[uuid.UUID]
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class EquipmentCreate(EquipmentBase):
    pass

 

class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: Optional[uuid.UUID] 
 

class TypeArmyEquipmentModel(BaseModel):
    name: Optional[str]
    id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeArmyEquipmentRead(BaseModel):
    id: Optional[uuid.UUID]
    type_of_army_equipment_models: Optional[List[TypeArmyEquipmentModel]] 
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentModel(BaseModel):
    name: Optional[str]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentRead(BaseModel):
    id: Optional[uuid.UUID]
    type_of_clothing_equipment_models: Optional[List[TypeClothingEquipmentModel]]
    name: Optional[str] 

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentModel(BaseModel):
    name: Optional[str]
    id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentRead(BaseModel):
    id: Optional[uuid.UUID]
    type_of_other_equipment_models: Optional[List[TypeOtherEquipmentModel]]
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
