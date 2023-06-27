from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import EducationalProfile
from schemas.education import EducationalProfileCreate, EducationalProfileUpdate
from services import ServiceBase


class EducationalProfileService(
        ServiceBase[EducationalProfile,
                    EducationalProfileCreate,
                    EducationalProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        educational_profile = super().get(db, id)
        if educational_profile is None:
            raise NotFoundException(
                detail=f"EducationalProfile with id: {id} is not found!")
        return educational_profile

    def get_by_profile_id(self, db: Session, profile_id: str):
        profile = db.query(
            self.model).filter(
            self.model.profile_id == profile_id)
        if profile is None:
            raise NotFoundException(
                detail=('EducationalProfile with profile_id:'
                        f" {profile_id} is not found!"))
        return profile


educational_profile_service = EducationalProfileService(EducationalProfile)
