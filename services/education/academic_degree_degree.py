from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models.education import AcademicDegreeDegree
from schemas.education import AcademicDegreeDegreeCreate, AcademicDegreeDegreeUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class AcademicDegreeDegreeService(
        ServiceBase[AcademicDegreeDegree,
                    AcademicDegreeDegreeCreate,
                    AcademicDegreeDegreeUpdate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        academic_degree_degrees = db.query(AcademicDegreeDegree)

        if filter != '':
            academic_degree_degrees = add_filter_to_query(academic_degree_degrees,
                                                          filter,
                                                          AcademicDegreeDegree)

        academic_degree_degrees = (academic_degree_degrees
                       .order_by(func.to_char(AcademicDegreeDegree.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(AcademicDegreeDegree).count()

        return {'total': total, 'objects': academic_degree_degrees}

    def get_by_id(self, db: Session, id: str):
        academic_degree_degree = super().get(db, id)
        if academic_degree_degree is None:
            raise NotFoundException(
                detail="AcademicDegreeDegree is not found!")
        return academic_degree_degree


academic_degree_degree_service = AcademicDegreeDegreeService(
    AcademicDegreeDegree
)
