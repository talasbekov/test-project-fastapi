import uuid

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import HrDocumentTemplate
from schemas import HrDocumentTemplateCreate, HrDocumentTemplateUpdate

from .base import ServiceBase


class HrDocumentTemplateService(ServiceBase[HrDocumentTemplate, HrDocumentTemplateCreate, HrDocumentTemplateUpdate]):

    def get_by_id(self, db: Session, id: str):
        hr_document_template = super().get(db, id)
        if hr_document_template is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with id: {id} is not found!')
        return hr_document_template


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
