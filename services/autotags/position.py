from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import user_service, staff_division_service


class PositionAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "position"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        full_name, full_nameKZ = staff_division_service.get_full_name(
            db, user.staff_unit.staff_division_id)
        full_name = full_name.replace("/", "")
        full_nameKZ = full_nameKZ.replace("/", "")
        actual_position = (f"({user.staff_unit.actual_position.name})"
                           if user.staff_unit.actual_position else "")
        actual_positionKZ = (f"({user.staff_unit.actual_position.nameKZ})"
                             if user.staff_unit.actual_position else "")
        res = (f"{full_name} {user.staff_unit.position.name}"
               f" ({user.staff_unit.position.category_code.upper()})"
               f" {actual_position}")
        resKZ = (f"{full_nameKZ} {user.staff_unit.position.nameKZ}"
                 f" ({user.staff_unit.position.category_code.upper()})"
                 f" {actual_positionKZ}")
        return AutoTagRead(name=res, nameKZ=resKZ)


handler = PositionAutoTagHandler()
