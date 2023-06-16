from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PrivilegeEmergency
from schemas import PrivelegeEmergencyCreate, PrivelegeEmergencyUpdate
from .base import ServiceBase


class PrivelegeEmergencyService(
        ServiceBase[PrivilegeEmergency, PrivelegeEmergencyCreate, PrivelegeEmergencyUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"PrivilegeEmergency with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        privelege_emergency = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return privelege_emergency


privelege_emergency_service = PrivelegeEmergencyService(PrivilegeEmergency)
