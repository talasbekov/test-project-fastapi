from sqlalchemy import (
    BigInteger,
    Column,
    String,
    UUID,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import hr_document_equipments


class Equipment(Model):

    __tablename__ = "hr_erp_equipments"

    date_from = Column(TIMESTAMP, nullable=True)
    document_number = Column(String, nullable=True)
    document_link = Column(String, nullable=True)

    type_of_equipment = Column(String, nullable=True)

    hr_documents = relationship("HrDocument",
                                secondary=hr_document_equipments,
                                back_populates="equipments")
    inventory_count = Column(BigInteger, nullable=True)
    inventory_number = Column(String, nullable=True)
    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="equipments")

    __mapper_args__ = {
        "polymorphic_identity": "equipment",
        "polymorphic_on": type_of_equipment,
    }


class TypeArmyEquipmentModel(NamedModel):
    """Type of equipment. Example: AK-47, RPG-7, etc."""
    __tablename__ = "hr_erp_type_ar_equip_models"

    type_of_army_equipment_id = Column(
        String(),
        ForeignKey("hr_erp_type_army_equipments.id"),
        nullable=True)
    army_equipments = relationship(
        "ArmyEquipment",
        back_populates="type_of_army_equipment_model")
    type_of_army_equipment = relationship(
        "TypeArmyEquipment",
        back_populates="type_of_army_equipment_models")


class TypeArmyEquipment(NamedModel):
    """Type of army equipment. Example:
    Автомат, РПГ, etc."""
    __tablename__ = "hr_erp_type_army_equipments"

    type_of_army_equipment_models = relationship(
        "TypeArmyEquipmentModel",
        back_populates="type_of_army_equipment")


class ArmyEquipment(Equipment):

    type_of_army_equipment_model_id = Column(
        String(),
        ForeignKey("hr_erp_type_ar_equip_models.id"),
        nullable=True)
    count_of_ammo = Column(BigInteger, nullable=True)

    type_of_army_equipment_model = relationship(
        "TypeArmyEquipmentModel",
        back_populates="army_equipments",
        uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "army_equipment",
    }


class TypeClothingEquipmentModel(NamedModel):
    """Type of equipment. Example:
    ШАПКА, ПОЛУЧЕК, ПОЛУЧЕК, etc."""
    __tablename__ = "hr_erp_type_cloth_eq_models"

    cloth_eq_types_models = relationship(
        "ClothingEquipmentTypesModels",
        back_populates="type_cloth_eq_models")


class TypeClothingEquipment(NamedModel):  # obj.
    """Type of clothing equipment. Example:
    ПАРАДНАЯ, ПОВСЕДНЕВНО-ПОСТОВАЯ, ТАКТИЧЕСКАЯ, etc."""
    __tablename__ = "hr_erp_type_cloth_equipmets"

    cloth_eq_types_models = relationship(
        "ClothingEquipmentTypesModels",
        back_populates="type_cloth_equipmets"
)

class ClothingEquipmentTypesModels(Model):
    __tablename__ = 'hr_erp_cloth_eq_types_models'

    type_cloth_eq_models_id = Column(String(),
                                    ForeignKey("hr_erp_type_cloth_eq_models.id"),
                                    nullable=True)
    type_cloth_eq_models = relationship("TypeClothingEquipmentModel",
                                    back_populates="cloth_eq_types_models",
                                    uselist=False)

    type_cloth_equipmets_id = Column(String(),
                                    ForeignKey("hr_erp_type_cloth_equipmets.id"),
                                    nullable=True)
    type_cloth_equipmets = relationship("TypeClothingEquipment",
                                    back_populates="cloth_eq_types_models",
                                    uselist=False)

    clothing_equipments = relationship(
        "ClothingEquipment",
        back_populates="cloth_eq_types_models")


class ClothingEquipment(Equipment):
    cloth_eq_types_models_id = Column(String(), ForeignKey(
        "hr_erp_cloth_eq_types_models.id"), nullable=True)
    cloth_eq_types_models = relationship(
        "ClothingEquipmentTypesModels",
        back_populates="clothing_equipments",
        uselist=False)
    clothing_size = Column(String, nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "clothing_equipment",
    }


class TypeOtherEquipmentModel(NamedModel):
    """Type of equipment. Example: HP laserjet 1020, HP laserjet 1020, etc."""
    __tablename__ = "hr_erp_type_oth_eq_models"

    type_of_other_equipment_id = Column(
        String(),
        ForeignKey("hr_erp_type_other_equipments.id"),
        nullable=True)
    other_equipments = relationship(
        "OtherEquipment",
        back_populates="type_of_other_equipment_model")
    type_of_other_equipment = relationship(
        "TypeOtherEquipment",
        back_populates="type_of_other_equipment_models")


class TypeOtherEquipment(NamedModel):
    """Type of clothing equipment. Example: КОМПЬЮТЕР, КОМПЬЮТЕР, КОМПЬЮТЕР, etc."""
    __tablename__ = "hr_erp_type_other_equipments"

    type_of_other_equipment_models = relationship(
        "TypeOtherEquipmentModel",
        back_populates="type_of_other_equipment")


class OtherEquipment(Equipment):

    type_of_other_equipment_model_id = Column(
        String(),
        ForeignKey("hr_erp_type_oth_eq_models.id"),
        nullable=True)
    type_of_other_equipment_model = relationship(
        "TypeOtherEquipmentModel",
        back_populates="other_equipments",
        uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "other_equipment",
    }
