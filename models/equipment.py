from sqlalchemy import (
    BigInteger,
    Column,
    String,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from models import Model, NamedModel  # Ваши базовые классы
from models.association import hr_document_equipments


# ------------------------------------------------------------------
#  Полиморфная базовая модель Equipment
# ------------------------------------------------------------------
class Equipment(Model):
    __tablename__ = "hr_erp_equipments"

    date_from = Column(TIMESTAMP(timezone=True), nullable=True)
    date_to = Column(TIMESTAMP(timezone=True), nullable=True)
    document_number = Column(String, nullable=True)
    document_link = Column(String, nullable=True)

    # Поле для полиморфного определения, какой подкласс использовать
    type_of_equipment = Column(String, nullable=True)

    inventory_count = Column(BigInteger, nullable=True)
    inventory_number = Column(String, nullable=True)

    user_id = Column(String, ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="equipments")

    hr_documents = relationship(
        "HrDocument",
        secondary=hr_document_equipments,
        back_populates="equipments"
    )

    __mapper_args__ = {
        "polymorphic_identity": "equipment",
        "polymorphic_on": type_of_equipment,
    }


# ------------------------------------------------------------------
#  Армейское оборудование
# ------------------------------------------------------------------

class ArmyEquipmentType(NamedModel):
    """
    Прежнее: TypeArmyEquipment. Пример: «Автомат», «РПГ».
    """
    __tablename__ = "hr_erp_army_equipment_types"

    army_equipment_type_models = relationship(
        "ArmyEquipmentTypeModel",
        back_populates="army_equipment_type",
        cascade="all, delete-orphan"
    )


class ArmyEquipmentTypeModel(NamedModel):
    """
    Прежнее: TypeArmyEquipmentModel. Пример: «АК-47».
    """
    __tablename__ = "hr_erp_army_equipment_type_models"

    army_equipment_type_id = Column(
        String,
        ForeignKey("hr_erp_army_equipment_types.id"),
        nullable=True
    )
    army_equipment_type = relationship(
        "ArmyEquipmentType",
        back_populates="army_equipment_type_models"
    )
    # Список конкретных единиц оборудования
    army_equipments = relationship(
        "ArmyEquipment",
        back_populates="army_equipment_type_model"
    )


class ArmyEquipment(Equipment):
    """
    Наследник Equipment: конкретный экземпляр армейского оборудования.
    """
    __mapper_args__ = {
        "polymorphic_identity": "army_equipment",
    }

    # Внешний ключ на модель
    army_equipment_type_model_id = Column(
        String,
        ForeignKey("hr_erp_army_equipment_type_models.id"),
        nullable=True
    )

    count_of_ammo = Column(BigInteger, nullable=True)

    # Связь "один к одному/многим" (но uselist=False для одного объекта)
    army_equipment_type_model = relationship(
        "ArmyEquipmentTypeModel",
        back_populates="army_equipments",
        uselist=False
    )

# ------------------------------------------------------------------
#  Одежда
# ------------------------------------------------------------------
class ClothingEquipmentType(NamedModel):
    __tablename__ = "hr_erp_clothing_equipment_types"

    clothing_equipment_type_models = relationship(
        "ClothingEquipmentTypeModel",
        back_populates="clothing_equipment_type",
        cascade="all, delete-orphan"
    )


class ClothingEquipmentTypeModel(NamedModel):
    __tablename__ = "hr_erp_clothing_equipment_type_models"

    clothing_equipment_type_id = Column(
        String,
        ForeignKey("hr_erp_clothing_equipment_types.id"),
        nullable=True
    )
    # This is the existing relationship to the parent clothing_equipment_type
    clothing_equipment_type = relationship(
        "ClothingEquipmentType",
        back_populates="clothing_equipment_type_models",
        uselist=False
    )
    clothing_equipments = relationship(
        "ClothingEquipment",
        back_populates="clothing_equipment_type_model"
    )


class ClothingEquipment(Equipment):
    __mapper_args__ = {
        "polymorphic_identity": "clothing_equipment",
    }

    clothing_equipment_type_model_id = Column(
        String,
        ForeignKey("hr_erp_clothing_equipment_type_models.id"),
        nullable=True
    )
    # Связь "один к одному/многим" (но uselist=False для одного объекта)
    clothing_equipment_type_model = relationship(
        "ClothingEquipmentTypeModel",
        back_populates="clothing_equipments",
        uselist=False
    )

    clothing_size = Column(String, nullable=True)


# ------------------------------------------------------------------
#  Прочее оборудование
# ------------------------------------------------------------------
class OtherEquipmentType(NamedModel):
    """
    Прежнее: TypeOtherEquipment. Пример: «Компьютер», «Принтер».
    """
    __tablename__ = "hr_erp_other_equipment_types"

    other_equipment_type_models = relationship(
        "OtherEquipmentTypeModel",
        back_populates="other_equipment_type",
        cascade="all, delete-orphan"
    )




class OtherEquipmentTypeModel(NamedModel):
    """
    Прежнее: TypeOtherEquipmentModel. Пример: «HP LaserJet 1020».
    """
    __tablename__ = "hr_erp_other_equipment_type_models"

    other_equipment_type_id = Column(
        String,
        ForeignKey("hr_erp_other_equipment_types.id"),
        nullable=True
    )
    other_equipment_type = relationship(
        "OtherEquipmentType",
        back_populates="other_equipment_type_models"
    )
    other_equipments = relationship(
        "OtherEquipment",
        back_populates="other_equipment_type_model"
    )


class OtherEquipment(Equipment):
    """
    Наследник Equipment для 'прочего' оборудования.
    """
    __mapper_args__ = {
        "polymorphic_identity": "other_equipment",
    }

    other_equipment_type_model_id = Column(
        String,
        ForeignKey("hr_erp_other_equipment_type_models.id"),
        nullable=True
    )

    other_equipment_type_model = relationship(
        "OtherEquipmentTypeModel",
        back_populates="other_equipments",
        uselist=False
    )
