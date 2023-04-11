from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (Equipment,
                    TypeClothingEquipment, 
                    TypeArmyEquipment, 
                    TypeOtherEquipment,
                    ClothingEquipment,
                    TypeClothingEquipmentModel,
                    ArmyEquipment,
                    ClothingEquipment,
                    OtherEquipment)
from schemas import (EquipmentCreate, 
                     EquipmentUpdate,
                     TypeClothingEquipmentRead, 
                     TypeArmyEquipmentRead, 
                     TypeOtherEquipmentRead)
from .base import ServiceBase

equipment = {
    "army_equipment": ArmyEquipment,
    "clothing_equipment": ClothingEquipment,
    "other_equipment": OtherEquipment
}



class EquipmentService(ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_id(self, db: Session, id: str):
        equipment_obj = db.query(Equipment).filter(Equipment.id == id).first()
        equipment_type = equipment_obj.type_of_equipment
        cls = equipment[equipment_type]
        return db.query(cls).filter(cls.id == id).first()

    
    def get_all_army_equipments(self, db: Session, skip: int = 0, limit: int = 10):
        return [TypeArmyEquipmentRead.from_orm(army_equipment) for army_equipment in db.query(TypeArmyEquipment).offset(skip).limit(limit).all()]
    
    def get_all_clothing_equipments(self, db: Session, skip: int = 0, limit: int = 10):
        return [TypeClothingEquipmentRead.from_orm(clothing_equipment) for clothing_equipment in db.query(TypeClothingEquipment).offset(skip).limit(limit).all()]
    
    def get_all_other_equipments(self, db: Session, skip: int = 0, limit: int = 10):
        return [TypeOtherEquipmentRead.from_orm(other_equipment) for other_equipment in db.query(TypeOtherEquipment).offset(skip).limit(limit).all()]
    
    def get_all_available_equipments(self, db: Session, user_id: str, skip: int = 0, limit: int = 10): 
     
        history = db.query(ClothingEquipment.type_of_clothing_equipment_model_id).filter(
            ClothingEquipment.user_id == user_id
        ).distinct().subquery()

        # Query for all clothing types which the user does not have in the history
        return db.query(TypeClothingEquipment).filter(
            ~TypeClothingEquipment.type_of_clothing_equipment_models.any(
                TypeClothingEquipmentModel.id == history.c.type_of_clothing_equipment_model_id
            )
        ).offset(skip).limit(limit).all()

    def create(self, db: Session, body: EquipmentCreate):
        cls = equipment[body.type_of_equipment]
        equipment1 = cls(**body.dict(exclude_none=True))
        db.add(equipment1)
        db.flush()
        return equipment1
    
    def update(self, db: Session, id: str, body: EquipmentUpdate):
        equipment = self.get_by_id(db, id)
        if not equipment:
            raise NotFoundException("Equipment not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(equipment, key, value)
        db.add(equipment)
        db.flush()
        return equipment



equipment_service = EquipmentService(Equipment)
