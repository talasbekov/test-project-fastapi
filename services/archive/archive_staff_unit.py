import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveStaffUnit, StaffUnit, ArchiveStaffDivision
from schemas import ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate, ArchiveStaffUnitFunctions, \
    NewArchiveStaffUnitCreate, NewArchiveStaffUnitUpdate
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

    def create_based_on_existing_staff_unit(self, db: Session, staff_unit: StaffUnit, user_id: uuid.UUID, actual_user_id: uuid.UUID, archive_staff_division: ArchiveStaffDivision):
        return super().create(db, ArchiveStaffUnitCreate(
            position_id=staff_unit.position_id,
            staff_division_id=archive_staff_division.id,
            user_id=user_id,
            actual_user_id=user_id,
            origin_id=staff_unit.id
        ))

    def create_staff_unit(self, db: Session, body: NewArchiveStaffUnitCreate):
        return super().create(db, ArchiveStaffUnitCreate(
            position_id=body.position_id,
            staff_division_id=body.staff_division_id,
            user_id=body.user_id,
            actual_user_id=body.actual_user_id,
            origin_id=None
        ))

    def update_staff_unit(self, db: Session, staff_unit: ArchiveStaffUnit, body: NewArchiveStaffUnitUpdate):
        return super().update(db, db_obj=staff_unit, obj_in=ArchiveStaffUnitUpdate(
            position_id=body.position_id,
            staff_division_id=body.staff_division_id,
            user_id=body.user_id,
            actual_user_id=body.actual_user_id,
            origin_id=None
        ))


archive_staff_unit_service = ArchiveStaffUnitService(ArchiveStaffUnit)
