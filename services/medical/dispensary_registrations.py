from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from exceptions import client
from models.medical import DispensaryRegistration, MedicalProfile
from schemas.medical import DispensaryRegistrationUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from utils.date import parse_datetime


class DispensaryRegistrationService(
        ServiceBase[DispensaryRegistration,
                    DispensaryRegistrationUpdate,
                    DispensaryRegistrationUpdate]):
    def get_by_id(self, db: Session, id: str):
        dispensary_registration = super().get(db, id)
        if dispensary_registration is None:
            raise client.NotFoundException(
                detail="Dispensary registration is not found!")
        return dispensary_registration

    def create(self, db: Session,
            obj_in: Union[DispensaryRegistrationUpdate, Dict[str, Any]]) -> DispensaryRegistration:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data['start_date'] is not None:
            obj_in_data['start_date'] = parse_datetime(obj_in_data['start_date'])
        if obj_in_data['end_date'] is not None:
            obj_in_data['end_date'] = parse_datetime(obj_in_data['end_date'])
        try:
            medical_profile = db.query(MedicalProfile).filter(MedicalProfile.profile_id == obj_in_data['profile_id']).one()
            obj_in_data['medical_profile_id'] = medical_profile.id  
            obj_in_data['profile_id'] = medical_profile.id  
        except NoResultFound:
            raise ValueError("Profile ID not found in hr_erp_medical_profiles.")
        
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_profile_id(self, db: Session, profile_id: str):
        disp = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not disp:
        #     raise NotFoundException(
        #         "Course profile with id: {profile_id} not found!")
        return disp

dispensary_registration_service = DispensaryRegistrationService(
    DispensaryRegistration)
