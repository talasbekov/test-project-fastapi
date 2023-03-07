from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Profile
from schemas import ProfileCreate, ProfileUpdate, ProfileRead

from services.base import ServiceBase


class ProfileService(ServiceBase[Profile, ProfileCreate, ProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        profile = super().get(db, id)
        if profile is None:
            raise NotFoundException(detail=f"Profile with id: {id} is not found!")
        return profile
    
    
    def get_by_user_id(self, db: Session, user_id: str):
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile is None:
            raise NotFoundException(detail=f"Profile with user_id: {user_id} is not found!")
        return profile
    

profile_service = ProfileService(Profile)
