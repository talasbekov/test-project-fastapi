import json
from typing import List

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException, BadRequestException
from models import ArchiveStaffUnit, StaffUnit, ArchiveStaffDivision
from schemas import (
    ArchiveStaffUnitCreate,
    ArchiveStaffUnitUpdate,
    ArchiveStaffUnitFunctions,
    NewArchiveStaffUnitCreate,
    NewArchiveStaffUnitUpdate
)
from services import position_service

from .service_archive_staff_function import service_archive_staff_function_service
from .document_archive_staff_function import document_archive_staff_function_service

from . import increment_changes_size
from services.base import ServiceBase


class ArchiveStaffUnitService(
        ServiceBase[ArchiveStaffUnit, ArchiveStaffUnitCreate, ArchiveStaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str) -> ArchiveStaffUnit:
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(
                detail=f"ArchiveStaffUnit with id: {id} is not found!")
        return position
    
    def get_by_id_for_api(self, db: Session, id: str) -> ArchiveStaffUnit:
        archive_staff_unit = super().get(db, id)
        if isinstance(archive_staff_unit.requirements, str):
            archive_staff_unit.requirements = eval(archive_staff_unit.requirements)
        if archive_staff_unit is None:
            raise NotFoundException(
                detail=f"ArchiveStaffUnit with id: {id} is not found!")
        return archive_staff_unit

    
    def dispose_all_units(
            self,
            db: Session,
            archive_staff_unit_ids: List[str],
            archive_staff_division_id: str):
        (db.query(self.model)
           .filter(self.model.id.in_(archive_staff_unit_ids))
           .update(
               {self.model.staff_division_id: archive_staff_division_id}
           )
        )
        return db.query(self.model).filter(
            self.model.id.in_(archive_staff_unit_ids)).all()

    def get_by_archive_staff_division_id(
            self,
            db: Session,
            archive_staff_division_id: str) -> ArchiveStaffUnit:
        archive_staff_units = (db.query(ArchiveStaffUnit)
                               .filter(ArchiveStaffUnit.staff_division_id
                                       == archive_staff_division_id)
                               .all()
                               )
        if archive_staff_units is None:
            raise NotFoundException(
                detail=f"ArchiveStaffUnit with id: {id} is not found!")
        return archive_staff_units

    def duplicate_archive_staff_units_by_division_id(
            self,
            db: Session,
            duplicate_division_id: str,
            division_id: str):

        archive_staff_units = self.get_by_archive_staff_division_id(
            db, division_id)

        for archive_staff_unit in archive_staff_units:
            duplicate_unit = ArchiveStaffUnit()

            duplicate_unit.requirements = archive_staff_unit.requirements
            duplicate_unit.position_id = archive_staff_unit.position_id
            duplicate_unit.staff_division_id = duplicate_division_id
            duplicate_unit.user_id = None
            duplicate_unit.curator_of_id = archive_staff_unit.curator_of_id
            duplicate_unit.form = archive_staff_unit.form
            duplicate_unit.actual_user_id = archive_staff_unit.actual_user_id
            duplicate_unit.origin_id = archive_staff_unit.origin_id
            duplicate_unit.user_replacing_id = archive_staff_unit.user_replacing_id

            db.add(duplicate_unit)
            db.flush()

    def get_by_user(self, db: Session, user_id: str) -> ArchiveStaffUnit:
        position = db.query(self.model).filter(
            self.model.user_id == user_id
        ).first()

        if position is None:
            raise NotFoundException(
                detail=f"ArchiveStaffUnit with user_id: {user_id} is not found!")

        return position

    def add_service_staff_function(
            self,
            db: Session,
            body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_archive_staff_function_service.get_by_id(
                db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_service_staff_function(
            self,
            db: Session,
            body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_archive_staff_function_service.get_by_id(
                db, id)
            if staff_function is None:
                continue
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError:
                continue

        db.add(staff_unit)
        db.flush()

    def remove(self, db: Session, id: str) -> ArchiveStaffUnit:
        self._validate_leader(db, id)
        super().remove(db, str(id))

    def add_document_staff_function(
            self,
            db: Session,
            body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = document_archive_staff_function_service.get_by_id(
                db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_document_staff_function(
            self, db: Session, body: ArchiveStaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = document_archive_staff_function_service.get_by_id(
                db, id)
            if staff_function is None:
                continue
            try:
                staff_unit.staff_functions.remove(staff_function)
            except ValueError:
                continue

        db.add(staff_unit)
        db.flush()

    def create_based_on_existing_staff_unit(
            self,
            db: Session,
            staff_unit: StaffUnit,
            curator_of_id: str,
            user_id: str,
            position_id: str,
            actual_position_id: str,
            actual_user_id: str,
            user_replacing_id: str,
            archive_staff_division: ArchiveStaffDivision):
        # print(staff_unit.requirements)
        return super().create(db, ArchiveStaffUnitCreate(
            position_id=position_id,
            actual_position_id=actual_position_id,
            staff_division_id=archive_staff_division.id,
            curator_of_id=curator_of_id,
            user_id=user_id,
            actual_user_id=actual_user_id,
            user_replacing_id=user_replacing_id,
            origin_id=staff_unit.id,
            requirements=staff_unit.requirements
        ))

    def create_staff_unit(self, db: Session, body: NewArchiveStaffUnitCreate):
        self._validate_archive_staff_position(db, body.position_id)
        reqs = None
        if isinstance(body.requirements, list):
            reqs = []
            for requirements in body.requirements:
                reqs.append(requirements.dict())
            reqs = json.dumps(reqs)
        archive_staff_unit = super().create(db, ArchiveStaffUnitCreate(
            position_id=body.position_id,
            staff_division_id=body.staff_division_id,
            user_id=body.user_id,
            actual_user_id=body.actual_user_id,
            user_replacing_id=body.user_replacing_id,
            origin_id=None,
            requirements=reqs,
            curator_of_id=body.curator_of_id,
        ))
        increment_changes_size(db, archive_staff_unit.staff_division.staff_list)
        if isinstance(archive_staff_unit.requirements, str):
            archive_staff_unit.requirements = json.loads(archive_staff_unit.requirements)
        if archive_staff_unit.user_replacing:
            if isinstance(archive_staff_unit.user_replacing.staff_unit.requirements, str):
                archive_staff_unit.user_replacing.staff_unit.requirements = json.loads(archive_staff_unit.user_replacing.staff_unit.requirements)
        return archive_staff_unit

    def update_staff_unit(
            self,
            db: Session,
            staff_unit: ArchiveStaffUnit,
            body: NewArchiveStaffUnitUpdate):
        self._validate_archive_staff_position(db, body.position_id)
        reqs = None
        if isinstance(body.requirements, list):
            reqs = []
            for requirements in body.requirements:
                reqs.append(requirements)
            reqs = json.dumps(reqs)
        archive_staff_unit = super().update(
            db,
            db_obj=staff_unit,
            obj_in=ArchiveStaffUnitUpdate(
                position_id=body.position_id,
                staff_division_id=body.staff_division_id,
                curator_of_id=body.curator_of_id,
                user_id=body.user_id,
                actual_user_id=body.actual_user_id,
                user_replacing_id=body.user_replacing_id,
                origin_id=staff_unit.origin_id,
                requirements=reqs))
        increment_changes_size(db, archive_staff_unit.staff_division.staff_list)
        if isinstance(archive_staff_unit.requirements, str):
            archive_staff_unit.requirements = json.loads(archive_staff_unit.requirements)
        if archive_staff_unit.user_replacing:
            if isinstance(archive_staff_unit.user_replacing.staff_unit.requirements, str):
                archive_staff_unit.user_replacing.staff_unit.requirements = json.loads(archive_staff_unit.user_replacing.staff_unit.requirements)
        return archive_staff_unit

    def _validate_archive_staff_position(
            self, db: Session, position_id: str):
        position_service.get_by_id(db, position_id)

    def get_service_staff_functions(
            self, db: Session, staff_unit_id: str):
        staff_unit = self.get_by_id(db, staff_unit_id)
        # filter so that only service staff functions are returned
        # discriminator field is different
        return [staff_function
                for staff_function in staff_unit.staff_functions
                if staff_function.discriminator
                == "service_staff_function"]

    def get_document_staff_functions(
            self, db: Session, staff_unit_id: str):
        staff_unit = self.get_by_id(db, staff_unit_id)
        # filter so that only document staff functions are returned
        # discriminator field is different
        return [staff_function
                for staff_function in staff_unit.staff_functions
                if staff_function.discriminator
                == "document_staff_function"]

    def get_object(self, db: Session, id: str, type: str):
        return db.query(ArchiveStaffUnit).filter(
            ArchiveStaffUnit.id == id).first()

    def get_all_by_staff_division_id(self, db: Session,
                                 staff_division_id: str,
                                 skip: int = 0,
                                 limit: int = 1000,
                                 filter: str = ''):
        staff_units = (db.query(self.model)
                       .filter(self.model.staff_division_id == staff_division_id))

        if filter != '':
            staff_units = self._add_filter_to_query(staff_units, filter)

        total = staff_units.count()

        staff_units = (staff_units
                       .offset(skip)
                       .limit(limit)
                       .all())

        return {'total': total, 'objects': staff_units}

    def _add_filter_to_query(self, staff_unit_query, filter):
        key_words = filter.lower().split()
        staff_units = (
            staff_unit_query
            .filter(
                and_(func.concat(func.concat(func.concat(func.lower(ArchiveStaffUnit.user.first_name), ' '),
                                             func.concat(func.lower(ArchiveStaffUnit.user.last_name), ' ')),
                                 func.lower(ArchiveStaffUnit.user.father_name))
                     .contains(name) for name in key_words)
            )
        )
        return staff_units


    def _validate_leader(self, db: Session, staff_unit_id: str):
        # get staff_division by staff unit id, if staff_unit is staff_division
        # leader, raise Exception
        staff_division = (db.query(ArchiveStaffDivision) .filter(
            ArchiveStaffDivision.leader_id == staff_unit_id) .first())
        if staff_division:
            raise BadRequestException(
                detail=f"Невозможно удалить начальника {staff_division.name}")


archive_staff_unit_service = ArchiveStaffUnitService(ArchiveStaffUnit)
