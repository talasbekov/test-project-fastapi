from sqlalchemy import BigInteger, Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import hr_document_equipments


class Equipment(Model):

    __tablename__ = "equipments"

    quantity = Column(BigInteger, nullable=True)
    
    type_of_equipment = Column(String, nullable=True)

    hr_documents = relationship("HrDocument", secondary=hr_document_equipments,
                                back_populates="equipments")

class TypeArmyEquipmentModel(NamedModel):
    """Type of equipment. Example: AK-47, RPG-7, etc."""
    __tablename__ = "type_equipments"

    type_of_army_equipment_id = Column(UUID(as_uuid=True), ForeignKey("type_army_equipments.id"), nullable=True)
    army_equipments = relationship("ArmyEquipment", back_populates="type_of_army_equipment_model")

class TypeArmyEquipment(NamedModel):
    """Type of army equipment. Example: Автомат, РПГ, etc."""
    __tablename__ = "type_army_equipments"

    type_of_equipments = relationship("TypeEquipment", back_populates="type_of_army_equipment")

class ArmyEquipment(Equipment):

    type_of_army_equipment_model_id = Column(UUID(as_uuid=True), ForeignKey("type_army_equipment_models.id"), nullable=True)
    inventory_number = Column(String, nullable=True)
    count_of_ammo = Column(BigInteger, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "army_equipment",
    }


class TypeClothingEquipment(NamedModel):
    """Type of clothing equipment. Example: ПАРАДНАЯ, ПОВСЕДНЕВНО-ПОСТОВАЯ, ТАКТИЧЕСКАЯ, etc."""
    __tablename__ = "type_clothing_equipments"

    type_of_clothing_equipments = relationship("TypeClothingEquipment", back_populates="type_of_clothing_equipment")


class ClothingEquipment(Equipment):

    __mapper_args__ = {
        "polymorphic_identity": "clothing_equipment",
    }
