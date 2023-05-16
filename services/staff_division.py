import uuid
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi.logger import logger as log

from exceptions import BadRequestException, NotFoundException, NotSupportedException
from models import StaffDivision, StaffDivisionEnum
from schemas import (
    StaffDivisionCreate,
    StaffDivisionRead,
    StaffDivisionUpdate,
    StaffDivisionUpdateParentGroup,
    StaffDivisionOptionRead,
)

from .base import ServiceBase


class StaffDivisionService(ServiceBase[StaffDivision, StaffDivisionCreate, StaffDivisionUpdate]):

    def get_by_id(self, db: Session, id: str) -> StaffDivision:
        group = super().get(db, id)
        if group is None:
            raise NotFoundException(f"StaffDivision with id: {id} is not found!")
        return group

    def get_departments(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[StaffDivision]:
        departments = db.query(self.model).filter(
            StaffDivision.parent_group_id == None,
            StaffDivision.name.not_in([*StaffDivisionEnum])
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return departments
    
    def get_all_parents(self, db: Session, skip: int, limit: int) -> List[StaffDivision]:
        parents = db.query(self.model).filter(
            StaffDivision.parent_group_id == None
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()
        return parents

    def get_child_groups(self, db: Session, id: str, skip: int, limit: int) -> List[StaffDivision]:
        return db.query(self.model).filter(
           StaffDivision.parent_group_id == id
        ).order_by(StaffDivision.created_at).offset(skip).limit(limit).all()

    def get_by_name(self, db: Session, name: str) -> StaffDivision:
        group = db.query(self.model).filter(
            StaffDivision.name == name
        ).first()

        if group is None:
            raise NotFoundException(f"StaffDivision with name: {name} is not found!")
        return group

    def change_parent_group(self,
            db: Session,
            id: str,
            body: StaffDivisionUpdateParentGroup
    ) -> StaffDivisionRead:
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
    
    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        if id is None:
            return [StaffDivisionOptionRead.from_orm(i) for i in self.get_all_parents(db, skip, limit)]
        return [StaffDivisionOptionRead.from_orm(i) for i in self.get_child_groups(db, id, skip, limit)]


staff_division_service = StaffDivisionService(StaffDivision)
