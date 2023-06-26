from __future__ import annotations
import uuid
from typing import List

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models import User, StaffUnit, Position, PositionNameEnum
from exceptions import NotFoundException
from .base import BaseCategory


class SupervisorCategory(BaseCategory):
    __handler__ = 3

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
        users = (
            db.query(User)
            .join(User.staff_unit)
            .join(
                Position,
                and_(
                    StaffUnit.position_id == Position.id,
                    func.lower(
                        Position.name).contains(
                        PositionNameEnum.SUPERVISOR.value.lower()),
                ),
            )
            .all()
        )
        res = list(set([user.id for user in users]))
        return res

    def get_templates(
        self,
        db: Session,
        role_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> List[uuid.UUID]:
        if not self.validate(db, user_id):
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
        if user.staff_unit.position is None:
            return False
        if user.staff_unit.position.name.lower() not in\
                PositionNameEnum.SUPERVISOR.value.lower():
            return False
        return True


handler = SupervisorCategory()
