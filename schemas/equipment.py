from typing import Optional, List, get_origin, get_args
from datetime import datetime

from models import OtherEquipmentTypeModel, ClothingEquipmentTypeModel, ArmyEquipmentTypeModel
from schemas.base import Model, ReadModel, ReadNamedModel, NamedModel, Field

# ----------------------------------------------------
#              Общие схемы Equipment
# ----------------------------------------------------
class EquipmentBase(Model):
    """
    Общие поля для сущности Equipment.
    """
    type_of_equipment: Optional[str]
    army_equipment_type_model_id: Optional[str]
    clothing_equipment_type_model_id: Optional[str]
    other_equipment_type_model_id: Optional[str]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    clothing_size: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


class EquipmentCreate(EquipmentBase):
    """
    Схема для создания Equipment.
    Поскольку все поля соответствуют модели, дополнительных полей для одежды не требуется.
    """
    pass


class EquipmentUpdate(EquipmentBase):
    """
    Схема для обновления Equipment.
    """
    pass


# ----------------------------------------------------
#           Армейское оборудование (Army)
# ----------------------------------------------------
class ArmyEquipmentTypeModelRead(ReadNamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ArmyEquipmentTypeRead(ReadNamedModel):
    """
    Тип армейского оборудования (например, «Автомат») с привязанными моделями.
    """
    army_equipment_type_models: Optional[List[ArmyEquipmentTypeModelRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ArmyEquipmentTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[ArmyEquipmentTypeRead]]


class ArmyEquipmentTypeModelCreate(NamedModel):
    army_equipment_type_id: Optional[str]


class ArmyEquipmentTypeCreate(NamedModel):
    pass


# ----------------------------------------------------
#             Одежда (Clothing)
# ----------------------------------------------------
class ClothingEquipmentTypeModelRead(ReadNamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ClothingEquipmentTypeRead(ReadNamedModel):
    """
    Тип одежды (например, «Шапка») с привязанными моделями.
    """
    # В модели поле называется "clothing_equipment_models"
    clothing_equipment_type_models: Optional[List[ClothingEquipmentTypeModelRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ClothingEquipmentTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[ClothingEquipmentTypeRead]]


class ClothingEquipmentTypeModelCreate(NamedModel):
    clothing_equipment_type_id: Optional[str]


class ClothingEquipmentTypeCreate(NamedModel):
    """
    При создании типа одежды можно передать список идентификаторов моделей.
    """
    pass


class ClothingEquipmentTypeUpdate(NamedModel):
    pass


# ----------------------------------------------------
#           Прочее оборудование (Other)
# ----------------------------------------------------
class OtherEquipmentTypeModelRead(ReadNamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class OtherEquipmentTypeRead(ReadNamedModel):
    """
    Тип прочего оборудования (например, «Принтер») с привязанными моделями.
    """
    other_equipment_type_models: Optional[List[OtherEquipmentTypeModelRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class OtherEquipmentTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[OtherEquipmentTypeRead]]


class OtherEquipmentTypeModelCreate(NamedModel):
    other_equipment_type_id: Optional[str]


class OtherEquipmentTypeCreate(NamedModel):
    pass


# ----------------------------------------------------
#        Основная схема чтения: EquipmentRead
# ----------------------------------------------------

class ArmyBaseEquipmentTypeRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @classmethod
    def from_orm(cls, orm_obj: ArmyEquipmentTypeModel):
        parent_type = orm_obj.army_equipment_type  # родитель
        return cls(
            id=parent_type.id,
            name=parent_type.name,
            nameKZ=parent_type.nameKZ,
            type_of_equipment={
                "name": orm_obj.name,
                "nameKZ": orm_obj.nameKZ,
            }
        )


class ClothingBaseEquipmentTypeRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @classmethod
    def from_orm(cls, orm_obj: ClothingEquipmentTypeModel):
        parent_type = orm_obj.clothing_equipment_type  # родитель
        return cls(
            id=parent_type.id,
            name=parent_type.name,
            nameKZ=parent_type.nameKZ,
            type_of_equipment={
                "name": orm_obj.name,
                "nameKZ": orm_obj.nameKZ,
            }
        )


class OtherBaseEquipmentTypeRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    @classmethod
    def from_orm(cls, orm_obj: OtherEquipmentTypeModel):
        parent_type = orm_obj.other_equipment_type  # родитель
        return cls(
            id=parent_type.id,
            name=parent_type.name,
            nameKZ=parent_type.nameKZ,
            type_of_equipment={
                "name": orm_obj.name,
                "nameKZ": orm_obj.nameKZ,
            }
        )

class EquipmentRead(EquipmentBase, ReadModel):
    army_equipment_type_model: Optional[ArmyBaseEquipmentTypeRead]
    clothing_equipment_type_model: Optional[ClothingBaseEquipmentTypeRead]
    other_equipment_type_model: Optional[OtherBaseEquipmentTypeRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
