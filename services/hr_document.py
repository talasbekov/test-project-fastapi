from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase

from models import HrDocument
from schemas import HrDocumentCreate, HrDocumentUpdate
from exceptions import NotFoundException


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):
    def get_by_id(self, db: Session, id: str):
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")


hr_document_service = HrDocumentService(HrDocument)
