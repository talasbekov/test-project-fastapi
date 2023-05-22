import datetime
import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import StaffUnit, Position, User, StaffDivision, EmergencyServiceHistory, ArchiveStaffUnit, StaffDivisionEnum
from schemas import StaffUnitCreate, StaffUnitUpdate, StaffUnitFunctions, StaffUnitRead
from services import service_staff_function_service, document_staff_function_service, staff_division_service
from .base import ServiceBase


class StaffUnitService(ServiceBase[StaffUnit, StaffUnitCreate, StaffUnitUpdate]):
    def get_by_id(self, db: Session, id: uuid.UUID):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail=f"StaffUnit  with id: {id} is not found!")
        return position

    def get_by_staff_division_id(self, db: Session, staff_division_id: str):
        return db.query(self.model).filter(self.model.staff_division_id == staff_division_id).all()

    def add_service_staff_function(self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)


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

    def get_object(self, db: Session, id: str):
        return self.get(db, id)

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
            staff_function = document_staff_function_service.get_by_id(db, id)
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError as e:
                continue

        db.add(staff_unit)
        db.flush()

    def get_all_by_position(self, db: Session, position_id: str):
        return db.query(self.model).filter(
            self.model.position_id == position_id
        ).all()

    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        return [StaffUnitRead.from_orm(item).dict() for item in super().get_multi(db, skip, limit)]

    def create_relation(self, db:Session, user: User, staff_unit_id: uuid.UUID):
        staff_unit = self.get_by_id(db, staff_unit_id)
        staff_unit.users.append(user)
        db.add(staff_unit)
        db.flush()
        return staff_unit

    def exists_relation(self, db: Session, user_id: str, staff_unit_id: uuid.UUID):
        return (
            db.query(StaffUnit)
            .join(StaffUnit.users)
            .filter(User.id == user_id)
            .filter(StaffUnit.id == staff_unit_id)
            .first()
        ) is not None

    def existing_or_create(self, db: Session, name: str):
        staff_division = staff_division_service.get_by_name(db, name)
        staff_unit = self._get_free_by_staff_division_id(db, staff_division.id)

        if staff_unit is not None:
            return staff_unit
        else:
            position = db.query(Position).filter(Position.name == name).first()
            staff_unit = self.create(
                db,
                StaffUnit(
                    position_id=position.id,
                    staff_division_id=staff_division.id,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                )
            )

            staff_division.staff_units.append(staff_unit)
            db.add(staff_division)
            db.flush()
        return staff_unit

    def _get_free_by_staff_division_id(self, db: Session, staff_division_id: str):
        return (
            db.query(self.model)
            .filter(
                self.model.staff_division_id == staff_division_id,
                self.model.users == None
            )
            .first())

    def get_last_history(self, db: Session, user_id: uuid.UUID):
        return (
            db.query(EmergencyServiceHistory)
            .filter(
                EmergencyServiceHistory.user_id == user_id,
                EmergencyServiceHistory.date_to == None
            )
            .order_by(EmergencyServiceHistory.date_from.desc())
            .first()
        )

    def create_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit, staff_division_id: uuid.UUID):
        res = super().create(
            db, StaffUnitCreate(
                position_id=archive_staff_unit.position_id,
                staff_division_id=staff_division_id
                )
            )
        return res

    def update_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit, staff_division_id: uuid.UUID):
        staff_unit = self.get_by_id(db, archive_staff_unit.origin_id)
        res = super().update(
            db,
            db_obj=staff_unit,
            obj_in=StaffUnitUpdate(
                position_id=archive_staff_unit.position_id,
                staff_division_id=staff_division_id,
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit, staff_division_id: uuid.UUID):
        if archive_staff_unit.origin_id is None:
            return self.create_from_archive(db, archive_staff_unit, staff_division_id)
        return self.update_from_archive(db, archive_staff_unit, staff_division_id)

    def make_all_inactive(self, db: Session, exclude_ids: list[uuid.UUID] = []):
        db.query(self.model).filter(
            self.model.staff_division_id.not_in(exclude_ids)
        ).update({self.model.is_active: False})
        db.flush()

    def delete_all_inactive(self, db: Session, exclude_ids: list[uuid.UUID] = []):
        db.query(self.model).filter(
            self.model.staff_division_id.not_in(exclude_ids),
            self.model.is_active == False
        ).update({self.model.staff_division_id: None})
        db.flush()


staff_unit_service = StaffUnitService(StaffUnit)
