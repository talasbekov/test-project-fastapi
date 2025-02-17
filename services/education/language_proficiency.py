from sqlalchemy.orm import Session
from typing import Union, Dict, Any, List
from exceptions import NotFoundException
from models.education import LanguageProficiency, EducationalProfile
from schemas.education import LanguageProficiencyCreate, LanguageProficiencyUpdate
from services import ServiceBase
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException



class LanguageProficiencyService(
        ServiceBase[LanguageProficiency,
                    LanguageProficiencyCreate,
                    LanguageProficiencyUpdate]):

    def get_by_id(self, db: Session, id: str):
        language_proficiency = super().get(db, id)
        if language_proficiency is None:
            raise NotFoundException(
                detail=f"LanguageProficiency with id: {id} is not found!")
        return language_proficiency
    
    def create(self, db: Session,
               obj_in: Union[LanguageProficiencyCreate, Dict[str, Any]]) -> LanguageProficiency:
        obj_in_data = jsonable_encoder(obj_in)
        try:
            educational_profile_id = db.query(EducationalProfile).filter(EducationalProfile.profile_id == obj_in_data['profile_id']).one()
            obj_in_data['educational_profile_id'] = educational_profile_id.id 
            obj_in_data['profile_id'] = educational_profile_id.id 
        except NoResultFound:
            raise HTTPException(status_code=400, detail="Profile ID not found in hr_erp_educational_profiles.")
        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_profile_id(self, db: Session, profile_id: str):
        language_proficiency = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not language_proficiency:
        #     raise NotFoundException(
        #         "Course profile with id: {profile_id} not found!")
        return language_proficiency



language_proficiency_service = LanguageProficiencyService(LanguageProficiency)
