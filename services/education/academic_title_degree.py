from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import AcademicTitleDegree
from schemas.education import AcademicTitleDegreeCreate, AcademicTitleDegreeUpdate
from services import ServiceBase
from utils import add_filter_to_query


class AcademicTitleDegreeService(
        ServiceBase[AcademicTitleDegree,
                    AcademicTitleDegreeCreate,
                    AcademicTitleDegreeUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        academic_title_degrees = db.query(AcademicTitleDegree)

        if filter != '':
            academic_title_degrees = add_filter_to_query(academic_title_degrees,
                                                         filter,
                                                         AcademicTitleDegree)

        academic_title_degrees = (academic_title_degrees
                     .order_by(func.to_char(AcademicTitleDegree.name))
                     .offset(skip)
                     .limit(limit)
                     .all())

        total = db.query(AcademicTitleDegree).count()

        return {'total': total, 'objects': academic_title_degrees}

    def get_by_id(self, db: Session, id: str):
        academic_title_degree = super().get(db, id)
        if academic_title_degree is None:
            raise NotFoundException(
                detail=f"AcademicTitleDegree with id: {id} is not found!")
        return academic_title_degree


academic_title_degree_service = AcademicTitleDegreeService(AcademicTitleDegree)
