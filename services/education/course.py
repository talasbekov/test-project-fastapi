from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Course
from schemas.education import CourseCreate, CourseUpdate
from services import ServiceBase


class CourseService(ServiceBase[Course, CourseCreate, CourseUpdate]):

    def get_by_id(self, db: Session, id: str):
        course = super().get(db, id)
        if course is None:
            raise NotFoundException(
                detail=f"Course with id: {id} is not found!")
        return course


course_service = CourseService(Course)
