from sqlalchemy.orm import Session

from exceptions import client
from models.medical import UserLiberation, MedicalProfile
from schemas.medical import UserLiberationCreate, UserLiberationUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException
from datetime import datetime
from utils.date import parse_datetime


class UserLiberationService(
        ServiceBase[UserLiberation, UserLiberationCreate, UserLiberationUpdate]):
    def get_by_id(self, db: Session, id: str):
        user_liberations = super().get(db, id)
        if user_liberations is None:
            raise client.NotFoundException(
                detail="User liberation is not found!")
        return user_liberations

    def create(self, db: Session,
            obj_in: Union[UserLiberationCreate, Dict[str, Any]]) -> UserLiberation:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['start_date'] = parse_datetime(obj_in_data['start_date'])
        obj_in_data['end_date'] = parse_datetime(obj_in_data['end_date'])

        try:
            medical_profile = db.query(MedicalProfile).filter(MedicalProfile.profile_id == obj_in_data['profile_id']).one()
            obj_in_data['medical_profile_id'] = medical_profile.id 
            obj_in_data['profile_id'] = medical_profile.id
        except NoResultFound:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_medical_profiles.")

        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_profile_id(self, db: Session, profile_id: str):
        user_lib = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not user_lib:
        #     raise NotFoundException(
        #         "Course profile with id: {profile_id} not found!")
        return user_lib

user_liberations_service = UserLiberationService(UserLiberation)
