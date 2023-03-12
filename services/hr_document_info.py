import uuid
from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import HrDocument, HrDocumentInfo, HrDocumentStep, DocumentStaffFunction
from schemas import (HrDocumentInfoCreate, HrDocumentInfoRead,
                     HrDocumentInfoUpdate)
from services import (hr_document_step_service, staff_division_service,
                      user_service, staff_unit_service, document_staff_function_service)

from .base import ServiceBase


class HrDocumentInfoService(ServiceBase[HrDocumentInfo, HrDocumentInfoCreate, HrDocumentInfoUpdate]):

    def get_by_id(self, db: Session, id: str):

        hr_document_info = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.id == id
        ).first()
        print(hr_document_info)

        if hr_document_info is None:
            raise NotFoundException(detail=f"Document Info with id: {id} is not found!")

        return hr_document_info

    def create_info_for_step(self, db: Session, document_id: str, step_id: str, user_id: str, is_signed: bool,
                             comment: str, signed_at: datetime):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            assigned_to_id=user_id,
            signed_by=None,
            comment="",
            is_signed=is_signed,
            signed_at=signed_at
        )

        return super().create(db, document_info)

    def create_next_info_for_step(self, db: Session, document_id: str, step_id: str):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            signed_by=None,
            comment="",
            is_signed=None
        )

        return super().create(db, document_info)

    def get_not_signed_by_position(self, db: Session, staff_unit_id: str, skip: int, limit: int):

        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.is_signed == None,
            HrDocumentInfo.hr_document_step.has(staff_unit_id=staff_unit_id)
        ).offset(skip).limit(limit).all()

        return infos
    
    def get_by_document_id_and_step_id(self, db: Session, document_id: str, step_id: str) -> HrDocumentInfo:

        info = db.query(self.model).filter(
            self.model.hr_document_id == document_id,
            self.model.hr_document_step_id == step_id,
            self.model.is_signed == None
        ).first()

        if info is None:
            raise NotFoundException(detail=f'Нет истории подписания!')
        
        return info

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
        info.signed_at = datetime.now()

        db.add(info)
        db.flush()

        return info

    def get_signed_by_user_id(self, db: Session, user_id: uuid.UUID, skip: int, limit: int):

        infos = db.query(self.model).filter(
            self.model.signed_by == user_id
        ).offset(skip).limit(limit).all()

        return infos

    def get_by_document_id(self, db: Session, id: str):

        infos = db.query(self.model)\
            .join(HrDocumentStep)\
            .join(DocumentStaffFunction)\
            .filter(self.model.hr_document_id == id)\
            .order_by(self.model.created_at.asc(), DocumentStaffFunction.priority.asc())\
            .all()

        return infos
    
    def get_initialized_by_user_id(self, db: Session, user_id: str, skip: int, limit: int) -> List[HrDocumentInfo]:

        infos = db.query(HrDocumentInfo).join(HrDocumentStep).join(DocumentStaffFunction).filter(
            HrDocumentInfo.assigned_to_id == user_id,
            DocumentStaffFunction.priority == 1
        ).order_by(
            HrDocumentInfo.created_at.desc()
        ).offset(skip).limit(limit).all()

        return infos

    def _get_history_by_document_id(self, db: Session, document_id: str) -> List[HrDocumentInfo]:
        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == document_id
        ).order_by(
            HrDocumentInfo.signed_at.asc() 
        ).all()

        return infos


hr_document_info_service = HrDocumentInfoService(HrDocumentInfo)
