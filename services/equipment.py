import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (
    Equipment,
    TypeClothingEquipment,
    TypeArmyEquipment,
    TypeOtherEquipment,
    TypeClothingEquipmentModel,
    ArmyEquipment,
    ClothingEquipment,
    OtherEquipment,
    ClothingEquipmentTypesModels,
    TypeArmyEquipmentModel,
    TypeOtherEquipmentModel
)
from models.position import logger
from schemas import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentRead,
    TypeClothingEquipmentRead,
    TypeArmyEquipmentRead,
    TypeOtherEquipmentRead,
    TypeArmyEquipmentModelCreate,
    TypeClothingEquipmentModelCreate,
    TypeOtherEquipmentModelCreate,
    TypeClothingEquipmentUpdate,
    TypeArmyEquipmentCreate,
    TypeClothingEquipmentCreate,  # Импорт добавлен!
    TypeOtherEquipmentCreate,
    TypeClothingEquipmentModelSchema,
    TypeArmyEquipmentReadPagination,
    TypeOtherEquipmentReadPagination
)
from .base import ServiceBase
from .filter import add_filter_to_query


class EquipmentCreationError(Exception):
    """
    Кастомное исключение для ошибок создания моделей оборудования.
    """
    pass


# Словарь для соответствия типа оборудования и ORM-модели
equipment = {
    "army_equipment": ArmyEquipment,
    "clothing_equipment": ClothingEquipment,
    "other_equipment": OtherEquipment
}


