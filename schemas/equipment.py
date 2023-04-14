import uuid
from typing import Optional, List
from datetime import datetime

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class EquipmentBase(Model):
    type_of_equipment: str
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    count_of_ammo: Optional[int]
    type_of_clothing_equipment_model_id: Optional[uuid.UUID]
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    user_id: Optional[uuid.UUID]
    inventory_number_of_other_equipment: Optional[str]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class EquipmentCreate(EquipmentBase):
    pass

 

class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase, ReadModel):
    pass
 

class TypeArmyEquipmentModel(ReadNamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeArmyEquipmentRead(ReadNamedModel):
    type_of_army_equipment_models: Optional[List[TypeArmyEquipmentModel]] 

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentModel(ReadNamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentRead(ReadNamedModel):

    type_of_clothing_equipment_models: Optional[List[TypeClothingEquipmentModel]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentModel(ReadNamedModel):
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentRead(ReadNamedModel):
    type_of_other_equipment_models: Optional[List[TypeOtherEquipmentModel]]
    inventory_number_of_other_equipment: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
