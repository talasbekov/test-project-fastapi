from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SpecialCheck
from schemas import SpecialCheckCreate, SpecialCheckUpdate
from services import profile_service
from services.base import ServiceBase


class SpecialCheckService(
        ServiceBase[SpecialCheck, SpecialCheckCreate, SpecialCheckUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank

    def create(self, db: Session, obj_in: SpecialCheckCreate):
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_of_issue'] = datetime.strptime(obj_in_data['date_of_issue'],
                                                '%Y-%m-%dT%H:%M:%S.%f%z')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(self, db: Session, db_obj: SpecialCheck,
               obj_in: SpecialCheckUpdate):
        return super().update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str):
        return super().delete(db, id)

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


special_check_service = SpecialCheckService(SpecialCheck)
