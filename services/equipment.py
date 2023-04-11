from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (Equipment,
                    TypeClothingEquipment, 
                    TypeArmyEquipment, 
                    TypeOtherEquipment,
                    ClothingEquipment,
                    TypeClothingEquipmentModel,)
from schemas import (EquipmentCreate, 
                     EquipmentUpdate,
                     TypeClothingEquipmentRead, 
                     TypeArmyEquipmentRead, 
                     TypeOtherEquipmentRead)
from .base import ServiceBase

equipment = {
    "army_equipment": TypeArmyEquipment,
    "clothing_equipment": TypeClothingEquipment,
    "other_equipment": TypeOtherEquipment
}



class EquipmentService(ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_id(self, db: Session, id: str):
        equipment = super().get(db, id)
        if equipment is None:
            raise NotFoundException(detail="Equipment is not found!")
        return equipment

    def create(self, db: Session, body: EquipmentCreate):
        cls = equipment[body.type_of_equipment]
        equipment = cls(**body.dict())
        db.add(equipment)
        db.flush()
        return equipment
    
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


equipment_service = EquipmentService(Equipment)
