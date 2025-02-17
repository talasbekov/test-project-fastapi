from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Passport, PersonalProfile, Profile
from schemas import PassportCreate, PassportUpdate
from services.base import ServiceBase


class PassportService(ServiceBase[Passport, PassportCreate, PassportUpdate]):

    def get_by_id(self, db: Session, id: str):
        passport = super().get(db, id)
        if passport is None:
            raise NotFoundException(
                detail=f"Passport with id: {id} is not found!")
        return passport

    def create(self, db: Session,
               obj_in: Union[PassportCreate, Dict[str, Any]]) -> Passport:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_to'] = datetime.strptime(
            obj_in_data['date_to'], '%Y-%m-%d')
        obj_in_data['date_of_issue'] = datetime.strptime(
            obj_in_data['date_of_issue'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_user_id(self, db: Session, user_id: str):
        passport = (db.query(Passport)
                    .join(PersonalProfile)
                    .join(Profile)
                    .filter(Profile.user_id == user_id)
                    .first())

        return passport

    def get_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        passport = (db.query(Passport)
                    .join(PersonalProfile)
                    .join(Profile)
                    .filter(Profile.user_id == user_id)
                    .filter(Passport.date_of_issue <= date_till)
                    .filter(Passport.date_to <= date_till)
                    .first())

        return passport


passport_service = PassportService(Passport)