class EquipmentService(ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    """
    Сервис для управления оборудованием (армейским, одеждой, прочим).
    """

    def get_by_id(self, db: Session, id: str):
        equipment_obj = db.query(Equipment).filter(Equipment.id == id).first()
        if equipment_obj is None:
            raise NotFoundException(detail=f"Equipment with id {id} not found!")
        equipment_type = equipment_obj.type_of_equipment
        cls = equipment[equipment_type]
        return db.query(cls).filter(cls.id == id).first()

    def create(self, db: Session, body: EquipmentCreate):
        if body.type_of_equipment not in equipment:
            raise NotFoundException(
                detail=f"Unknown type_of_equipment '{body.type_of_equipment}'"
            )
        cls = equipment[body.type_of_equipment]
        if body.type_of_equipment == "clothing_equipment":
            result = self.get_clothing_equipment_type_model_by_ids(
                db, body.cloth_eq_types_id, body.cloth_eq_models_id
            )
            if result is None:
                raise NotFoundException(
                    "Clothing equipment model not found for given type and model ids"
                )
            body.cloth_eq_types_models_id = result
            body.cloth_eq_types_id = None
            body.cloth_eq_models_id = None
        equipment_obj = cls(**body.dict(exclude_none=True))
        db.add(equipment_obj)
        db.flush()
        return equipment_obj

    def update(self, db: Session, id: str, body: EquipmentUpdate):
        equipment_obj = self.get_by_id(db, id)
        if not equipment_obj:
            raise NotFoundException("Equipment not found")
        if body.type_of_equipment == "clothing_equipment":
            body.cloth_eq_types_models_id = self.get_clothing_equipment_type_model_by_ids(
                db, body.cloth_eq_types_id, body.cloth_eq_models_id
            )
            body.cloth_eq_types_id = None
            body.cloth_eq_models_id = None
        for key, value in body.dict(exclude_none=True).items():
            setattr(equipment_obj, key, value)
        setattr(equipment_obj, 'updated_at', datetime.now())
        db.add(equipment_obj)
        db.flush()
        return equipment_obj

    def get_clothing_equipment_type_by_ids(self, db: Session, type_id: str, model_id: str):
        return (
            db.query(ClothingEquipmentTypesModels.id)
            .filter(
                ClothingEquipmentTypesModels.type_cloth_equipmets_id == type_id,
                ClothingEquipmentTypesModels.type_cloth_eq_models_id == model_id
            )
            .first()
        )

    def get_clothing_equipment_type_model_by_ids(self, db: Session, type_id: str, model_id: str):
        if not (type_id and model_id):
            return None
        res = self.get_clothing_equipment_type_by_ids(db, type_id, model_id)
        if res:
            return res[0]
        return None

    # ------------- Армейское оборудование ------------- #

    def get_army_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(TypeArmyEquipment).filter(TypeArmyEquipment.id == id).first()
        if not obj:
            raise NotFoundException(f"TypeArmyEquipment with id {id} not found!")
        return obj

    def create_army_eq_type(self, db: Session, body: TypeArmyEquipmentCreate):
        return super().create(db, body, TypeArmyEquipment)

    def create_army_eq_model(self, db: Session, body: TypeArmyEquipmentModelCreate):
        return super().create(db, body, TypeArmyEquipmentModel)

    def update_army_model(self, db: Session, id: str, body: TypeArmyEquipmentModelCreate):
        army_eq_model = self.get_army_equipment_model_by_id(db, id)
        if not army_eq_model:
            raise NotFoundException("Army equipment model not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(army_eq_model, key, value)
        setattr(army_eq_model, 'updated_at', datetime.now())
        db.add(army_eq_model)
        db.flush()
        return army_eq_model

    def delete_army_model(self, db: Session, id: str):
        army_eq_model = self.get_army_equipment_model_by_id(db, id)
        if not army_eq_model:
            raise NotFoundException("Army equipment model not found")
        db.delete(army_eq_model)
        db.flush()
        return True

    def get_army_equipment_model_by_id(self, db: Session, id: str):
        return db.query(TypeArmyEquipmentModel).filter(TypeArmyEquipmentModel.id == id).first()

    def get_all_army_equipments(self, db: Session, skip=0, limit=10, filter_str=''):
        query = db.query(TypeArmyEquipment)
        if filter_str:
            query = add_filter_to_query(query, filter_str, TypeArmyEquipment)
        objects = query.offset(skip).limit(limit).all()
        total = db.query(TypeArmyEquipment).count()
        return {
            'total': total,
            'objects': [TypeArmyEquipmentRead.from_orm(obj) for obj in objects]
        }

    # ------------- Одежда ------------- #

    def get_clothing_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(TypeClothingEquipment).filter(TypeClothingEquipment.id == id).first()
        if not obj:
            raise NotFoundException(f"TypeClothingEquipment with id {id} not found!")
        return obj

    def create_cloth_eq_type(self, db: Session, body: TypeClothingEquipmentCreate):
        cloth_type = self.get_clothing_equipment_type_by_name(db, body.name)
        if not cloth_type:
            new_type = TypeClothingEquipment(name=body.name, nameKZ=body.nameKZ)
            cloth_type = super().create(db, new_type, TypeClothingEquipment)
        if body.model_ids:
            for m_id in body.model_ids:
                if m_id:
                    link_data = {
                        'type_cloth_eq_models_id': m_id,
                        'type_cloth_equipmets_id': cloth_type.id
                    }
                    super().create(db, link_data, ClothingEquipmentTypesModels)
        db.add(cloth_type)
        db.flush()
        return cloth_type

    def create_cloth_eq_model(self, db: Session, body: TypeClothingEquipmentModelCreate):
        try:
            cloth_model = super().create(db, body, TypeClothingEquipmentModel)
            return cloth_model
        except Exception as e:
            logger.exception("Ошибка при создании модели оборудования: %s", e)
            raise EquipmentCreationError("Ошибка при создании модели оборудования") from e

    def update_type_clothing(self, db: Session, id: str, body: TypeClothingEquipmentUpdate):
        type_cloth = self.get_clothing_equipment_type_by_id(db, id)
        for key, value in body.dict(exclude_none=True).items():
            setattr(type_cloth, key, value)
        setattr(type_cloth, 'updated_at', datetime.now())
        db.add(type_cloth)
        db.flush()
        return type_cloth

    def delete_type_clothing(self, db: Session, id: str):
        type_cloth = self.get_clothing_equipment_type_by_id(db, id)
        db.delete(type_cloth)
        db.flush()
        return True

    def get_all_clothing_equipments(self, db: Session, skip=0, limit=10):
        query = db.query(TypeClothingEquipment)
        objects = query.offset(skip).limit(limit).all()
        if not objects:
            raise NotFoundException("Equipment not found")
        result = []
        for cloth_type in objects:
            models = db.query(TypeClothingEquipmentModel).filter(
                TypeClothingEquipmentModel.type_cloth_eq_types_id == cloth_type.id
            ).all()
            cloth_type_read = TypeClothingEquipmentRead.from_orm(cloth_type)
            cloth_type_read.type_cloth_eq_models = [
                TypeClothingEquipmentModelSchema.from_orm(m) for m in models
            ]
            result.append(cloth_type_read)
        total = db.query(TypeClothingEquipment).count()
        return {'total': total, 'objects': result}

    def get_all_clothing_equipment_models(self, db: Session):
        return db.query(TypeClothingEquipmentModel).all()

    def get_clothing_equipment_type_by_name(self, db: Session, name: str):
        return db.query(TypeClothingEquipment).filter(TypeClothingEquipment.name == name).first()

    # ------------- Прочее оборудование ------------- #

    def get_other_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(TypeOtherEquipment).filter(TypeOtherEquipment.id == id).first()
        if not obj:
            raise NotFoundException(f"TypeOtherEquipment with id {id} not found!")
        return obj

    def create_other_eq_type(self, db: Session, body: TypeOtherEquipmentCreate):
        return super().create(db, body, TypeOtherEquipment)

    def create_other_eq_model(self, db: Session, body: TypeOtherEquipmentModelCreate):
        return super().create(db, body, TypeOtherEquipmentModel)

    def update_other_type(self, db: Session, id: str, body: TypeOtherEquipmentCreate):
        obj = self.get_other_equipment_type_by_id(db, id)
        for key, value in body.dict(exclude_none=True).items():
            setattr(obj, key, value)
        setattr(obj, 'updated_at', datetime.now())
        db.add(obj)
        db.flush()
        return obj

    def delete_other_type(self, db: Session, id: str):
        obj = self.get_other_equipment_type_by_id(db, id)
        db.delete(obj)
        db.flush()
        return True

    def get_all_other_equipments(self, db: Session, skip=0, limit=10, filter_str=''):
        query = db.query(TypeOtherEquipment)
        if filter_str:
            query = add_filter_to_query(query, filter_str, TypeOtherEquipment)
        objects = query.offset(skip).limit(limit).all()
        total = db.query(TypeOtherEquipment).count()
        return {
            'total': total,
            'objects': [TypeOtherEquipmentRead.from_orm(o) for o in objects]
        }

    # ------------- Дополнительно ------------- #

    def get_all_available_equipments(self, db: Session, user_id: str, skip=0, limit=10):
        subquery = self._get_user_clothing_type_query(db, user_id)
        return (
            db.query(TypeClothingEquipment)
            .except_(subquery)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def _get_user_clothing_type_query(self, db: Session, user_id: str):
        return (
            db.query(TypeClothingEquipment)
            .join(ClothingEquipmentTypesModels)
            .join(ClothingEquipment)
            .filter(ClothingEquipment.user_id == user_id)
        )

    def get_all_clothing_equipments_by_user(self, db: Session, user_id: str, skip=0, limit=10):
        return (
            self._get_user_clothing_type_query(db, user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


equipment_service = EquipmentService(Equipment)
