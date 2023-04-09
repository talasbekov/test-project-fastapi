from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Education
from schemas.education import EducationCreate, EducationUpdate
from services import ServiceBase


class EducationService(ServiceBase[Education, EducationCreate, EducationUpdate]):

    def get_by_id(self, db: Session, id: str):
        education = super().get(db, id)
        if education is None:
            raise NotFoundException(
                detail=f"Education with id: {id} is not found!")
        return education

    def get_by_profile_id(self, db: Session, id: str):
        education = db.query(self.model).filter(
            self.model.profile_id == id).first()
        if not education:
            raise NotFoundException(
                detail=f"Education with id: {id} is not found!")
        return education


education_service = EducationService(Education)
