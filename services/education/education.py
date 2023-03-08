from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Education
from schemas.education import EducationCreate, EducationRead, EducationUpdate

from services import ServiceBase


class EducationService(ServiceBase[Education, EducationCreate, EducationUpdate]):

    def get_by_id(self, db: Session, id: str):
        education = super().get(db, id)
        if education is None:
            raise NotFoundException(detail=f"Education with id: {id} is not found!")
        return education


education_service = EducationService(Education)
