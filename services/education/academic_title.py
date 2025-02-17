from datetime import datetime
from typing import Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import NotFoundException
from models.education import AcademicTitle, EducationalProfile
from schemas.education import AcademicTitleCreate, AcademicTitleUpdate
from services import ServiceBase
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException


class AcademicTitleService(
        ServiceBase[AcademicTitle, AcademicTitleCreate, AcademicTitleUpdate]):

    def create(self, db: Session,
               obj_in: Union[AcademicTitleCreate, Dict[str, Any]]) -> AcademicTitle:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(obj_in_data['assignment_date'],
                                                           '%Y-%m-%d')
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
        academic_title = super().get(db, id)
        if academic_title is None:
            raise NotFoundException(
                detail=f"AcademicTitle with id: {id} is not found!")
        return academic_title

    def get_by_profile_id(self, db: Session, profile_id: str):
        academic_title = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not academic_title:
        #     return None
        return academic_title


academic_title_service = AcademicTitleService(AcademicTitle)
