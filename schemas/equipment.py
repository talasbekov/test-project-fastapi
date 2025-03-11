import uuid
from typing import Optional, List
from datetime import datetime

from schemas.base import Model, ReadModel, ReadNamedModel, NamedModel


class EquipmentBase(Model):
    """
    Общие поля для сущности Equipment.
    """
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
    """
    Схема для создания Equipment.
    Если type_of_equipment == 'clothing_equipment',
    используются поля cloth_eq_types_id и cloth_eq_models_id.
    """
    cloth_eq_types_id: Optional[str]
    cloth_eq_models_id: Optional[str]


class EquipmentUpdate(EquipmentBase):
    """
    Схема для обновления Equipment (аналогична EquipmentCreate).
    """
    cloth_eq_types_id: Optional[str]
    cloth_eq_models_id: Optional[str]


class EquipmentRead(EquipmentBase, ReadModel):
    """
    Схема для чтения Equipment (id, created_at, updated_at).
    """
    pass


# ------------------- Армейское оборудование ------------------- #

class TypeArmyEquipmentModel(ReadNamedModel):
    """
    Схема чтения для модели армейского оборудования.
    """
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeArmyEquipmentRead(ReadNamedModel):
    """
    Схема чтения для типа армейского оборудования,
    со связанными моделями (type_of_army_equipment_models).
    """
    type_of_army_equipment_models: Optional[List[TypeArmyEquipmentModel]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeArmyEquipmentReadPagination(Model):
    """
    Схема пагинации для списка типов армейского оборудования.
    """
    total: Optional[int]
    objects: Optional[List[TypeArmyEquipmentRead]]


class TypeArmyEquipmentModelCreate(NamedModel):
    """
    Схема для создания модели армейского оборудования.
    """
    type_of_army_equipment_id: Optional[str]


class TypeArmyEquipmentCreate(NamedModel):
    """
    Схема для создания типа армейского оборудования.
    (Поля name, nameKZ наследуются от NamedModel.)
    """
    pass


# ------------------- Одежда ------------------- #

class TypeClothingEquipmentModelSchema(ReadNamedModel):
    """
    Схема чтения для одной модели одежды.
    """
    type_cloth_eq_types_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentRead(ReadNamedModel):
    """
    Схема чтения для типа одежды,
    со связанными моделями (type_cloth_eq_models).
    """
    type_cloth_eq_models: Optional[List[TypeClothingEquipmentModelSchema]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentReadPagination(Model):
    """
    Схема пагинации для списка типов одежды.
    """
    total: Optional[int]
    objects: Optional[List[TypeClothingEquipmentRead]]


class ClothingEquipmentTypesModelsRead(ReadNamedModel):
    """
    Схема для промежуточной таблицы ClothingEquipmentTypesModels.
    """
    type_cloth_eq_models: Optional[List[TypeClothingEquipmentModelSchema]]
    type_cloth_equipmets: Optional[List[TypeClothingEquipmentRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeClothingEquipmentModelCreate(NamedModel):
    """
    Схема для создания модели одежды.
    """
    # Пока полей нет
    pass


class TypeClothingEquipmentCreate(NamedModel):
    """
    Схема для создания типа одежды, с привязкой к нескольким моделям.
    model_ids: список id моделей.
    """
    model_ids: Optional[List[Optional[str]]]  # можно заменить на Optional[List[str]]


class TypeClothingEquipmentUpdate(NamedModel):
    """
    Схема для обновления типа одежды (без model_ids).
    """
    pass


# ------------------- Прочее оборудование ------------------- #

class TypeOtherEquipmentModel(ReadNamedModel):
    """
    Схема чтения для модели 'другого' оборудования.
    """
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentRead(ReadNamedModel):
    """
    Схема чтения для типа 'другого' оборудования,
    со связанными моделями.
    """
    type_of_other_equipment_models: Optional[List[TypeOtherEquipmentModel]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TypeOtherEquipmentReadPagination(Model):
    """
    Схема пагинации для списка типов 'другого' оборудования.
    """
    total: Optional[int]
    objects: Optional[List[TypeOtherEquipmentRead]]


class TypeOtherEquipmentModelCreate(NamedModel):
    """
    Схема для создания модели 'другого' оборудования.
    """
    type_of_other_equipment_id: Optional[str]


class TypeOtherEquipmentCreate(NamedModel):
    """
    Схема для создания типа 'другого' оборудования.
    """
    pass
