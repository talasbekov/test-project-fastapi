import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase

from models import HrDocumentTemplate
from schemas import HrDocumentTemplateCreate, HrDocumentTemplateUpdate
from exceptions import NotFoundException


class HrDocumentTemplateService(ServiceBase[HrDocumentTemplate, HrDocumentTemplateCreate, HrDocumentTemplateUpdate]):

    def get_by_id(self, db: Session, id: str):
        hr_document_template = db.query(HrDocumentTemplate).filter(HrDocumentTemplate.id == id).first()
        if hr_document_template is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with id: {id} is not found!')
        return hr_document_template


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
