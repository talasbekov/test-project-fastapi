from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import StaffUnit, Position
from schemas import StaffUnitCreate, StaffUnitUpdate, StaffUnitFunctions
from services import service_staff_function_service, document_staff_function_service
from .base import ServiceBase


class StaffUnitService(ServiceBase[StaffUnit, StaffUnitCreate, StaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail="StaffUnit is not found!")
        return position

    def get_by_staff_division_id(self, db: Session, staff_division_id: str):
        return db.query(self.model).filter(self.model.staff_division_id == staff_division_id).all()

    def add_service_staff_function(self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        print(staff_unit.staff_functions)

        db.add(staff_unit)
        db.flush()

    def remove_service_staff_function(self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_staff_function_service.get_by_id(db, id)
            if staff_function is None:
                continue
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError as e:
                continue

        db.add(staff_unit)
        db.flush()

    def add_document_staff_function(self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = document_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_document_staff_function(self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = get_by_option
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError as e:
                continue

        db.add(staff_unit)
        db.flush()

    def get_all_by_position(self, db: Session, position_id: str):
        return db.query(self.model).filter(
            self.model.position_id == position_id
        ).first()


staff_unit_service = StaffUnitService(StaffUnit)
