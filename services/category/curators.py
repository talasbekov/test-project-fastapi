from __future__ import annotations
import uuid
from typing import List

from sqlalchemy.orm import Session

from models import (
    StaffDivisionEnum,
    StaffDivision,
    User,
)
from services import staff_division_service
from exceptions import NotFoundException
from .base import BaseCategory


class CuratorCategory(BaseCategory):
    __handler__ = 1

    def handle(self, db: Session, user_id: str) -> list[str]:
        staff_division = staff_division_service.get_by_name(
            db, StaffDivisionEnum.SERVICE.value)
        groups = (
            db.query(StaffDivision)
            .filter(
                StaffDivision.is_active == True,
                StaffDivision.parent_group_id == staff_division.id,
            )
            .all()
        )
        res = set()
        print(groups)
        for group in groups:
            for staff_unit in group.curators:
                if staff_unit.users == []:
                    continue
                first_user = staff_unit.users[0]
                if first_user is not None:
                    res.add(first_user.id)
        return list(res)

    def get_templates(
        self,
        db: Session,
        role_id: str,
        user_id: str,
    ) -> List[str]:
        if not self.validate(db, user_id):
            return []
        return super().get_templates(db, role_id, user_id, self.__handler__)

    def validate(
        self,
        db: Session,
        user_id: str,
    ) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundException(f'User with id {user_id} not found!')
        if user.staff_unit is None or user.staff_unit.courted_group is None:
            return False
        return True


handler = CuratorCategory()
