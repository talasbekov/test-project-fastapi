from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Passport
from schemas import PassportCreate, PassportUpdate
from services.base import ServiceBase


class PassportService(ServiceBase[Passport, PassportCreate, PassportUpdate]):

    def get_by_id(self, db: Session, id: str):
        passport = super().get(db, id)
        if passport is None:
            raise NotFoundException(detail=f"Passport with id: {id} is not found!")
        return passport


passport_service = PassportService(Passport)
