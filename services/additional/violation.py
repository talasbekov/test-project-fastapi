from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Violation
from schemas import ViolationCreate, ViolationUpdate
from services import profile_service
from services.base import ServiceBase
from utils.date import parse_datetime


class ViolationService(
        ServiceBase[Violation, ViolationCreate, ViolationUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank

    def create(self, db: Session,
               obj_in: Union[ViolationCreate, Dict[str, Any]]) -> Violation:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date'] = parse_datetime(
            obj_in_data['date'])
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def create_family_violation(self, db: Session,
               obj_in: Union[ViolationCreate, Dict[str, Any]]) -> Violation:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date'] = parse_datetime(
            obj_in_data['date'])
        obj_in_data['profile_id'] = None
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        profile = profile_service.get_by_user_id(db, user_id)
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with user_id: {user_id} is not found!")

        polygraph_checks = db.query(self.model).filter(
            self.model.profile_id == profile.additional_profile.id
        ).offset(skip).limit(limit).all()

        return polygraph_checks


violation_service = ViolationService(Violation)
