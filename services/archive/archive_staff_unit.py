from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveStaffUnit
from schemas import ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate, ArchiveStaffUnitFunctions
from services import service_staff_function_service, document_staff_function_service

from services.base import ServiceBase


class ArchiveStaffUnitService(ServiceBase[ArchiveStaffUnit, ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str) -> ArchiveStaffUnit:
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail="StaffUnit is not found!")
        return position

    def add_service_staff_function(self, db: Session, body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        print(staff_unit.staff_functions)

        db.add(staff_unit)
        db.flush()

    def remove_service_staff_function(self, db: Session, body: ArchiveStaffUnitFunctions):
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

    def add_document_staff_function(self, db: Session, body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = document_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_document_staff_function(self, db: Session, body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = document_staff_function_service.get_by_id(db, id)
            if staff_function is None:
                continue
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError as e:
                continue

        db.add(staff_unit)
        db.flush()


archive_staff_unit_service = ArchiveStaffUnitService(ArchiveStaffUnit)
