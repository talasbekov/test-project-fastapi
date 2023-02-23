from datetime import datetime

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import HrDocumentInfo, HrDocumentStep
from schemas import (HrDocumentInfoCreate, HrDocumentInfoRead,
                     HrDocumentInfoUpdate)
from services import (hr_document_step_service, staff_division_service,
                      user_service)

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
    
    def create_info_for_step(self, db: Session, document_id: str, step_id: str, user_id: str, is_signed: bool):

        document_info = HrDocumentInfoCreate(
            hr_document_id=document_id,
            hr_document_step_id=step_id,
            signed_by=user_id,
            comment="",
            is_signed=is_signed,
            signed_at=datetime.now()
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
    
    def get_not_signed_by_position(self, db: Session, staff_unit_id: str, skip: int, limit: int):

        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.is_signed == None,
            HrDocumentInfo.hr_document_step.has(staff_unit_id = staff_unit_id)
        ).offset(skip).limit(limit).all()

        return infos
    
    def get_all(self, db: Session, staff_unit_id, skip: int, limit: int) -> list[HrDocumentInfo]:
        
        infos = db.query(HrDocumentInfo).filter(
            or_(
                and_(
                    HrDocumentInfo.is_signed == None,
                    HrDocumentInfo.hr_document_step.has(staff_unit_id = staff_unit_id)
                ),
                HrDocumentInfo.hr_document_step.has(previous_step_id = None)
            )
        ).order_by(
            desc(HrDocumentInfo.created_at)
        ).offset(skip).limit(limit).all()

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
        info.signed_at = datetime.now()

        db.add(info)
        db.flush()

        return info

    def get_by_document_id(self, db: Session, id: str):

        infos = db.query(HrDocumentInfo).filter(
            HrDocumentInfo.hr_document_id == id
        ).order_by(
            HrDocumentInfo.created_at.asc()
        ).all()

        last_info = infos[len(infos)-1]

        user = last_info.hr_document.users[0]

        step: HrDocumentStep = last_info.hr_document_step

        while step is not None:
            
            users = user_service.get_by_staff_unit(db, step.staff_unit_id)

            res = None

            for i in users:
                if staff_division_service.get_department_id_from_staff_division_id(db, user.staff_division_id) == staff_division_service.get_department_id_from_staff_division_id(db, i.staff_division_id):
                    res = i
                    break
            
            infos.append(
                {
                    "id": None,
                    "hr_document_step_id": step.id,
                    "hr_document_step": step,
                    "signed_by": None,
                    "comment": None,
                    "is_signed": None,
                    "signed_at": None,
                    "hr_document_id":  last_info.hr_document_id,
                    "will_sign": i
                }
            )

            if len(step.next_step) == 0:
                break

            print(step.next_step[0].id)

            tmp = hr_document_step_service.get_by_id(db, step.next_step[0].id)

            step = tmp

        infos.remove(last_info)

        infos.reverse()

        return infos


hr_document_info_service = HrDocumentInfoService(HrDocumentInfo)
