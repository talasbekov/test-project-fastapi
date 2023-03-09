from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import AcademicTitle
from schemas.education import AcademicTitleCreate, AcademicTitleUpdate
from services import ServiceBase


class AcademicTitleService(ServiceBase[AcademicTitle, AcademicTitleCreate, AcademicTitleUpdate]):

    def get_by_id(self, db: Session, id: str):
        academic_title = super().get(db, id)
        if academic_title is None:
            raise NotFoundException(detail=f"AcademicTitle with id: {id} is not found!")
        return academic_title


academic_title_service = AcademicTitleService(AcademicTitle)
