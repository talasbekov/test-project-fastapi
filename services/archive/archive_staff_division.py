import uuid
from typing import List

from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import ArchiveStaffDivision, StaffDivision, StaffDivisionEnum
from schemas import (ArchiveStaffDivisionCreate, ArchiveStaffDivisionUpdate,
                     ArchiveStaffDivisionUpdateParentGroup, ArchiveStaffDivisionRead, NewArchiveStaffDivisionCreate,
                     NewArchiveStaffDivisionUpdate)
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
            staff_list_id: uuid.UUID,
            skip: int = 0,
            limit: int = 100
    ) -> List[ArchiveStaffDivision]:
        return db.query(self.model).filter(
            ArchiveStaffDivision.staff_list_id == staff_list_id,
            ArchiveStaffDivision.parent_group_id == None,
        ).offset(skip).limit(limit).all()
    
    def get_parents(self, db: Session, staff_list_id: uuid.UUID) -> List[ArchiveStaffDivision]:
        return db.query(self.model).filter(
            ArchiveStaffDivision.staff_list_id == staff_list_id,
            ArchiveStaffDivision.parent_group_id == None,
            StaffDivision.name.not_in([*StaffDivisionEnum])
        ).all()

    def change_parent_group(self,
            db: Session,
            id: str,
            body: ArchiveStaffDivisionUpdateParentGroup
    ) -> ArchiveStaffDivisionRead:
        group = self.get_by_id(db, id)
        self.get_by_id(db, body.parent_group_id)
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

    def get_division_parents_by_id(self, db: Session, archive_staff_division_id: uuid.UUID):

        archive_staff_division = self.get_by_id(db, archive_staff_division_id)

        parent_id = archive_staff_division.parent_group_id

        prev_archive_staff_division = archive_staff_division
        archive_staff_division.children = []
        while parent_id is not None:
            archive_staff_division = self.get_by_id(db, parent_id)
            archive_staff_division.children = [prev_archive_staff_division]
            prev_archive_staff_division = archive_staff_division
            parent_id = archive_staff_division.parent_group_id
        res = ArchiveStaffDivisionRead.from_orm(archive_staff_division)
        db.rollback()
        return res

    def create_based_on_existing_staff_division(self, db: Session, staff_division: StaffDivision, staff_list_id: uuid.UUID, parent_group_id: uuid.UUID):
        return super().create(db, ArchiveStaffDivisionCreate(
            parent_group_id=parent_group_id,
            name=staff_division.name,
            description=staff_division.description,
            staff_list_id=staff_list_id,
            origin_id=staff_division.id,
            is_combat_unit=staff_division.is_combat_unit,
            leader_id=None,
        ))

    def create_staff_division(self, db: Session, body: NewArchiveStaffDivisionCreate):
        return super().create(db, ArchiveStaffDivisionCreate(
            parent_group_id=body.parent_group_id,
            name=body.name,
            description=body.description,
            staff_list_id=body.staff_list_id,
            origin_id=None,
            is_combat_unit=body.is_combat_unit,
            leader_id=body.leader_id,
        ))

    def update_staff_division(self, db: Session, archive_staff_division: ArchiveStaffDivision, body: NewArchiveStaffDivisionUpdate):
        return super().update(db, db_obj=archive_staff_division, obj_in=ArchiveStaffDivisionUpdate(
            parent_group_id=body.parent_group_id,
            name=body.name,
            description=body.description,
            staff_list_id=body.staff_list_id,
            origin_id=None,
            is_combat_unit=body.is_combat_unit,
            leader_id=body.leader_id,
        ))


archive_staff_division_service = ArchiveStaffDivisionService(ArchiveStaffDivision)
