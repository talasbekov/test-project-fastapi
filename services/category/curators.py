import uuid

from sqlalchemy.orm import Session

from models import StaffDivision
from .base import BaseCategory


class CuratorCategory(BaseCategory):
    __handler__ = 1

    def handle(self, db: Session) -> list[uuid.UUID]:
        groups = (
            db.query(StaffDivision)
            .filter(
                StaffDivision.is_active == True,
                StaffDivision.curators.isnot(None),
            )
            .all()
        )
        res = set()
        for group in groups:
            for user in group.curators:
                res.add(user.id)
        return list(res)


handler = CuratorCategory()
