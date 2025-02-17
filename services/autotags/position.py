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
        
        try:
            category_code = user.staff_unit.actual_position.category_code.upper()
        except: 
            category_code = user.staff_unit.position.category_code.upper()
        finally:
            category_code = ''
        
        try:
            actual_position_name = user.staff_unit.actual_position.name
            actual_position_nameKZ = user.staff_unit.actual_position.nameKZ
        except:
            actual_position_name = ''
            actual_position_nameKZ = ''

        position = (f"({user.staff_unit.position.name})"
                           if user.staff_unit.position else "")
        positionKZ = (f"({user.staff_unit.position.nameKZ})"
                             if user.staff_unit.position else "")
        res = (f"{full_name} {actual_position_name}"
               f" ({category_code})"
               f" {position}")
        resKZ = (f"{full_name} {actual_position_nameKZ}"
               f" ({category_code})"
               f" {positionKZ}")
        return AutoTagRead(name=res, nameKZ=resKZ)


handler = PositionAutoTagHandler()
