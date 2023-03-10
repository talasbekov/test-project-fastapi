from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import AcademicTitleDegree
from schemas.education import AcademicTitleDegreeCreate, AcademicTitleDegreeUpdate
from services import ServiceBase


class AcademicTitleDegreeService(ServiceBase[AcademicTitleDegree, AcademicTitleDegreeCreate, AcademicTitleDegreeUpdate]):

    def get_by_id(self, db: Session, id: str):
        academic_title_degree = super().get(db, id)
        if academic_title_degree is None:
            raise NotFoundException(detail=f"AcademicTitleDegree with id: {id} is not found!")
        return academic_title_degree


academic_title_degree_service = AcademicTitleDegreeService(AcademicTitleDegree)
