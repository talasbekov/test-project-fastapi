from typing import Any, Optional

from charset_normalizer.md import List
from sqlalchemy.orm import Query, Session

from models import (
    ArchiveStaffDivision,
    StaffDivision,
    StaffUnit,
    ArchiveStaffUnit,
    User,
    HrDocument,
    PrivilegeEmergency
)
from exceptions import ForbiddenException
from .base import BaseHandler
from .. import (
    staff_division_service,
    staff_unit_service,
    staff_list_service,
    archive_staff_division_service,
    archive_privelege_emergency_service,
    privelege_emergency_service
)


class ApplyStaffListHandler(BaseHandler):
    __handler__ = "apply_staff_list"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        staff_list_id = self.get_args(action, props)
        staff_list_service.get_by_id(db, staff_list_id)

        staff_division_service.make_all_inactive(db)
        exclude_staff_division_ids = [i.id for i in staff_division_service.get_excluded_staff_divisions(db)]
        staff_unit_service.make_all_inactive(db, exclude_staff_division_ids)

        staff_divisions: list[ArchiveStaffDivision] = (
            archive_staff_division_service.get_departments(db, staff_list_id, 0, 100)
        )
        new_staff_divisions = []
        privelege_emergencies = archive_privelege_emergency_service.get_multi(db, 0, 100)
        for privelege_emergency in privelege_emergencies:
            self._create_privelege_emergency(db, privelege_emergency)
        for staff_division in staff_divisions:
            new_staff_division = self._create_staff_division(db, staff_division, None)
            new_staff_divisions.append(new_staff_division)

        db.flush()

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass


    def _create_staff_division(self, db: Session, staff_division: ArchiveStaffDivision, parent_id: Optional[int]) -> StaffDivision:
        is_leader_needed = None
        leader_id = None

        parent = archive_staff_division_service.get(db, staff_division.parent_group_id)

        new_staff_division = staff_division_service.create_or_update_from_archive(
            db,
            staff_division,
            parent.origin_id if parent else None,
            None
        )
        if staff_division.children:
            for child in staff_division.children:
                child_staff_division = self._create_staff_division(
                    db,
                    child,
                    new_staff_division.id
                )
                new_staff_division.children.append(child_staff_division)
            
        staff_division.origin_id = new_staff_division.id

        if staff_division.leader_id is not None:
            is_leader_needed = True
        staff_units: list[ArchiveStaffUnit] = staff_division.staff_units

        for staff_unit in staff_units:
            new_staff_unit = staff_unit_service.create_or_update_from_archive(db, staff_unit, new_staff_division.id)
            if is_leader_needed and staff_unit.id == staff_division.leader_id:
                leader_id = new_staff_unit.id
            staff_unit.origin_id = new_staff_unit.id
            db.add(new_staff_unit)
            db.add(staff_unit)

        new_staff_division.leader_id = leader_id
        db.add(new_staff_division)
        db.add(staff_division)
        db.flush()
        return new_staff_division
    

    def _create_privelege_emergency(self, db: Session, privelege_emergency: PrivilegeEmergency):
        privelege_emergency_service.create_or_update_from_archive(db, privelege_emergency)

    def get_args(self, action, properties):
        try:
            staff_list_id = properties[action["staff_list"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(f"Staff list is not defined for this action: {self.__handler__}")
        return staff_list_id


handler = ApplyStaffListHandler()
