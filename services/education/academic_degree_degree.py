from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models.education import AcademicDegreeDegree
from schemas.education import AcademicDegreeDegreeCreate, AcademicDegreeDegreeUpdate

from services import ServiceBase


class AcademicDegreeDegreeService(ServiceBase[AcademicDegreeDegree, AcademicDegreeDegreeCreate, AcademicDegreeDegreeUpdate]):
    def get_by_id(self, db: Session, id: str):
        academic_degree_degree = super().get(db, id)
        if academic_degree_degree is None:
            raise NotFoundException(detail="AcademicDegreeDegree is not found!")
        return academic_degree_degree


academic_degree_degree_service = AcademicDegreeDegreeService(AcademicDegreeDegree)
