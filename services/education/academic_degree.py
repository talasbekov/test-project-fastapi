from datetime import datetime
from typing import Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions.client import NotFoundException
from models.education import AcademicDegree
from schemas.education import AcademicDegreeCreate, AcademicDegreeUpdate
from services import ServiceBase


class AcademicDegreeService(
        ServiceBase[AcademicDegree, AcademicDegreeCreate, AcademicDegreeUpdate]):

    def create(self, db: Session,
               obj_in: Union[AcademicDegreeCreate, Dict[str, Any]]) -> AcademicDegree:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(obj_in_data['assignment_date'],
                                                           '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str):
        academic_degree = super().get(db, id)
        if academic_degree is None:
            raise NotFoundException(detail="Academic Degree is not found!")
        return academic_degree


academic_degree_service = AcademicDegreeService(AcademicDegree)
