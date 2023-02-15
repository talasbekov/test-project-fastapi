from datetime import datetime

from sqlalchemy import desc
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
    
    def create_info_for_step(self, db: Session, document_id: str, step_id: str, user_id: str, is_signed: bool):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            signed_by=user_id,
            comment="",
            is_signed=is_signed
        )

        return super().create(db, document_info)
    
    def create_next_info_for_step(self, db: Session,  document_id: str, step_id: str):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            signed_by=None,
            comment="",
            is_signed=None
        )

        return super().create(db, document_info)
    
    def get_not_signed_by_position(self, db: Session, position_id: str):

        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.is_signed == None,
            HrDocumentInfo.hr_document_step.has(position_id = position_id)
        ).all()

        return infos
    
    def get_last_signed_step_info(self, db: Session, id: str):

        info = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == id
        ).order_by(
            desc(HrDocumentInfo.created_at)
        ).first()

        if info is None:
            raise NotFoundException(detail=f'Нет истории подписания!')

        return info
    
    def get_last_unsigned_step_info(self, db: Session, id: str):

        info = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == id,
            HrDocumentInfo.is_signed == None
        ).first()

        if info is None:
            raise NotFoundException(detail=f'Все подписано!')

        return info

    def sign(self, db: Session, info: HrDocumentInfo, user_id: str, comment: str, is_signed: bool):

        info.signed_by = user_id
        info.comment = comment
        info.is_signed = is_signed
        info.updated_at = datetime.now()

        db.add(info)
        db.flush()

        return info
    
    def get_by_document_id(self, db: Session, id: str):

        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == id
        ).order_by(
            HrDocumentInfo.created_at.desc()
        ).all()

        return infos


hr_document_info_service = HrDocumentInfoService(HrDocumentInfo)
