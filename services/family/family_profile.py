from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyProfile
from schemas import FamilyProfileCreate, FamilyProfileUpdate
from services import ServiceBase


class FamilyProfileService(ServiceBase[FamilyProfile, FamilyProfileCreate, FamilyProfileUpdate]):
    
    def get_by_id(self, db: Session, id: str) -> FamilyProfile:
        family_profile = db.query(FamilyProfile).filter(FamilyProfile.id == id).first()
        if not family_profile:
            raise NotFoundException("Family profile with id: {id} not found!")
        return family_profile
    
    def get_by_profile_id(self, db: Session, profile_id: str):
        family_profile = db.query(FamilyProfile).filter(FamilyProfile.profile_id == profile_id).first()
        if not family_profile:
            raise NotFoundException("Family profile with id: {profile_id} not found!")
        return family_profile


family_profile_service = FamilyProfileService(FamilyProfile)
