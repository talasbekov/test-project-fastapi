from typing import Any, Optional

from charset_normalizer.md import List
from sqlalchemy.orm import Query, Session

from models import ArchiveStaffDivision, StaffDivision, StaffUnit, ArchiveStaffUnit
from .base import BaseHandler
from .. import staff_division_service, staff_unit_service


class ApplyStaffListHandler(BaseHandler):
    __handler__ = "apply_staff_list"

    def handle_action(self, db: Session, staff_list: Optional[Any], staff_divisions: List[Any]):
        staff_division_query = db.query(StaffDivision)
        staff_unit_query = db.query(StaffUnit)
        for archive_staff_division in staff_list.archive_staff_divisions:
            self._handle_update(db, archive_staff_division, staff_list.id, staff_division_query,
                                staff_unit_query)

    def _handle_update(self, db: Session, archive_staff_division: ArchiveStaffDivision, staff_list_id,
                       staff_division_query: Query[Any], staff_unit_query: Query[Any]):
        staff_division_id = archive_staff_division.origin_id
        if staff_division_id:
            staff_division = staff_division_service.get_by_id(db, archive_staff_division.origin_id)
            staff_division.parent_group_id = archive_staff_division.parent_group_id
        else:
            pass
            # TODO: Create StaffDivision object

        if archive_staff_division.children:
            for child in archive_staff_division.children:
                self._handle_update(db, child, staff_list_id, staff_division_query, staff_unit_query)

        if archive_staff_division.staff_units:
            for archive_staff_unit in archive_staff_division.staff_units:
                staff_unit_id = archive_staff_unit.origin_id
                if staff_unit_id:
                    staff_unit = staff_unit_service.get_by_id(db, archive_staff_unit.origin_id)
                    staff_unit.staff_division = archive_staff_division.id
                else:
                    pass
                    # TODO: Create StaffUnit object

        db.add(archive_staff_division)
        db.flush()

    def handle_validation(self):
        pass


handler = ApplyStaffListHandler()
