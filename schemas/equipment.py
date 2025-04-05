from typing import Optional, List
from datetime import datetime
from pydantic import Field
from schemas.base import Model, ReadModel, ReadNamedModel, NamedModel

# ----------------------------------------------------
#              Общие схемы Equipment
# ----------------------------------------------------
class EquipmentBase(Model):
    """
    Общие поля для сущности Equipment.
    """
    type_of_equipment: Optional[str]
    army_equipment_type_model_id: Optional[str]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    clothing_type_association_id: Optional[str]
    other_equipment_type_model_id: Optional[str]
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
    army_equipment_type_models: Optional[List[ArmyEquipmentTypeModelRead]] = None

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
    clothing_equipment_models: Optional[List[ClothingEquipmentTypeModelRead]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ClothingEquipmentTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[ClothingEquipmentTypeRead]]


class ClothingEquipmentTypesModelsRead(ReadNamedModel):
    """
    Ассоциативная сущность, отражающая связь между типом и моделью одежды.
    """
    clothing_equipment_type_model: Optional[ClothingEquipmentTypeModelRead] = None
    clothing_equipment_type: Optional[ClothingEquipmentTypeRead] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ClothingEquipmentTypeModelCreate(NamedModel):
    pass


class ClothingEquipmentTypeCreate(NamedModel):
    """
    При создании типа одежды можно передать список идентификаторов моделей.
    """
    # model_ids: Optional[List[Optional[str]]] = None
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
    other_equipment_type_models: Optional[List[OtherEquipmentTypeModelRead]] = None

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
class EquipmentRead(EquipmentBase, ReadModel):
    """
    Схема для чтения Equipment, объединяющая общие поля и связанные объекты.
    """
    # Соответствие: ArmyEquipment.army_equipment_type_model -> army_object
    army_object: Optional[ArmyEquipmentTypeRead] = Field(None, alias='army_equipment_type_model')
    # Соответствие: ClothingEquipment.clothing_type_association -> clothes_object
    clothes_object: Optional[ClothingEquipmentTypesModelsRead] = Field(None, alias='clothing_type_association')
    # Соответствие: OtherEquipment.other_equipment_type_model -> other_object
    other_object: Optional[OtherEquipmentTypeRead] = Field(None, alias='other_equipment_type_model')

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
