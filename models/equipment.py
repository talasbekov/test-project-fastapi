from sqlalchemy import BigInteger, Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import hr_document_equipments


class Equipment(Model):

    __tablename__ = "equipments"
 
    
    type_of_equipment = Column(String, nullable=True)

    hr_documents = relationship("HrDocument", secondary=hr_document_equipments,
                                back_populates="equipments")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="equipments")
    
    __mapper_args__ = {
        "polymorphic_identity": "equipment",
        "polymorphic_on": type_of_equipment,
    }


class TypeArmyEquipmentModel(NamedModel):
    """Type of equipment. Example: AK-47, RPG-7, etc."""
    __tablename__ = "type_army_equipment_models"

    type_of_army_equipment_id = Column(UUID(as_uuid=True), ForeignKey("type_army_equipments.id"), nullable=True)
    army_equipments = relationship("ArmyEquipment", back_populates="type_of_army_equipment_model")
    type_of_army_equipment = relationship("TypeArmyEquipment", back_populates="type_of_army_equipment_models")


class TypeArmyEquipment(NamedModel):
    """Type of army equipment. Example: Автомат, РПГ, etc."""
    __tablename__ = "type_army_equipments"

    type_of_army_equipment_models = relationship("TypeArmyEquipmentModel", back_populates="type_of_army_equipment")

class ArmyEquipment(Equipment):

    type_of_army_equipment_model_id = Column(UUID(as_uuid=True), ForeignKey("type_army_equipment_models.id"), nullable=True)
    inventory_number = Column(String, nullable=True)
    count_of_ammo = Column(BigInteger, nullable=True)

    type_of_army_equipment_model = relationship("TypeArmyEquipmentModel", back_populates="army_equipments", uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "army_equipment",
    }

class TypeClothingEquipmentModel(NamedModel):
    """Type of equipment. Example: ШАПКА, ПОЛУЧЕК, ПОЛУЧЕК, etc."""
    __tablename__ = "type_clothing_equipment_models"
    
    type_of_clothing_equipment_id = Column(UUID(as_uuid=True), ForeignKey("type_clothing_equipments.id"), nullable=True)
    clothing_equipments = relationship("ClothingEquipment", back_populates="type_of_clothing_equipment_model")
    type_of_clothing_equipment = relationship("TypeClothingEquipment", back_populates="type_of_clothing_equipment_models")


class TypeClothingEquipment(NamedModel):
    """Type of clothing equipment. Example: ПАРАДНАЯ, ПОВСЕДНЕВНО-ПОСТОВАЯ, ТАКТИЧЕСКАЯ, etc."""
    __tablename__ = "type_clothing_equipments"

    type_of_clothing_equipment_models = relationship("TypeClothingEquipmentModel", back_populates="type_of_clothing_equipment")


class ClothingEquipment(Equipment):
    
    type_of_clothing_equipment_model_id = Column(UUID(as_uuid=True), ForeignKey("type_clothing_equipment_models.id"), nullable=True)
    type_of_clothing_equipment_model = relationship("TypeClothingEquipmentModel", back_populates="clothing_equipments", uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "clothing_equipment",
    }



class TypeOtherEquipmentModel(NamedModel):
    """Type of equipment. Example: HP laserjet 1020, HP laserjet 1020, etc."""
    __tablename__ = "type_other_equipment_models"
    
    type_of_other_equipment_id = Column(UUID(as_uuid=True), ForeignKey("type_other_equipments.id"), nullable=True)
    other_equipments = relationship("OtherEquipment", back_populates="type_of_other_equipment_model")
    type_of_other_equipment = relationship("TypeOtherEquipment", back_populates="type_of_other_equipment_models")

class TypeOtherEquipment(NamedModel):
    """Type of clothing equipment. Example: КОМПЬЮТЕР, КОМПЬЮТЕР, КОМПЬЮТЕР, etc."""
    __tablename__ = "type_other_equipments"

    type_of_other_equipment_models = relationship("TypeOtherEquipmentModel", back_populates="type_of_other_equipment")


class OtherEquipment(Equipment):
    
    type_of_other_equipment_model_id = Column(UUID(as_uuid=True), ForeignKey("type_other_equipment_models.id"), nullable=True)
    type_of_other_equipment_model = relationship("TypeOtherEquipmentModel", back_populates="other_equipments", uselist=False)

    __mapper_args__ = {
        "polymorphic_identity": "other_equipment",
    }
