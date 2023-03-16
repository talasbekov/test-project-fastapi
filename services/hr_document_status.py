from typing import Optional

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import HrDocumentStatus
from schemas import HrDocumentStatusCreate, HrDocumentStatusUpdate

from .base import ServiceBase


class HrDocumentStatusService(ServiceBase[HrDocumentStatus, HrDocumentStatusCreate, HrDocumentStatusUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocumentStatus:
        status = super().get(db, id)
        if status is None:
            raise NotFoundException(detail=f"HrDocumentStatus with id: {id} is not found!")
        return status

    def get_by_name(self, db: Session, name_ru: str) -> Optional[HrDocumentStatus]:
        return db.query(self.model).filter(self.model.name_ru == name_ru).first()


hr_document_status_service = HrDocumentStatusService(HrDocumentStatus)