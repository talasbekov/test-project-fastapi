from __future__ import annotations
import uuid
from typing import List

from sqlalchemy.orm import Session

from models import StaffDivisionEnum, User
from services import staff_division_service
from exceptions import NotFoundException
from .base import BaseCategory


class PgsCategory(BaseCategory):
    __handler__ = 2

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
        staff_divisions = (staff_division_service
                           .get_all_by_name(db,
                                            StaffDivisionEnum.SERVICE.value)
                           )
        res = set()
        for staff_division in staff_divisions:
            for staff_unit in staff_division.staff_units:
                for user in staff_unit.users:
                    if user.is_active:
                        res.add(user.id)
        return list(res)

    def get_templates(
        self,
        db: Session,
        role_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> List[uuid.UUID]:
        if self.validate(db, user_id):
            return []
        return super().get_templates(db, role_id, user_id, self.__handler__)

    def validate(
        self,
        db: Session,
        user_id: uuid.UUID,
    ) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundException(f'User with id {user_id} not found!')
        if user.staff_unit is None:
            return False
        service_division = staff_division_service.get_by_name(
            db,
            StaffDivisionEnum.SERVICE.value,
        )
        if user.staff_unit.staff_division.id != service_division.id:
            return False
        return True


handler = PgsCategory()
