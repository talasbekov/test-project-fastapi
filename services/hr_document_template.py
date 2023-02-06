from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from .hr_document import hr_document_service

from models import HrDocumentTemplate
from schemas import HrDocumentTemplateCreate, HrDocumentTemplateUpdate


class HrDocumentTemplateService(ServiceBase[HrDocumentTemplate, HrDocumentTemplateCreate, HrDocumentTemplateUpdate]):
    pass


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
