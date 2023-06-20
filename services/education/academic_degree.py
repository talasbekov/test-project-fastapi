from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models.education import AcademicDegree
from schemas.education import AcademicDegreeCreate, AcademicDegreeUpdate
from services import ServiceBase


class AcademicDegreeService(
        ServiceBase[AcademicDegree, AcademicDegreeCreate, AcademicDegreeUpdate]):
    def get_by_id(self, db: Session, id: str):
        academic_degree = super().get(db, id)
        if academic_degree is None:
            raise NotFoundException(detail="Academic Degree is not found!")
        return academic_degree


academic_degree_service = AcademicDegreeService(AcademicDegree)
