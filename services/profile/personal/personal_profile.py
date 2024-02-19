import uuid
import random

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (
    PersonalProfile,
    DrivingLicense,
    IdentificationCard,
    Passport,
    TaxDeclaration,
    Profile
)
from schemas import PersonalProfileCreate, PersonalProfileUpdate
from services.base import ServiceBase


class PersonalProfileService(
        ServiceBase[PersonalProfile, PersonalProfileCreate, PersonalProfileUpdate]):
    def get_by_id(self, db: Session, id: str):
        personal_profile = super().get(db, id)
        if personal_profile is None:
            raise NotFoundException(
                detail=f"PersonalProfile with id: {id} is not found!")
        return personal_profile

    def get_rand(self, db: Session, id: str):
        personal_documents = [
            DrivingLicense,
            IdentificationCard,
            Passport,
            TaxDeclaration]
        random_model = random.choice(personal_documents)
        rand_document = db.query(random_model).filter(
            random_model.profile_id == id).first()

        if rand_document is None:
            raise NotFoundException(
                detail=f"Personal document {rand_document} with id: {id} is not found!")

        return rand_document

    def get_by_user_id(self, db: Session, user_id: str):
        personal_profile = (
            db.query(PersonalProfile)
            .join(Profile,
                  and_(PersonalProfile.profile_id == Profile.id,
                       Profile.user_id == user_id))
            .first()
        )
        if personal_profile is None:
            raise NotFoundException(
                detail=f"PersonalProfile with user_id: {user_id} is not found!")
        return personal_profile


personal_profile_service = PersonalProfileService(PersonalProfile)
