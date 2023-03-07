from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import AdditionalProfile
from services.base import ServiceBase
from schemas import AdditionalProfileCreate, AdditionalProfileUpdate

class AdditionalProfileService(ServiceBase[AdditionalProfile, AdditionalProfileCreate, AdditionalProfileUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Violation with id: {id} is not found!")
        return rank
    
    def create(self, db: Session, obj_in: AdditionalProfileCreate):
        return super().create(db, obj_in)
    
    def update(self, db: Session, db_obj: AdditionalProfile, obj_in: AdditionalProfileUpdate):
        return super().update(db, db_obj, obj_in)
    
    def delete(self, db: Session, id: str):
        return super().delete(db, id)


additional_profile_service = AdditionalProfileService(AdditionalProfile)
