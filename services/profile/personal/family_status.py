from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyStatus
from schemas import FamilyStatusCreate, FamilyStatusUpdate
from services.base import ServiceBase
from services.profile import profile_service

class FamilyStatusService(ServiceBase[FamilyStatus, FamilyStatusCreate, FamilyStatusUpdate]):

    def get_by_id(self, db: Session, id: str):
        family_status = super().get(db, id)
        if family_status is None:
            raise NotFoundException(detail=f"FamilyStatus with id: {id} is not found!")
        return family_status
    
    def get_by_user_id(self, db: Session, id: str):
        return profile_service.get_by_user_id(db, id).personal_profile


family_status_service = FamilyStatusService(FamilyStatus)
