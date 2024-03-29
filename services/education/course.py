from typing import Union, Dict, Any, List
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Course
from schemas.education import CourseCreate, CourseUpdate
from services import ServiceBase
from fastapi.encoders import jsonable_encoder


class CourseService(ServiceBase[Course, CourseCreate, CourseUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Course]:
        return (db.query(Course)
                  .order_by(Course.name)
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        course = super().get(db, id)
        if course is None:
            raise NotFoundException(
                detail=f"Course with id: {id} is not found!")
        return course

    def create(self, db: Session,
               obj_in: Union[CourseCreate, Dict[str, Any]]) -> Course:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['start_date'] = datetime.strptime(
            obj_in_data['start_date'], '%Y-%m-%d')
        obj_in_data['end_date'] = datetime.strptime(
            obj_in_data['end_date'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj


course_service = CourseService(Course)
