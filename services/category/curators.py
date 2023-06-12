import uuid

from sqlalchemy.orm import Session

from schemas import UserShortRead
from models import StaffDivision, StaffDivisionEnum
from services import staff_division_service
from utils import is_valid_uuid
from .base import BaseCategory


class CuratorCategory(BaseCategory):
    __handler__ = 1

    def handle(self, db: Session) -> list[uuid.UUID]:
        staff_division = staff_division_service.get_by_name(db, StaffDivisionEnum.SERVICE.value)
        groups = (
            db.query(StaffDivision)
            .filter(
                StaffDivision.is_active == True,
                StaffDivision.parent_group_id == staff_division.id,
            )
            .all()
        )
        res = set()
        for group in groups:
            for staff_unit in group.staff_units:
                if staff_unit.users:
                    if staff_unit.users[0].supervised_by != None:
                        res.add(staff_unit.users[0].supervised_by)
        
        return list(res)


handler = CuratorCategory()
