import uuid

from sqlalchemy import func, and_
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
                    ClothingEquipmentTypesModels,
                    TypeArmyEquipmentModel,
                    TypeOtherEquipmentModel)
from schemas import (EquipmentCreate,
                     EquipmentUpdate,
                     TypeClothingEquipmentRead,
                     TypeArmyEquipmentRead,
                     TypeOtherEquipmentRead)
from .base import ServiceBase
from .filter import add_filter_to_query

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
                                                              body.cloth_eq_models_id)[0]
            )
            body.cloth_eq_types_id = None
            body.cloth_eq_models_id = None
        equipment1 = cls(**body.dict(exclude_none=True))
        db.add(equipment1)
        db.flush()
        return equipment1

    def get_all_army_equipments(
            self, db: Session, skip: int = 0, limit: int = 10, filter: str = ''):
        army_equipments = db.query(TypeArmyEquipment)

        if filter != '':
            army_equipments = add_filter_to_query(army_equipments,
                                                  filter,
                                                  TypeArmyEquipment)

        army_equipments = (army_equipments
                           .offset(skip)
                           .limit(limit).all())

        total = db.query(TypeArmyEquipment).count()

        return {'total': total, 'objects': [TypeArmyEquipmentRead.from_orm(army_equipment)
                for army_equipment in army_equipments]}

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
            skip: int = 0, limit: int = 10, filter: str = ''):
        type_cloth_equipmets_list = db.query(TypeClothingEquipment)

        if filter != '':
            type_cloth_equipmets_list = add_filter_to_query(type_cloth_equipmets_list,
                                                            filter,
                                                            TypeClothingEquipment)

        type_cloth_equipmets_list = (type_cloth_equipmets_list
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

        total = db.query(TypeClothingEquipment).count()

        return {'total': total, 'objects': type_cloth_equipmets_read_list}

    def get_all_clothing_equipment_models(self, db: Session):
        return db.query(TypeClothingEquipmentModel).all()

    def get_clothing_equipment_model_by_id(self, db: Session, id: str):
        return (db.query(TypeClothingEquipmentModel)
                .filter(TypeClothingEquipmentModel.id==id)
                .first())

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
            skip: int = 0, limit: int = 10, filter: str = ''):

        other_equipments = db.query(TypeOtherEquipment)

        if filter != '':
            other_equipments = add_filter_to_query(other_equipments,
                                                  filter,
                                                  TypeOtherEquipment)

        other_equipments = (other_equipments
                           .offset(skip)
                           .limit(limit).all())

        total = db.query(TypeOtherEquipment).count()

        return {'total': total, 'objects': [TypeOtherEquipmentRead.from_orm(other_equipment)
                for other_equipment in other_equipments]}

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
    def update(self, db: Session, id: str, body: EquipmentUpdate):
        equipment = self.get_by_id(db, id)
        if not equipment:
            raise NotFoundException("Equipment not found")
        if body.type_of_equipment == "clothing_equipment":
            body.cloth_eq_types_models_id = (
                self.get_clothing_equipment_type_model_by_ids(db,
                                                              body.cloth_eq_types_id,
                                                              body.cloth_eq_models_id)[0]
            )
            body.cloth_eq_types_id = None
            body.cloth_eq_models_id = None
        for key, value in body.dict(exclude_none=True).items():
            setattr(equipment, key, value)
        db.add(equipment)
        db.flush()
        return equipment

    def create_army_eq_type(self, db, body):
        army_type = super().create(db, body, TypeArmyEquipment)
        return army_type

    def create_army_eq_model(self, db: Session, body):
        army_model = super().create(db, body, TypeArmyEquipmentModel)
        return army_model

    def create_other_eq_type(self, db, body):
        other_type = super().create(db, body, TypeOtherEquipment)
        return other_type

    def create_other_eq_model(self, db: Session, body):
        other_model = super().create(db, body, TypeOtherEquipmentModel)
        return other_model

    def create_cloth_eq_type(self, db, body):
        cloth_eq_type = TypeClothingEquipment(name=body.name,
                                              nameKZ=body.nameKZ)
        cloth_type = super().create(db, cloth_eq_type, TypeOtherEquipment)
        cloth_eq_types_models = []

        for model_id in body.model_ids:
            cloth_eq_types_models.append(
                self.get_clothing_equipment_model_by_id(db, model_id)
            )

        cloth_type.cloth_eq_types_models = cloth_eq_types_models

        db.add(cloth_type)
        db.flush()
        return cloth_type

    def create_cloth_eq_model(self, db: Session, body):
        cloth_model = super().create(db, body, TypeClothingEquipmentModel)
        return cloth_model

    def _get_user_clothing_type_query(self, db: Session, user_id: str):
        return (
            db.query(TypeClothingEquipment)
            .join(ClothingEquipmentTypesModels)
            .join(ClothingEquipment)
            .filter(
                ClothingEquipment.user_id == user_id
            )
        )



equipment_service = EquipmentService(Equipment)
