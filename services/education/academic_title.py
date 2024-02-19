from datetime import datetime
from typing import Union, Dict, Any

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import NotFoundException
from models.education import AcademicTitle
from schemas.education import AcademicTitleCreate, AcademicTitleUpdate
from services import ServiceBase


class AcademicTitleService(
        ServiceBase[AcademicTitle, AcademicTitleCreate, AcademicTitleUpdate]):

    def create(self, db: Session,
               obj_in: Union[AcademicTitleCreate, Dict[str, Any]]) -> AcademicTitle:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(obj_in_data['assignment_date'],
                                                           '%Y-%m-%d')
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


academic_title_service = AcademicTitleService(AcademicTitle)
