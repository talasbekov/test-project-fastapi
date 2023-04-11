from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PersonalReserve
from schemas import PersonnalReserveCreate, PersonnalReserveRead, PersonnalReserveUpdate
from .base import ServiceBase


class PersonnalReserveService(ServiceBase[PersonalReserve, PersonnalReserveCreate, PersonnalReserveUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        personnal_reserve = db.query(self.model).filter(self.model.user_id == user_id).first()
        return personnal_reserve

personnal_reserve_service = PersonnalReserveService(PersonalReserve)
