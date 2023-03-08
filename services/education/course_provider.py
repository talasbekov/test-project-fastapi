from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import CourseProvider
from schemas.education import CourseProviderCreate, CourseProviderRead, CourseProviderUpdate

from services import ServiceBase


class CourseProviderService(ServiceBase[CourseProvider, CourseProviderCreate, CourseProviderUpdate]):

    def get_by_id(self, db: Session, id: str):
        course_provider = super().get(db, id)
        if course_provider is None:
            raise NotFoundException(detail=f"CourseProvider with id: {id} is not found!")
        return course_provider


course_provider_service = CourseProviderService(CourseProvider)
