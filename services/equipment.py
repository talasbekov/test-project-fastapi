import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (Equipment,
                    TypeClothingEquipment,
                    TypeArmyEquipment,
                    TypeOtherEquipment,
                    TypeClothingEquipmentModel,
                    ArmyEquipment,
                    ClothingEquipment,
                    OtherEquipment,
                    ClothingEquipmentTypesModels)
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


class EquipmentService(
        ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_id(self, db: Session, id: str):
        equipment_obj = db.query(Equipment).filter(Equipment.id == id).first()
        equipment_type = equipment_obj.type_of_equipment
        cls = equipment[equipment_type]
        return db.query(cls).filter(cls.id == id).first()

    def create(self, db: Session, body: EquipmentCreate):
        cls = equipment[body.type_of_equipment]
        if body.type_of_equipment == "clothing_equipment":
            body.cloth_eq_types_models_id = (
                self.get_clothing_equipment_type_model_by_ids(db,
                                                              body.cloth_eq_types_id,
                                                              body.cloth_eq_models_id)
            )
        equipment1 = cls(**body.dict(exclude_none=True))
        db.add(equipment1)
        db.flush()
        return equipment1

    def get_all_army_equipments(
            self, db: Session, skip: int = 0, limit: int = 10):

        army_equipments = (db.query(TypeArmyEquipment)
                           .offset(skip)
                           .limit(limit).all())

        return [TypeArmyEquipmentRead.from_orm(army_equipment)
                for army_equipment in army_equipments]

    def get_clothing_equipment_type_model_by_ids(
            self, db: Session,
            type_id: str,
            model_id: str
    ):
        clothing_equipment_type_model_id = \
            (db.query(ClothingEquipmentTypesModels.id)
             .filter(ClothingEquipmentTypesModels.type_cloth_equipmets_id == type_id,
                     ClothingEquipmentTypesModels.type_cloth_eq_models_id == model_id)
             .first()
            )
        return clothing_equipment_type_model_id



    def get_all_clothing_equipments(
            self, db: Session,
            skip: int = 0, limit: int = 10):

        type_cloth_equipmets_list = (db.query(TypeClothingEquipment)
                                         .offset(skip).limit(limit).all())

        if not type_cloth_equipmets_list:
            raise NotFoundException("Equipment not found")
        type_cloth_equipmets_read_list = []
        for type_clothing_equipment in type_cloth_equipmets_list:
            clothing_equipment_models = (db.query(TypeClothingEquipmentModel)
                        .join(ClothingEquipmentTypesModels)
                        .filter(ClothingEquipmentTypesModels.type_cloth_equipmets_id
                                == type_clothing_equipment.id)
                        .offset(skip)
                        .limit(limit)
                        .all()
            )
            type_clothing_equipment_read = TypeClothingEquipmentRead.from_orm(
                type_clothing_equipment)
            type_clothing_equipment_read.type_cloth_eq_models = (
                clothing_equipment_models
            )
            type_cloth_equipmets_read_list.append(
                type_clothing_equipment_read)

        return type_cloth_equipmets_read_list

    def get_all_clothing_equipment_models(self, db: Session):
        return db.query(TypeClothingEquipmentModel).all()

    def get_clothing_equipment_models_count_by_user(
            self, db: Session, user_id: str):
        res = (
            db.query(TypeClothingEquipmentModel.name,
                     func.count(
                         ClothingEquipmentTypesModels.type_cloth_equipmets_id)
                     )
            .join(ClothingEquipmentTypesModels)
            .join(ClothingEquipment)
            .filter(ClothingEquipment.user_id == user_id)
            .group_by(TypeClothingEquipmentModel.name)
            .all()
        )
        return res

    def get_clothing_equipments_type_count(self, db: Session):
        return db.query(TypeClothingEquipment).count()

    def get_all_other_equipments(
            self, db: Session,
            skip: int = 0, limit: int = 10):

        other_equipments = (db.query(TypeOtherEquipment)
                            .offset(skip)
                            .limit(limit).all())

        return [TypeOtherEquipmentRead.from_orm(other_equipment)
                for other_equipment in other_equipments]

    def get_all_available_equipments(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 10):

        user_clothing_type = self._get_user_clothing_type_query(db, user_id)

        return (
            db.query(TypeClothingEquipment)
            .except_(user_clothing_type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_clothing_equipments_by_user(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 10):

        return (
            self._get_user_clothing_type_query(db, user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def _get_user_clothing_type_query(self, db: Session, user_id: str):
        return (
            db.query(TypeClothingEquipment)
            .join(ClothingEquipmentTypesModels)
            .join(ClothingEquipment)
            .filter(
                ClothingEquipment.user_id == user_id
            )
        )

    def update(self, db: Session, id: str, body: EquipmentUpdate):
        equipment = self.get_by_id(db, id)
        if not equipment:
            raise NotFoundException("Equipment not found")
        if body.type_of_equipment == "clothing_equipment":
            body.cloth_eq_types_models_id = (
                self.get_clothing_equipment_type_model_by_ids(db,
                                                              body.cloth_eq_types_id,
                                                              body.cloth_eq_models_id)
            )
        for key, value in body.dict(exclude_none=True).items():
            setattr(equipment, key, value)
        db.add(equipment)
        db.flush()
        return equipment


equipment_service = EquipmentService(Equipment)
