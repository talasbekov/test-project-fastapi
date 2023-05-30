from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PrivilegeEmergency, ArchivePrivilegeEmergency, PrivelegeEnum
from schemas import PrivelegeEmergencyCreate, PrivelegeEmergencyRead, PrivelegeEmergencyUpdate
from .base import ServiceBase


class PrivelegeEmergencyService(ServiceBase[PrivilegeEmergency, PrivelegeEmergencyCreate, PrivelegeEmergencyUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"PrivilegeEmergency with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        privelege_emergency = db.query(self.model).filter(self.model.user_id == user_id).first()
        return privelege_emergency
    
    def create_from_archive(self, db: Session, archive_privelege_emergency: ArchivePrivilegeEmergency):
        res = super().create(
            db, PrivelegeEmergencyCreate(
                form=archive_privelege_emergency.form.name,
                date_from=archive_privelege_emergency.date_from,
                date_to=archive_privelege_emergency.date_to,
                user_id=archive_privelege_emergency.user_id
                )
            )
        return res

    def update_from_archive(self, db: Session, archive_privelege_emergency: ArchivePrivilegeEmergency):
        staff_unit = self.get_by_id(db, archive_privelege_emergency.origin_id)
        res = super().update(
            db,
            db_obj=staff_unit,
            obj_in=PrivelegeEmergencyUpdate(
                form=archive_privelege_emergency.form.name,
                date_from=archive_privelege_emergency.date_from,
                date_to=archive_privelege_emergency.date_to,
                user_id=archive_privelege_emergency.user_id
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session, archive_privelege_emergency: ArchivePrivilegeEmergency):
        if archive_privelege_emergency.origin_id is None:
            return self.create_from_archive(db, archive_privelege_emergency)
        return self.update_from_archive(db, archive_privelege_emergency)

privelege_emergency_service = PrivelegeEmergencyService(PrivilegeEmergency)
