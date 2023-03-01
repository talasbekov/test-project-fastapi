from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Jurisdiction
from schemas import JurisdictionCreate, JurisdictionUpdate
from exceptions.client import NotFoundException


class JurisdictionService(ServiceBase[Jurisdiction, JurisdictionCreate, JurisdictionUpdate]):

    def get_by_id(self, db: Session, id: str):
        jurisdiction = super().get(db, id)
        if jurisdiction is None:
            raise NotFoundException(detail=f"Jurisdiction with id: {id} is not found!")
        return jurisdiction


jurisdiction_service = JurisdictionService(Jurisdiction)
