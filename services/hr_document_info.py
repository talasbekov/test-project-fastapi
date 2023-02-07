from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import HrDocumentInfo
from schemas import HrDocumentInfoCreate, HrDocumentInfoUpdate, HrDocumentInfoRead

from exceptions import NotFoundException


class HrDocumentInfoService(ServiceBase[HrDocumentInfo, HrDocumentInfoCreate, HrDocumentInfoUpdate]):

    def get_by_id(self, db: Session, id: str):
        hr_document_info = super().get(db, id)
        if hr_document_info is None:
            raise NotFoundException(detail=f"Document Info with id: {id} is not found!")
        return hr_document_info

hr_document_info_service = HrDocumentInfoService(HrDocumentInfo)
