from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Profile
from schemas.education import ProfileCreate, ProfileRead, ProfileUpdate

from services import ServiceBase


class ProfileService(ServiceBase[Profile, ProfileCreate, ProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        profile = super().get(db, id)
        if profile is None:
            raise NotFoundException(detail=f"Profile with id: {id} is not found!")
        return profile


profile_service = ProfileService(Profile)
