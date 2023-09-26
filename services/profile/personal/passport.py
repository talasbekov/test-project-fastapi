from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Passport, PersonalProfile, Profile
from schemas import PassportCreate, PassportUpdate
from services.base import ServiceBase


class PassportService(ServiceBase[Passport, PassportCreate, PassportUpdate]):

    def get_by_id(self, db: Session, id: str):
        passport = super().get(db, id)
        if passport is None:
            raise NotFoundException(
                detail=f"Passport with id: {id} is not found!")
        return passport
    
    def get_by_user_id(self, db: Session, user_id: str):
        passport = (db.query(Passport)
                        .join(PersonalProfile)
                        .join(Profile)
                        .filter(Profile.user_id == user_id)
                        .first())
        if passport is None:
            raise NotFoundException(
                detail=f"Passport with user id: {id} is not found!")
        return passport


passport_service = PassportService(Passport)
