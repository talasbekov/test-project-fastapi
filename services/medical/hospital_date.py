from sqlalchemy.orm import Session

from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from exceptions import client
from models.medical import HospitalData, MedicalProfile
from schemas.medical import HospitalDataCreate, HospitalDataUpdate
from services import ServiceBase
from utils.date import parse_datetime
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException

class HospitalDataService(
        ServiceBase[HospitalData, HospitalDataCreate, HospitalDataUpdate]):
    
    def create(self, db: Session,
               obj_in: Union[HospitalDataCreate, Dict[str, Any]]) -> HospitalData:
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
    
    
    def get_by_id(self, db: Session, id: str):
        hospital_data = super().get(db, id)
        if hospital_data is None:
            raise client.NotFoundException(
                detail="Hospital data is not found!")
        return hospital_data

    def get_by_profile_id(self, db: Session, profile_id: str):
        hosp_data = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not hosp_data:
        #     raise NotFoundException(
        #         "Course profile with id: {profile_id} not found!")
        return hosp_data


hospital_data_service = HospitalDataService(HospitalData)
