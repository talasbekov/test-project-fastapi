from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import position_service, user_service, staff_division_service


class PositionAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "position"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        full_name, full_nameKZ = staff_division_service.get_full_name(db, user.staff_unit.staff_division_id)
        full_name = full_name.replace("/", "")
        full_nameKZ = full_nameKZ.replace("/", "")
        res = f"{full_name} {user.staff_unit.position.name} ({user.staff_unit.position.category_code}) ({user.actual_staff_unit.position.name})"
        resKZ = f"{full_nameKZ} {user.staff_unit.position.nameKZ} ({user.staff_unit.position.category_code}) ({user.actual_staff_unit.position.nameKZ})"
        return AutoTagRead(name=res, nameKZ=resKZ)


handler = PositionAutoTagHandler()
