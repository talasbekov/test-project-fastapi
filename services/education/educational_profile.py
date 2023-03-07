from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import EducationalProfile
from schemas.education import EducationalProfileCreate, EducationalProfileRead, EducationalProfileUpdate

from services import ServiceBase


class EducationalProfileService(ServiceBase[EducationalProfile, EducationalProfileCreate, EducationalProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        educational_profile = super().get(db, id)
        if educational_profile is None:
            raise NotFoundException(detail=f"EducationalProfile with id: {id} is not found!")
        return educational_profile


educational_profile_service = EducationalProfileService(EducationalProfile)
