import uuid
from typing import Optional, List
from datetime import datetime

from schemas import Model, ReadModel, ReadNamedModel


class EquipmentBase(Model):
    type_of_equipment: Optional[str]
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    clothing_equipment_types_models_id: Optional[uuid.UUID]
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    clothing_size: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    user_id: Optional[uuid.UUID]

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
    type_clothing_equipment_models: Optional[List[TypeClothingEquipmentModel]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ClothingEquipmentTypesModelsRead(ReadNamedModel):

    type_clothing_equipment_models: Optional[List[TypeClothingEquipmentModel]]
    type_clothing_equipments: Optional[List[TypeClothingEquipmentRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentModel(ReadNamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentRead(ReadNamedModel):
    type_of_other_equipment_models: Optional[List[TypeOtherEquipmentModel]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
