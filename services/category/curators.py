import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Session

from models import (
    StaffDivisionEnum,
    StaffDivision,
)
from services import staff_division_service
from .base import BaseCategory

if TYPE_CHECKING:
    from services import (
        user_service,
    )


class CuratorCategory(BaseCategory):
    __handler__ = 1

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
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
        for group in groups:
            for staff_unit in group.curators:
                first_user = staff_unit.users[0]
                if first_user is not None:
                    res.add(first_user.id)
        return list(res)

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
        user = user_service.get_by_id(db, user_id)
        if user.staff_unit is None or user.staff_unit.courted_group is None:
            return False
        return True


handler = CuratorCategory()
