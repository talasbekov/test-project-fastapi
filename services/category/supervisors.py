import uuid

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from schemas import UserShortRead
from models import User, StaffUnit, Position, PositionNameEnum
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
                    func.lower(Position.name).contains(PositionNameEnum.SUPERVISOR.value.lower()),
                ),
            )
            .all()
        )
        res = list(set([user.id for user in users]))
        return res


handler = SupervisorCategory()
