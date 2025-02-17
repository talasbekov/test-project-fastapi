from datetime import datetime
from typing import Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions.client import NotFoundException
from models.education import AcademicDegree, EducationalProfile
from schemas.education import AcademicDegreeCreate, AcademicDegreeUpdate
from services import ServiceBase
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException

class AcademicDegreeService(
        ServiceBase[AcademicDegree, AcademicDegreeCreate, AcademicDegreeUpdate]):

    def create(self, db: Session,
               obj_in: Union[AcademicDegreeCreate, Dict[str, Any]]) -> AcademicDegree:
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

    def get_by_profile_id(self, db: Session, profile_id: str):
        academic_degree = db.query(self.model).filter(
            self.model.profile_id == profile_id).all()
        # if not academic_degree:
        #     raise NotFoundException(
        #         "AcademicProfile profile with id: {profile_id} not found!")
        return academic_degree

    def get_by_id(self, db: Session, id: str):
        academic_degree = super().get(db, id)
        if academic_degree is None:
            raise NotFoundException(detail="Academic Degree is not found!")
        return academic_degree


academic_degree_service = AcademicDegreeService(AcademicDegree)
