import uuid

from sqlalchemy.orm import Session
from api.v1 import position


from exceptions.client import NotFoundException, BadRequestException
from models import ArchiveStaffUnit, StaffUnit, ArchiveStaffDivision
from schemas import ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate, ArchiveStaffUnitFunctions, \
    NewArchiveStaffUnitCreate, NewArchiveStaffUnitUpdate
from services import (
    service_staff_function_service,
    document_staff_function_service
)
from .archive_position import archive_position_service

from services.base import ServiceBase


class ArchiveStaffUnitService(ServiceBase[ArchiveStaffUnit, ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str) -> ArchiveStaffUnit:
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail=f"ArchiveStaffUnit with id: {id} is not found!")
        return position
    
    def get_by_user(self, db: Session, user_id: str) -> ArchiveStaffUnit:
        position = db.query(self.model).filter(
            self.model.user_id == user_id
        ).first()
        
        if position is None:
            raise NotFoundException(detail=f"ArchiveStaffUnit with user_id: {user_id} is not found!")
        
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

    def remove(self, db: Session, id: uuid.UUID) -> ArchiveStaffUnit:
        self._validate_leader(db, id)
        super().remove(db, str(id))

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

    def create_based_on_existing_staff_unit(self, db: Session,
                                            staff_unit: StaffUnit, 
                                            user_id: uuid.UUID,
                                            staff_unit_form: str,
                                            actual_user_id: uuid.UUID,
                                            user_replacing_id: uuid.UUID,
                                            archive_staff_division: ArchiveStaffDivision):
        position = archive_position_service.get_by_origin_id(db,staff_unit.position_id)
        return super().create(db, ArchiveStaffUnitCreate(
            position_id=position.id,
            staff_division_id=archive_staff_division.id,
            user_id=user_id,
            form=staff_unit_form,
            actual_user_id=user_id,
            user_replacing_id=user_replacing_id,
            origin_id=staff_unit.id
        ))

    def create_staff_unit(self, db: Session, body: NewArchiveStaffUnitCreate):
        return super().create(db, ArchiveStaffUnitCreate(
            position_id=body.position_id,
            staff_division_id=body.staff_division_id,
            user_id=body.user_id,
            form=body.form,
            actual_user_id=body.actual_user_id,
            user_replacing_id=body.user_replacing_id,
            origin_id=None
        ))

    def update_staff_unit(self, db: Session, staff_unit: ArchiveStaffUnit, body: NewArchiveStaffUnitUpdate):
        return super().update(db, db_obj=staff_unit, obj_in=ArchiveStaffUnitUpdate(
            position_id=body.position_id,
            staff_division_id=body.staff_division_id,
            user_id=body.user_id,
            form=body.form,
            actual_user_id=body.actual_user_id,
            user_replacing_id=body.user_replacing_id,
            origin_id=staff_unit.origin_id
        ))

    def get_service_staff_functions(self, db: Session, staff_unit_id: uuid.UUID):
        staff_unit = self.get_by_id(db, staff_unit_id)
        # filter so that only service staff functions are returned discriminator field is different
        return [staff_function for staff_function in staff_unit.staff_functions if staff_function.discriminator == "service_staff_function"]

    def get_document_staff_functions(self, db: Session, staff_unit_id: uuid.UUID):
        staff_unit = self.get_by_id(db, staff_unit_id)
        # filter so that only document staff functions are returned discriminator field is different
        return [staff_function for staff_function in staff_unit.staff_functions if staff_function.discriminator == "document_staff_function"]

    def get_object(self, db: Session, id: uuid.UUID, type: str):
        return db.query(ArchiveStaffUnit).filter(ArchiveStaffUnit.id == id).first()
    
    def _validate_leader(self, db: Session, staff_unit_id: uuid.UUID):
        # get staff_division by staff unit id, if staff_unit is staff_division leader, raise Exception
        staff_division = (db.query(ArchiveStaffDivision)
                          .filter(ArchiveStaffDivision.leader_id == staff_unit_id)
                          .first())
        if staff_division:
            raise BadRequestException(detail=f"Невозможно удалить начальника {staff_division.name}")


archive_staff_unit_service = ArchiveStaffUnitService(ArchiveStaffUnit)
