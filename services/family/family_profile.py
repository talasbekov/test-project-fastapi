from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyProfile, Profile
from schemas import FamilyProfileCreate, FamilyProfileUpdate
from services import ServiceBase


class FamilyProfileService(
        ServiceBase[FamilyProfile, FamilyProfileCreate, FamilyProfileUpdate]):
    def get_by_id(self, db: Session, id: str) -> FamilyProfile:
        family_profile = db.query(FamilyProfile).filter(
            FamilyProfile.id == id).first()
        if not family_profile:
            raise NotFoundException("Family profile with id: {id} not found!")
        return family_profile

    def get_by_profile_id(self, db: Session, profile_id: str):
        family_profile = db.query(FamilyProfile).filter(
            FamilyProfile.profile_id == profile_id).first()
        if not family_profile:
            raise NotFoundException(
                "Family profile with id: {profile_id} not found!")
        return family_profile

    def get_by_user_id(self, db: Session, user_id: str):
        profile = (
            db.query(self.model)
            .join(Profile, 
                  and_(Profile.id == self.model.profile_id, 
                       Profile.user_id == user_id))
            .first()
        )
        return profile


family_profile_service = FamilyProfileService(FamilyProfile)
