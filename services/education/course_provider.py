from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import CourseProvider
from schemas.education import CourseProviderCreate, CourseProviderUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class CourseProviderService(
        ServiceBase[CourseProvider, CourseProviderCreate, CourseProviderUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        course_providers = db.query(CourseProvider)
        total = (db.query(CourseProvider))
        if filter != '':
            course_providers = add_filter_to_query(course_providers, filter, CourseProvider)
            total = add_filter_to_query(total, filter, CourseProvider)

        course_providers = (course_providers
                            .order_by(func.to_char(CourseProvider.name))
                            .offset(skip)
                            .limit(limit)
                            .all())

        total = (total
                 .count())

        return {'total': total, 'objects': course_providers}

    def get_by_id(self, db: Session, id: str):
        course_provider = super().get(db, id)
        if course_provider is None:
            raise NotFoundException(
                detail=f"CourseProvider with id: {id} is not found!")
        return course_provider


course_provider_service = CourseProviderService(CourseProvider)
