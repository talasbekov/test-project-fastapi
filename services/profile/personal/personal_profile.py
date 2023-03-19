from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PersonalProfile
from schemas import (PersonalProfileCreate, PersonalProfileUpdate)
from services.base import ServiceBase


class PersonalProfileService(ServiceBase[PersonalProfile, PersonalProfileCreate, PersonalProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        personal_profile = super().get(db, id)
        if personal_profile is None:
            raise NotFoundException(detail=f"PersonalProfile with id: {id} is not found!")
        return personal_profile


personal_profile_service = PersonalProfileService(PersonalProfile)
