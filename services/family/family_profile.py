from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyProfile, Profile, Family, FamilyRelation
from schemas import (FamilyProfileCreate, FamilyProfileUpdate,
                     FamilyProfileRead)
from services import ServiceBase, profile_service


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
        profile_id = profile_service.get_by_user_id(db, str(user_id))
        profile = (
            db.query(self.model)
            .filter(self.model.profile_id == profile_id.id)
            .first()
            # .join(Profile,
            #       and_(Profile.id == profile_id.id,
            #            Profile.user_id == user_id))
            # .first()
        )
        # print(profile.id)
        # print("Profile_id ", profile.profile_id)
        family = (
            db.query(Family)
            .join(FamilyRelation)
            .filter(Family.profile_id==profile.id)
            .order_by(FamilyRelation.family_order,
                      Family.birthday)
            .all()
        )
        return FamilyProfileRead(id=profile.id,
                                 profile_id=profile.profile_id,
                                 family=family)


family_profile_service = FamilyProfileService(FamilyProfile)
