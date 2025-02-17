import uuid
import json
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import ArchiveStaffDivision, StaffDivision, StaffDivisionEnum
from schemas import (
    ArchiveStaffDivisionCreate,
    ArchiveStaffDivisionUpdate,
    ArchiveStaffDivisionUpdateParentGroup,
    ArchiveStaffDivisionRead,
    NewArchiveStaffDivisionCreate,
    NewArchiveStaffDivisionUpdate,
    ArchiveStaffDivisionReadSchedule,)
from services.base import ServiceBase
from . import increment_changes_size
from .archive_staff_unit import archive_staff_unit_service


class ArchiveStaffDivisionService(
        ServiceBase[ArchiveStaffDivision,
                     ArchiveStaffDivisionCreate,
                     ArchiveStaffDivisionUpdate]):

    def get_by_id(self, db: Session, id: str):
        group = super().get(db, id)
        for child in group.children:
            if isinstance(child.description, str):
                child.description = json.loads(child.description)
            for staff_unit in child.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(staff_unit.requirements)
        if isinstance(group.description, str):
             group.description = json.loads(group.description)
        for staff_unit in group.staff_units:
            if isinstance(staff_unit.requirements, str):
                staff_unit.requirements = json.loads(staff_unit.requirements)
            if staff_unit.user_replacing:
                if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                    staff_unit.user_replacing.staff_unit.requirements = json.loads(staff_unit.user_replacing.staff_unit.requirements)
        if group is None:
            raise NotFoundException(
                f"ArchiveStaffDivision with id: {id} is not found!")
        # return ArchiveStaffDivisionReadSchedule.from_orm(group).update_forward_refs()
        return group

    def get_by_name(self, db: Session, name: str,
                    staff_list_id: str) -> ArchiveStaffDivision:
        group = db.query(self.model).filter(
            self.model.name == name,
            self.model.staff_list_id == staff_list_id
        ).first()
        if group is None:
            raise NotFoundException(
                f"ArchiveStaffDivision with name: {name} is not found!")
        return group

    def get_departments(
            self,
            db: Session,
            staff_list_id: str,
            skip: int = 0,
            limit: int = 10
    ): 
        archive_divisions = db.query(self.model).filter(
            ArchiveStaffDivision.staff_list_id == staff_list_id,
            ArchiveStaffDivision.parent_group_id == None,
            ArchiveStaffDivision.name != StaffDivisionEnum.DISPOSITION.value
        ).offset(skip).limit(limit).all()
        disposition_division = self.get_by_name(db,
                                        StaffDivisionEnum.DISPOSITION.value,
                                        staff_list_id)
        archive_divisions.append(disposition_division)
        for archive_division in archive_divisions:
            for child in archive_division.children:
                if isinstance(child.description, str):
                    child.description = json.loads(child.description)
                for staff_unit in child.staff_units:
                    if isinstance(staff_unit.requirements, str):
                        staff_unit.requirements = json.loads(staff_unit.requirements)
            if isinstance(archive_division.description, str):
                archive_division.description = json.loads(archive_division.description)
            for staff_unit in archive_division.staff_units:
                if isinstance(staff_unit.requirements, str):
                    staff_unit.requirements = json.loads(staff_unit.requirements)
                if staff_unit.user_replacing:
                    if isinstance(staff_unit.user_replacing.staff_unit.requirements, str):
                        staff_unit.user_replacing.staff_unit.requirements = json.loads(staff_unit.user_replacing.staff_unit.requirements)
        # archive_divisions = [ArchiveStaffDivisionRead.from_orm(archive_division) for archive_division in archive_divisions]
        # return [ArchiveStaffDivisionReadSchedule.from_orm(parent).update_forward_refs() for parent in archive_divisions]
        return archive_divisions
    def get_parents(self, db: Session,
                    staff_list_id: str) -> List[ArchiveStaffDivision]:
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
        self._validate_parent(db, body.parent_group_id)
        group.parent_group_id = body.parent_group_id
        setattr(group, 'updated_at', datetime.now())
        db.add(group)
        increment_changes_size(db, group.staff_list)
        db.flush()
        return group

    def get_department_id_from_staff_division_id(
            self, db: Session, staff_division_id: str):

        staff_division = self.get_by_id(db, staff_division_id)

        parent_id = staff_division.parent_group_id

        res_id = staff_division.id

        while parent_id is not None:
            res_id = parent_id
            tmp = self.get_by_id(db, parent_id)
            parent_id = tmp.parent_group_id

        return res_id

    def get_division_parents_by_id(
            self, db: Session, archive_staff_division_id: str):

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

    def create_based_on_existing_staff_division(
            self,
            db: Session,
            staff_division: StaffDivision,
            staff_list_id: str,
            parent_group_id: str):
        self._validate_parent(db, parent_group_id)
        return super().create(db, ArchiveStaffDivisionCreate(
            parent_group_id=parent_group_id,
            name=staff_division.name,
            nameKZ=staff_division.nameKZ,
            description='{"name": "", "nameKZ": ""}',
            type_id=staff_division.type_id,
            staff_division_number=staff_division.staff_division_number,
            staff_list_id=staff_list_id,
            origin_id=staff_division.id,
            is_combat_unit=staff_division.is_combat_unit,
            leader_id=None,
        ))

    def create_staff_division(self, db: Session,
                              body: NewArchiveStaffDivisionCreate):
        self._validate_parent(db, body.parent_group_id)
        res = super().create(db, ArchiveStaffDivisionCreate(
            parent_group_id=body.parent_group_id,
            name=body.name,
            nameKZ=body.nameKZ,
            description=body.description,
            staff_list_id=body.staff_list_id,
            type_id=body.type_id,
            staff_division_number=body.staff_division_number,
            origin_id=None,
            is_combat_unit=body.is_combat_unit,
            leader_id=body.leader_id,
        ))
        increment_changes_size(db, res.staff_list)
        return res

    def update_staff_division(
            self,
            db: Session,
            archive_staff_division: ArchiveStaffDivision,
            body: NewArchiveStaffDivisionUpdate):

        self._validate_parent(db, body.parent_group_id)
        res = super().update(db,
                             db_obj=archive_staff_division,
                             obj_in=ArchiveStaffDivisionUpdate(
            parent_group_id=body.parent_group_id,
            name=body.name,
            nameKZ=body.nameKZ,
            description=body.description,
            staff_list_id=body.staff_list_id,
            type_id=body.type_id,
            staff_division_number=body.staff_division_number,
            origin_id=None,
            is_combat_unit=body.is_combat_unit,
            leader_id=body.leader_id,
        ))
        increment_changes_size(db, res.staff_list)
        return res

    def duplicate(self, db: Session, id: str):
        archive_staff_division = archive_staff_division_service.get_by_id(
            db, str(id))

        # Create a new instance of ArchiveStaffDivision
        duplicate_division = ArchiveStaffDivision()

        # Copy the properties
        duplicate_division.parent_group_id = archive_staff_division.parent_group_id
        duplicate_division.description = archive_staff_division.description
        duplicate_division.is_combat_unit = archive_staff_division.is_combat_unit
        duplicate_division.leader_id = None
        duplicate_division.type_id = archive_staff_division.type_id,
        duplicate_division.staff_division_number = \
            archive_staff_division.staff_division_number
        duplicate_division.staff_list_id = archive_staff_division.staff_list_id
        duplicate_division.origin_id = archive_staff_division.origin_id
        duplicate_division.name = archive_staff_division.name + '_copy'
        duplicate_division.nameKZ = archive_staff_division.nameKZ + '_copy'

        # Copy the children
        for child in archive_staff_division.children:
            duplicate_child = self.duplicate(db, child.id)
            duplicate_division.children.append(duplicate_child)

        db.add(duplicate_division)
        increment_changes_size(db, duplicate_division.staff_list)
        db.flush()
        archive_staff_unit_service.duplicate_archive_staff_units_by_division_id(
            db, duplicate_division.id, id)
        # Return the duplicated division
        return duplicate_division

    def _validate_parent(self, db: Session, parent_id: str):
        parent = super().get(db, parent_id)
        if parent is None and parent_id:
            raise BadRequestException(
                f"Parent ArchiveStaffDivision with id: {parent_id} is not found!")


archive_staff_division_service = ArchiveStaffDivisionService(
    ArchiveStaffDivision)
