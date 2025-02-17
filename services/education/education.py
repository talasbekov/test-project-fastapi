from typing import Dict, Any, Union

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from exceptions import NotFoundException
from models.education import Education, EducationalProfile
from schemas.education import EducationCreate, EducationUpdate
from services import ServiceBase
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException

class EducationService(
        ServiceBase[Education, EducationCreate, EducationUpdate]):

    def create(self, db: Session,
               obj_in: Union[EducationCreate, Dict[str, Any]]) -> Education:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['start_date'] = obj_in.start_date
        obj_in_data['end_date'] = obj_in.end_date
        obj_in_data['date_of_issue'] = obj_in.date_of_issue
        try:
            educational_profile_id = db.query(EducationalProfile).filter(EducationalProfile.profile_id == obj_in_data['profile_id']).one()
            obj_in_data['educational_profile_id'] = educational_profile_id.id 
            obj_in_data['profile_id'] = educational_profile_id.id
        except NoResultFound:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_educational_profiles.")

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str):
        education = super().get(db, id)
        if education is None:
            raise NotFoundException(
                detail=f"Education with id: {id} is not found!")
        return education

    def get_by_profile_id(self, db: Session, id: str):
        education = db.query(self.model).filter(
            self.model.profile_id == id).all()
        # if not education:
        #     raise NotFoundException(
        #         detail=f"Education with id: {id} is not found!")
        return education

    


education_service = EducationService(Education)
