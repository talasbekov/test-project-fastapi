from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from exceptions.client import NotFoundException
from models import (
    Equipment,
    ClothingEquipmentType,        # вместо ClothingEquipmentType
    ArmyEquipmentType,            # вместо ArmyEquipmentType
    OtherEquipmentType,           # вместо OtherEquipmentType
    ClothingEquipmentTypeModel,   # вместо ClothingEquipmentTypeModel
    ArmyEquipment,
    ClothingEquipment,
    OtherEquipment,
    ArmyEquipmentTypeModel,       # вместо ArmyEquipmentTypeModel
    OtherEquipmentTypeModel       # вместо OtherEquipmentTypeModel
)
from models.position import logger
from schemas import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentRead,

    # Одежда
    ClothingEquipmentTypeRead,            # (был ClothingEquipmentTypeRead)
    ClothingEquipmentTypeUpdate,          # (был ClothingEquipmentTypeUpdate)
    ClothingEquipmentTypeModelRead,       # (был ClothingEquipmentTypeModelSchema)
    ClothingEquipmentTypeCreate,          # (был ClothingEquipmentTypeCreate)
    ClothingEquipmentTypeModelCreate,     # (был ClothingEquipmentTypeModelCreate)

    # Армейское
    ArmyEquipmentTypeRead,               # (был ArmyEquipmentTypeRead)
    ArmyEquipmentTypeCreate,             # (был ArmyEquipmentTypeCreate)
    ArmyEquipmentTypeModelCreate,        # (был ArmyEquipmentTypeModelCreate)
    ArmyEquipmentTypeReadPagination,     # (был ArmyEquipmentTypeReadPagination)

    # Прочее
    OtherEquipmentTypeRead,              # (был OtherEquipmentTypeRead)
    OtherEquipmentTypeCreate,            # (был OtherEquipmentTypeCreate)
    OtherEquipmentTypeModelCreate,       # (был OtherEquipmentTypeModelCreate)
    OtherEquipmentTypeReadPagination     # (был OtherEquipmentTypeReadPagination)
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

    def get_by_id(self, db: Session, equipment_id: str):
        equipment_obj = db.query(Equipment).options(
            selectinload(Equipment.user),
              # Для наследников: ArmyEquipment, ClothingEquipment, OtherEquipment
              selectinload(ArmyEquipment.army_equipment_type_model),
              selectinload(ClothingEquipment.clothing_equipment_type_model),
              selectinload(OtherEquipment.other_equipment_type_model),
          ).filter(Equipment.id == equipment_id).first()
        return equipment_obj

    def create(self, db: Session, body: EquipmentCreate):
        if body.type_of_equipment not in equipment:
            raise NotFoundException(
                detail=f"Unknown type_of_equipment '{body.type_of_equipment}'"
            )
        cls = equipment[body.type_of_equipment]
        equipment_obj = cls(**body.dict(exclude_none=True))
        db.add(equipment_obj)
        db.flush()
        return equipment_obj

    def update(self, db: Session, id: str, body: EquipmentUpdate):
        equipment_obj = self.get_by_id(db, id)
        if not equipment_obj:
            raise NotFoundException("Equipment not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(equipment_obj, key, value)
        setattr(equipment_obj, 'updated_at', datetime.now())
        db.add(equipment_obj)
        db.flush()
        return equipment_obj

    # ------------- Армейское оборудование ------------- #

    def get_army_equipment_model_by_id(self, db: Session, id: str):
        return db.query(ArmyEquipmentTypeModel).filter(ArmyEquipmentTypeModel.id == id).first()

    def get_all_army_equipment_models(self, db: Session):
        models = db.query(ArmyEquipmentTypeModel).all()
        if not models:
            raise NotFoundException("No Army Equipment Models found")
        return models

    def get_all_army_equipments(self, db: Session, skip=0, limit=10, filter_str=''):
        query = db.query(ArmyEquipmentType)
        if filter_str:
            query = add_filter_to_query(query, filter_str, ArmyEquipmentType)
        objects = query.offset(skip).limit(limit).all()
        total = db.query(ArmyEquipmentType).count()
        return {
            'total': total,
            'objects': [ArmyEquipmentTypeRead.from_orm(obj) for obj in objects]
        }

    def get_army_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(ArmyEquipmentType).filter(ArmyEquipmentType.id == id).first()
        if not obj:
            raise NotFoundException(f"ArmyEquipmentType with id {id} not found!")
        return obj

    def create_army_eq_type(self, db: Session, body: ArmyEquipmentTypeCreate):
        return super().create(db, body, ArmyEquipmentType)

    def create_army_eq_model(self, db: Session, body: ArmyEquipmentTypeModelCreate):
        body_type = db.query(ArmyEquipmentType).filter(
            ArmyEquipmentType.id == body.army_equipment_type_id
        ).first()

        if not body_type:
            raise HTTPException(
                status_code=400,
                detail="Тип с таким army_equipment_type_id не найден."
            )
        return super().create(db, body, ArmyEquipmentTypeModel)

    def update_army_model(self, db: Session, id: str, body: ArmyEquipmentTypeModelCreate):
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

    # ------------- Одежда ------------- #

    def get_all_clothing_equipments(self, db: Session, skip=0, limit=10, filter_str=''):
        query = db.query(ClothingEquipmentType)
        if filter_str:
            query = add_filter_to_query(query, filter_str, ClothingEquipmentType)
        objects = query.offset(skip).limit(limit).all()
        total = db.query(ClothingEquipmentType).count()
        return {
            'total': total,
            'objects': [ClothingEquipmentTypeRead.from_orm(obj) for obj in objects]
        }

    def get_all_clothing_equipment_models(self, db: Session):
        return db.query(ClothingEquipmentTypeModel).all()

    def get_clothing_equipment_type_by_name(self, db: Session, name: str):
        return db.query(ClothingEquipmentType).filter(ClothingEquipmentType.name == name).first()

    def get_clothing_equipment_model_by_id(self, db: Session, id: str):
        if not id:
            raise ValueError("ID must be provided")
        model = db.query(ClothingEquipmentTypeModel).filter(ClothingEquipmentTypeModel.id == id).first()
        if model is None:
            raise NotFoundException(f"ClothingEquipmentModel with id {id} not found")
        return model

    def get_clothing_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(ClothingEquipmentType).filter(ClothingEquipmentType.id == id).first()
        if not obj:
            raise NotFoundException(f"ClothingEquipmentType with id {id} not found!")
        return obj

    def create_clothing_equipment_type(self, db: Session, body: ClothingEquipmentTypeCreate):
        return super().create(db, body, ClothingEquipmentType)

    def create_clothing_equipment_model(self, db: Session, body: ClothingEquipmentTypeModelCreate):
        body_type = db.query(ClothingEquipmentType).filter(
            ClothingEquipmentType.id == body.clothing_equipment_type_id
        ).first()

        if not body_type:
            raise HTTPException(
                status_code=400,
                detail="Тип с таким clothing_equipment_type_id не найден."
            )
        return super().create(db, body, ClothingEquipmentTypeModel)

    def update_type_clothing(self, db: Session, id: str, body: ClothingEquipmentTypeUpdate):
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

    # ------------- Прочее оборудование ------------- #

    def get_other_equipment_type_by_id(self, db: Session, id: str):
        obj = db.query(OtherEquipmentType).filter(OtherEquipmentType.id == id).first()
        if not obj:
            raise NotFoundException(f"OtherEquipmentType with id {id} not found!")
        return obj

    def get_all_other_equipment_models(self, db: Session):
        return db.query(OtherEquipmentTypeModel).all()

    def get_other_equipment_model_by_id(self, db: Session, id: str):
        if not id:
            raise ValueError("ID must be provided")
        model = db.query(OtherEquipmentTypeModel).filter(OtherEquipmentTypeModel.id == id).first()
        if model is None:
            raise NotFoundException(f"OtherEquipmentModel with id {id} not found")
        return model

    def create_other_eq_type(self, db: Session, body: OtherEquipmentTypeCreate):
        return super().create(db, body, OtherEquipmentType)

    def create_other_eq_model(self, db: Session, body: OtherEquipmentTypeModelCreate):
        return super().create(db, body, OtherEquipmentTypeModel)

    def update_other_type(self, db: Session, id: str, body: OtherEquipmentTypeCreate):
        obj = self.get_other_equipment_type_by_id(db, id)
        for key, value in body.dict(exclude_none=True).items():
            setattr(obj, key, value)
        setattr(obj, 'updated_at', datetime.now())
        db.add(obj)
        db.flush()
        return obj

    def update_other_model(self, db: Session, id: str, body: OtherEquipmentTypeModelCreate):
        obj = self.get_other_equipment_model_by_id(db, id)
        if not obj:
            raise ValueError(f"OtherEquipmentModel with ID {id} not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(obj, key, value)
        obj.updated_at = datetime.now()
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete_other_type(self, db: Session, id: str):
        obj = self.get_other_equipment_type_by_id(db, id)
        db.delete(obj)
        db.flush()
        return True

    def get_all_other_equipments(self, db: Session, skip=0, limit=10, filter_str=''):
        query = db.query(OtherEquipmentType)
        if filter_str:
            query = add_filter_to_query(query, filter_str, OtherEquipmentType)
        objects = query.offset(skip).limit(limit).all()
        total = db.query(OtherEquipmentType).count()
        return {
            'total': total,
            'objects': [OtherEquipmentTypeRead.from_orm(o) for o in objects]
        }

    # ------------- Дополнительно ------------- #

    def get_all_available_equipments(self, db: Session, user_id: str, skip=0, limit=10):
        subquery = self._get_user_clothing_type_query(db, user_id)
        return (
            db.query(ClothingEquipmentType)
            .except_(subquery)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def _get_user_clothing_type_query(self, db: Session, user_id: str):
        return (
            db.query(ClothingEquipmentType)
            .join(ClothingEquipmentTypeModel)
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
