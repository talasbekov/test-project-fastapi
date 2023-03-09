from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PersonalProfile, Profile
from schemas import (PersonalProfileCreate, PersonalProfileRead,
                     PersonalProfileUpdate)
from services.base import ServiceBase


class PersonalProfileService(ServiceBase[PersonalProfile, PersonalProfileCreate, PersonalProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        personal_profile = super().get(db, id)
        if personal_profile is None:
            raise NotFoundException(detail=f"PersonalProfile with id: {id} is not found!")
        return personal_profile
    
    def get_by_user_id(self, db: Session, user_id: str) -> PersonalProfile:
        res = db.query(self.model).join(Profile).filter(Profile.user_id == user_id).first()
        if res is None:
            raise NotFoundException(detail=f'PersonalProfile for user_id: {user_id} is not found!')
        return res


personal_profile_service = PersonalProfileService(PersonalProfile)
