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
                     TypeOtherEquipmentRead,
                     TypeArmyEquipmentModelCreate,
                     TypeClothingEquipmentModelCreate,
                     TypeOtherEquipmentModelCreate,
                     TypeClothingEquipmentUpdate,
                     TypeArmyEquipmentCreate,
                     TypeOtherEquipmentCreate,
                     TypeClothingEquipmentModelSchema)
from .base import ServiceBase
from .filter import add_filter_to_query
from datetime import datetime
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

    def get_clothing_equipment_type_by_id(self, db: Session, id: str):
        type_cloth = (db.query(TypeClothingEquipment)
                      .filter(TypeClothingEquipment.id == id)
                      .first())
        if type_cloth is None:
            raise NotFoundException(
                detail=f"TypeClothingEquipment with id {id} not found!")
        return type_cloth

    def get_army_equipment_type_by_id(self, db: Session, id: str):
        type_army = (db.query(TypeArmyEquipment)
                     .filter(TypeArmyEquipment.id == id)
                     .first())
        if type_army is None:
            raise NotFoundException(
                detail=f"TypeArmyEquipment with id {id} not found!")
        return type_army

    def get_other_equipment_type_by_id(self, db: Session, id: str):
        type_other = (db.query(TypeOtherEquipment)
                      .filter(TypeOtherEquipment.id == id)
                      .first())
        if type_other is None:
            raise NotFoundException(
                detail=f"TypeArmyEquipment with id {id} not found!")
        return type_other

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
                        .filter(TypeClothingEquipmentModel.type_cloth_eq_types_id
                                == type_clothing_equipment.id)
                        .offset(skip)
                        .limit(limit)
                        .all()
            )
            print(i.__dict__ for i in clothing_equipment_models)
            type_clothing_equipment_read = TypeClothingEquipmentRead.from_orm(
                type_clothing_equipment)
            
            clothing = [TypeClothingEquipmentModelSchema.from_orm(i) for i in clothing_equipment_models]
            print(clothing)
            type_clothing_equipment_read.type_cloth_eq_models = (
                clothing
            )
            print(type_clothing_equipment_read)
            type_cloth_equipmets_read_list.append(
                type_clothing_equipment_read)

        total = db.query(TypeClothingEquipment).count()

        return {'total': total, 'objects': type_cloth_equipmets_read_list}

    def get_all_clothing_equipment_models(self, db: Session):
        return db.query(TypeClothingEquipmentModel).all()
    
    def update_cloth_model(self, db: Session, id: str, body: TypeClothingEquipmentModelCreate):
        cloth_eq_model = self.get_cloth_equipment_model_by_id(db, id)
        if not cloth_eq_model:
            raise NotFoundException("Clothing equipment model not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(cloth_eq_model, key, value)
        setattr(cloth_eq_model, 'updated_at', datetime.now())
        db.add(cloth_eq_model)
        db.flush()
        return cloth_eq_model
    
    def delete_cloth_model(self, db: Session, id: str):
        cloth_eq_model = self.get_cloth_equipment_model_by_id(db, id)
        if not cloth_eq_model:
            raise NotFoundException("Clothing equipment model not found")
        db.delete(cloth_eq_model)
        db.flush()
        return True

    def get_all_army_equipment_models(self, db: Session):
        return db.query(TypeArmyEquipmentModel).all()
    
    def get_army_equipment_model_by_id(self, db: Session, id: str):
        return (db.query(TypeArmyEquipmentModel)
                .filter(TypeArmyEquipmentModel.id==id)
                .first())

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
    
    def get_all_other_equipment_models(self, db: Session):
        return db.query(TypeOtherEquipmentModel).all()
    
    def get_other_equipment_model_by_id(self, db: Session, id: str):
        return (db.query(TypeOtherEquipmentModel)
                .filter(TypeOtherEquipmentModel.id==id)
                .first())
    
    def update_other_model(self, db: Session, id: str, body: TypeOtherEquipmentModelCreate):
        other_eq_model = self.get_other_equipment_model_by_id(db, id)
        if not other_eq_model:
            raise NotFoundException("Other equipment model not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(other_eq_model, key, value)
        setattr(other_eq_model, 'updated_at', datetime.now())
        db.add(other_eq_model)
        db.flush()
        return other_eq_model
    
    def delete_other_model(self, db: Session, id: str):
        other_eq_model = self.get_other_equipment_model_by_id(db, id)
        if not other_eq_model:
            raise NotFoundException("Other equipment model not found")
        db.delete(other_eq_model)
        db.flush()
        return True

    def get_clothing_equipment_model_by_id(self, db: Session, id: str):
        return (db.query(TypeClothingEquipmentModel)
                .filter(TypeClothingEquipmentModel.id==id)
                .first())

    def get_clothing_equipment_type_by_name(self, db: Session, name: str):
        return (db.query(TypeClothingEquipment)
                .filter(TypeClothingEquipment.name == name)
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
        setattr(equipment, 'updated_at', datetime.now())
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
        cloth_type = self.get_clothing_equipment_type_by_name(db, body.name)
        if cloth_type is None:
            cloth_eq_type = TypeClothingEquipment(name=body.name,
                                                  nameKZ=body.nameKZ)
            cloth_type = super().create(db, cloth_eq_type, TypeClothingEquipment)

        for model_id in body.model_ids:
            cloth_type_model = {
                'type_cloth_eq_models_id':model_id,
                'type_cloth_equipmets_id':cloth_type.id
            }
            super().create(db, cloth_type_model, ClothingEquipmentTypesModels)

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
    
    def update_type_clothing(self, db: Session, id: str, body: TypeClothingEquipmentUpdate):
        type_cloth = self.get_clothing_equipment_type_by_id(db, id)
        if not type_cloth:
            raise NotFoundException("TypeClothingEquipment not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(type_cloth, key, value)
        setattr(type_cloth, 'updated_at', datetime.now())
        db.add(type_cloth)
        db.flush()
        return type_cloth

    def delete_type_clothing(self, db: Session, id: str):
        type_cloth = self.get_clothing_equipment_type_by_id(db, id)
        if not type_cloth:
            raise NotFoundException("TypeClothingEquipment not found")
        db.delete(type_cloth)
        db.flush()
        return True
    
    def update_type_army(self, db: Session, id: str, body: TypeArmyEquipmentCreate):
        type_army = self.get_army_equipment_type_by_id(db, id)
        if not type_army:
            raise NotFoundException("TypeArmyEquipment not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(type_army, key, value)
        setattr(type_army, 'updated_at', datetime.now())
        db.add(type_army)
        db.flush()
        return type_army
    
    def delete_type_army(self, db: Session, id: str):
        type_army = self.get_army_equipment_type_by_id(db, id)
        if not type_army:
            raise NotFoundException("TypeArmyEquipment not found")
        db.delete(type_army)
        db.flush()
        return True
    
    def update_other_type(self, db: Session, id: str, body: TypeOtherEquipmentCreate):
        type_other = self.get_other_equipment_type_by_id(db, id)
        if not type_other:
            raise NotFoundException("TypeOtherEquipment not found")
        for key, value in body.dict(exclude_none=True).items():
            setattr(type_other, key, value)
        setattr(type_other, 'updated_at', datetime.now())
        db.add(type_other)
        db.flush()
        return type_other
    
    def delete_other_type(self, db: Session, id: str):
        type_other = self.get_other_equipment_type_by_id(db, id)
        if not type_other:
            raise NotFoundException("TypeOtherEquipment not found")
        db.delete(type_other)
        db.flush()
        return True

equipment_service = EquipmentService(Equipment)
