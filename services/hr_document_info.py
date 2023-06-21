import uuid
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from exceptions import NotFoundException

from models import (
    HrDocumentInfo,
    HrDocumentStep,
    DocumentStaffFunction,
    User,
)
from schemas import (HrDocumentInfoCreate, HrDocumentInfoUpdate)
from .base import ServiceBase


class HrDocumentInfoService(
        ServiceBase[HrDocumentInfo, HrDocumentInfoCreate, HrDocumentInfoUpdate]):

    def get_by_id(self, db: Session, id: str):

        hr_document_info = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.id == id
        ).first()

        if hr_document_info is None:
            raise NotFoundException(
                detail=f"Document Info with id: {id} is not found!")

        return hr_document_info

    def create_info_for_step(self,
                             db: Session,
                             document_id: str,
                             step_id: str,
                             user_id: str,
                             is_signed: bool,
                             comment: str,
                             signed_at: datetime,
                             order: int = 1):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            assigned_to_id=user_id,
            signed_by=None,
            comment="",
            is_signed=is_signed,
            signed_at=signed_at,
            order=order,
        )

        return super().create(db, document_info)

    def get_by_document_id_and_step_id(
            self, db: Session, document_id: str, step_id: str) -> HrDocumentInfo:

        info = db.query(self.model).filter(
            self.model.hr_document_id == document_id,
            self.model.hr_document_step_id == step_id,
            self.model.is_signed == None
        ).order_by(self.model.order).first()

        if info is None:
            raise NotFoundException(detail='Нет истории подписания для!')

        return info

    def find_by_document_id_and_step_id(
            self, db: Session, document_id: str, step_id: str) -> HrDocumentInfo:
        return db.query(self.model).filter(
            self.model.hr_document_id == document_id,
            self.model.hr_document_step_id == step_id,
            self.model.is_signed == None
        ).order_by(self.model.order).first()

    def find_by_document_id_and_step_id_signed(
            self, db: Session, document_id: str, step_id: str) -> HrDocumentInfo:
        return db.query(self.model).filter(
            self.model.hr_document_id == document_id,
            self.model.hr_document_step_id == step_id,
        ).order_by(self.model.order).first()

    def sign(self, db: Session, info: HrDocumentInfo,
             user: User, comment: str, is_signed: bool):

        info.signed_by = user
        info.comment = comment
        info.is_signed = is_signed
        info.updated_at = datetime.now()
        info.signed_at = datetime.now()

        db.add(info)
        db.flush()

        return info

    def get_signed_by_user_id(
            self, db: Session, user_id: uuid.UUID, skip: int, limit: int):

        infos = db.query(self.model).filter(
            self.model.signed_by == user_id
        ).offset(skip).limit(limit).all()

        return infos

    def get_by_document_id(self, db: Session, id: str):

        infos = db.query(self.model)\
            .join(HrDocumentStep)\
            .join(DocumentStaffFunction)\
            .filter(
                self.model.hr_document_id == id,
                self.model.signed_by_id is not None
        )\
            .order_by(self.model.created_at.asc(),
                      DocumentStaffFunction.priority.asc(),
                      self.model.order)\
            .all()

        additional_infos = db.query(self.model)\
            .join(HrDocumentStep)\
            .join(DocumentStaffFunction)\
            .filter(
                self.model.hr_document_id == id,
                self.model.signed_by_id is None
        )\
            .order_by(DocumentStaffFunction.priority.asc(), self.model.order)\
            .all()

        infos.extend(additional_infos)

        return infos

    def get_initialized_by_user_id(
            self,
            db: Session,
            user_id: str,
            skip: int,
            limit: int) -> List[HrDocumentInfo]:

        infos = (
            db
            .query(HrDocumentInfo)
            .join(HrDocumentStep)
            .join(DocumentStaffFunction)
            .filter(
                HrDocumentInfo.assigned_to_id == user_id,
                DocumentStaffFunction.priority == 1
            ).order_by(
                HrDocumentInfo.created_at.desc()
            ).offset(skip)
            .limit(limit).all()
        )

        return infos

    def _get_history_by_document_id(
            self, db: Session, document_id: str) -> List[HrDocumentInfo]:
        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == document_id
        ).order_by(
            HrDocumentInfo.signed_at.asc()
        ).all()

        return infos

    def get_signed_by_document_id_and_step_id(
            self,
            db: Session,
            document_id: str,
            step_id: str,
            order: int = 1) -> HrDocumentInfo:

        info = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == document_id,
            HrDocumentInfo.hr_document_step_id == step_id,
            HrDocumentInfo.is_signed is not None,
            HrDocumentInfo.order == order,
        ).order_by(HrDocumentInfo.signed_at.desc()).first()

        if info is None:
            raise NotFoundException(detail='Нет истории подписания!')

        return info


hr_document_info_service = HrDocumentInfoService(HrDocumentInfo)
