from typing import List
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Family
from schemas import FamilyCreate, FamilyUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class FamilyService(ServiceBase[Family, FamilyCreate, FamilyUpdate]):
    def get_multi(self, db: Session, skip: int = 0,
                  limit: int = 100) -> List[Family]:
        families = db.query(Family).join(Family.violation).join(
            Family.abroad_travel).offset(skip).limit(limit).all()

        return families

    def get_by_id(self, db: Session, id: str) -> Family:
        family = db.query(Family).outerjoin(
            Family.violation).outerjoin(
            Family.abroad_travel).filter(
            Family.id == id).first()
        if not family:
            raise NotFoundException(f"Family with id: {id} not found!")
        return family

    def get_by_relation_id(self, db: Session, relation_id: str):
        family = db.query(Family).filter(
            Family.relation_id == relation_id).first()
        return family

    def create(self, db: Session,
               obj_in: Union[FamilyCreate, Dict[str, Any]]) -> Family:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['birthday'] = datetime.strptime(
            obj_in_data['birthday'], '%Y-%m-%dT%H:%M:%S.%f%z')
        if obj_in_data['death_day'] is not None:
            obj_in_data['death_day'] = datetime.strptime(
                obj_in_data['death_day'], '%Y-%m-%dT%H:%M:%S.%f%z')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj


family_service = FamilyService(Family)
