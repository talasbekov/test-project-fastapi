import uuid
from sqlalchemy.orm import Session
from exceptions.client import NotFoundException

from models import (ArchivePrivilegeEmergency)
from schemas import ArchivePrivelegeEmergencyCreate, ArchivePrivelegeEmergencyUpdate, ArchivePrivelegeEmergencyAutoCreate
from services import ServiceBase


class ArchivePrivelegeEmergencyService(ServiceBase[ArchivePrivilegeEmergency, ArchivePrivelegeEmergencyCreate, ArchivePrivelegeEmergencyUpdate]):

    def get_by_name(self, db: Session, name: str):
        role = db.query(ArchivePrivilegeEmergency).filter(
            ArchivePrivilegeEmergency.name == name
        ).first()

        if role:
            return role.id
        else:
            return None

    def get_by_user_id(self, db: Session, user_id: str):
        privelege_emergency = db.query(self.model).filter(self.model.user_id == user_id).first()
        return privelege_emergency
        
    def get_by_origin_id(self, db: Session, id: uuid.UUID):
        position = db.query(self.model).filter(
            ArchivePrivilegeEmergency.origin_id == id
        ).first()
        if position is None:
            raise NotFoundException(detail=f"Privelege emergency with id {id} not found!")
        return position

    def create_based_on_existing_position(self, db: Session,
                                          form: str,
                                          date_from: str,
                                          date_to: str,
                                          origin_id: uuid.UUID,
                                          user_id: uuid.UUID):
        return super().create(db, ArchivePrivelegeEmergencyAutoCreate(
            form=form,
            date_from=date_from,
            date_to=date_to,
            origin_id=origin_id,
            user_id=user_id
        ))

archive_privelege_emergency_service = ArchivePrivelegeEmergencyService(ArchivePrivilegeEmergency)  # type: ignore
