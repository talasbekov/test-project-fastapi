import uuid

from sqlalchemy.orm import Session

from schemas import UserShortRead
from models import User, StaffUnit, StaffDivisionEnum
from services import staff_division_service
from .base import BaseCategory


class PgsCategory(BaseCategory):
    __handler__ = 2

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
        staff_divisions = staff_division_service.get_all_by_name(db, StaffDivisionEnum.SERVICE.value)
        res = set()
        for staff_division in staff_divisions:
            for staff_unit in staff_division.staff_units:
                for user in staff_unit.users:
                    if user.is_active:
                        res.add(user.id)
        return list(res)


handler = PgsCategory()
