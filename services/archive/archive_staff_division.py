import uuid
from typing import List

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import ArchiveStaffDivision
from schemas import (ArchiveStaffDivisionCreate, ArchiveStaffDivisionUpdate,
                     ArchiveStaffDivisionUpdateParentGroup, ArchiveStaffDivisionRead)

from services.base import ServiceBase


class ArchiveStaffDivisionService(ServiceBase[ArchiveStaffDivision, ArchiveStaffDivisionCreate, ArchiveStaffDivisionUpdate]):

    def get_by_id(self, db: Session, id: str) -> ArchiveStaffDivision:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"StaffDivision with id: {id} is not found!")
        return group

    def get_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[ArchiveStaffDivision]:
        return db.query(self.model).filter(
            ArchiveStaffDivision.parent_group_id == None
        ).offset(skip).limit(limit).all()
    
    def get_parents(self, db: Session) -> List[ArchiveStaffDivision]:
        return db.query(self.model).filter(
            ArchiveStaffDivision.parent_group_id == None
        ).all()

    def change_parent_group(self,
            db: Session,
            id: str,
            body: ArchiveStaffDivisionUpdateParentGroup
    ) -> ArchiveStaffDivisionRead:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"StaffDivision with id: {id} is not found!")

        parent_group = super().get(db, body.parent_group_id)
        if parent_group is None:
            raise BadRequestException(f"Parent staffDivision with id: {body.parent_group_id} is not found!")
        group.parent_group_id = body.parent_group_id
        db.add(group)
        db.flush()
        return group
    
    def get_department_id_from_staff_division_id(self, db: Session, staff_division_id: uuid.UUID):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        res_id = staff_division.id

        while parent_id != None:
            res_id = parent_id
            tmp = self.get_by_id(db, parent_id)
            parent_id = tmp.parent_group_id
        
        return res_id



archive_staff_division_service = ArchiveStaffDivisionService(ArchiveStaffDivision)
