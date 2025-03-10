import uuid
from typing import Optional, List
from datetime import datetime

from schemas import Model, ReadModel, ReadNamedModel, NamedModel, Model


class EquipmentBase(Model):
    type_of_equipment: Optional[str]
    type_of_army_eq_model_id: Optional[str]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    cloth_eq_types_models_id: Optional[str]
    type_of_other_eq_model_id: Optional[str]
    clothing_size: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EquipmentCreate(EquipmentBase):
    cloth_eq_types_id: Optional[str]
    cloth_eq_models_id: Optional[str]


class EquipmentUpdate(EquipmentBase):
    cloth_eq_types_id: Optional[str]
    cloth_eq_models_id: Optional[str]


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


class TypeArmyEquipmentReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[TypeArmyEquipmentRead]]


class TypeClothingEquipmentModelSchema(ReadNamedModel):
    type_cloth_eq_types_id: Optional[str]
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentRead(ReadNamedModel):
    type_cloth_eq_models: Optional[List[TypeClothingEquipmentModelSchema]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[TypeClothingEquipmentRead]]


class ClothingEquipmentTypesModelsRead(ReadNamedModel):

    type_cloth_eq_models: Optional[List[TypeClothingEquipmentModelSchema]]
    type_cloth_equipmets: Optional[List[TypeClothingEquipmentRead]]

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


class TypeOtherEquipmentReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[TypeOtherEquipmentRead]]


class TypeArmyEquipmentModelCreate(NamedModel):
    type_of_army_equipment_id: Optional[str]


class TypeArmyEquipmentCreate(NamedModel):
    pass


class TypeClothingEquipmentModelCreate(NamedModel):
    pass


class TypeClothingEquipmentCreate(NamedModel):
    model_ids: Optional[List[Optional[str]]]

class TypeClothingEquipmentUpdate(NamedModel):
    pass 

class TypeOtherEquipmentModelCreate(NamedModel):
    type_of_other_equipment_id: Optional[str]


class TypeOtherEquipmentCreate(NamedModel):
    pass