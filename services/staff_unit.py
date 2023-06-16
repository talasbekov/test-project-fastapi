import datetime
import uuid

from sqlalchemy.orm import Session

from exceptions.client import BadRequestException, NotFoundException
from models import (StaffUnit, Position, User, EmergencyServiceHistory,
                    ArchiveStaffUnit, 
                    StaffDivision, PositionNameEnum, StaffDivisionEnum)
from schemas import (StaffUnitCreate, StaffUnitUpdate,
                     StaffUnitFunctions, StaffUnitRead,
                     StaffUnitCreateWithPosition, StaffUnitFunctionsByPosition
                    )
from services import (service_staff_function_service,
                      document_staff_function_service,
                      staff_division_service, position_service)
from .base import ServiceBase


class StaffUnitService(ServiceBase[StaffUnit, StaffUnitCreate, StaffUnitUpdate]):
    def get_by_id(self, db: Session, id: uuid.UUID):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail=f"StaffUnit  with position id: {id} is not found!")
        return position


    def create_with_position(self, db: Session, staff_unit_with_position: StaffUnitCreateWithPosition):

        position = Position(name=staff_unit_with_position.name,
                            nameKZ=staff_unit_with_position.nameKZ,
                            category_code=staff_unit_with_position.category_code,
                            max_rank_id=staff_unit_with_position.max_rank_id
                            )
        db.add(position)
        db.flush()

        staff_unit = StaffUnit(position_id=position.id,
                               staff_division_id=staff_unit_with_position.staff_division_id,
                               is_active=staff_unit_with_position.is_active,
                               requirements=staff_unit_with_position.requirements)
        db.add(staff_unit)
        db.flush()
        return staff_unit


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
            except ValueError:
                continue

        db.add(staff_unit)
        db.flush()

    def get_object(self, db: Session, id: str, type: str):
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
            except ValueError:
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

    def create_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit,
                            staff_division_id: uuid.UUID):
        res = super().create(
            db, StaffUnitCreate(
                position_id=archive_staff_unit.position_id,
                staff_division_id=staff_division_id,
                is_active=True,
                user_replacing_id=archive_staff_unit.user_replacing_id,
                requirements=archive_staff_unit.requirements
                )
            )
        return res

    def update_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit,
                            staff_division_id: uuid.UUID):
        staff_unit = self.get_by_id(db, archive_staff_unit.origin_id)
        res = super().update(
            db,
            db_obj=staff_unit,
            obj_in=StaffUnitUpdate(
                position_id=archive_staff_unit.position_id,
                staff_division_id=staff_division_id,
                is_active=True,
                user_replacing_id=archive_staff_unit.user_replacing_id,
                requirements=archive_staff_unit.requirements
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit, staff_division_id: uuid.UUID):
        if archive_staff_unit.origin_id is None:
            return self.create_from_archive(db, archive_staff_unit, staff_division_id)
        return self.update_from_archive(db, archive_staff_unit, staff_division_id)

    def make_all_inactive(self, db: Session, exclude_ids: list[uuid.UUID] = []):
        (db.query(self.model)
         .filter(
            self.model.staff_division_id.not_in(exclude_ids)
        )
        .update({self.model.is_active: False}))
        db.flush()

    def delete_all_inactive(self, db: Session, exclude_ids: list[uuid.UUID] = []):
        db.query(self.model).filter(
            self.model.staff_division_id.not_in(exclude_ids),
            self.model.is_active == False
        ).update({self.model.staff_division_id: None})
        db.flush()

    def get_all(self, db: Session, users: list[uuid.UUID]):
        return db.query(self.model).filter(
            self.model.users.any(User.id.in_(users))
        ).all()

    def get_service_staff_functions(self, db: Session, staff_unit_id: uuid.UUID):
        staff_unit = self.get_by_id(db, staff_unit_id)
        return service_staff_function_service.get_by_staff_unit(db, staff_unit)

    def get_document_staff_functions(self, db: Session, staff_unit_id: uuid.UUID):
        staff_unit = self.get_by_id(db, staff_unit_id)
        return document_staff_function_service.get_by_staff_unit(db, staff_unit)

    def has_staff_function(self, db: Session, staff_unit_id: uuid.UUID, staff_function_id: uuid.UUID):
        return db.query(StaffUnit).filter(
            StaffUnit.id == staff_unit_id,
            StaffUnit.staff_functions.any(id=staff_function_id)
        ).first() is not None

    # TODO Нужно закончить реализацию для должностей: пгс, начальники
    def add_document_staff_function_by_position(self, db: Session, body: StaffUnitFunctionsByPosition, role_id: str):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности
        """
        current_user_staff_unit = self.get_by_id(db, role_id)
        current_user_department = staff_division_service.get_department_id_from_staff_division_id(db, current_user_staff_unit.staff_division_id)
        
        if body.position.lower() == 'куратор':
            return self._add_document_staff_function_to_curator(db, current_user_department, body.staff_function_ids)
        elif body.position.lower() == 'прямой начальник':
            return self._add_document_staff_function_to_head_of_department(db, current_user_department, body.staff_function_ids)
        elif body.position.lower() == 'непосредственный начальник':
            return self._add_document_staff_function_to_irrelevant_head(db, current_user_department, body.staff_function_ids)
        else:
            raise BadRequestException('Должность не найдена')

    def _add_document_staff_function_to_curator(self, db: Session, department: uuid.UUID, staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности куратора
        """
        staff_division = staff_division_service.get_by_name(db, StaffDivisionEnum.SERVICE.value)
        
        groups = (
            db.query(StaffDivision)
            .filter(
                StaffDivision.is_active == True,
                StaffDivision.parent_group_id == staff_division.id,
            )
            .all()
        )
        
        if len(groups) == 0:
            raise BadRequestException('В данном подразделении нет кураторов')
        
        for group in groups:
            for staff_unit in group.curators:
                self.add_document_staff_function(db, StaffUnitFunctions(staff_unit_id=staff_unit.id, staff_function_ids=staff_function_ids))

    def _add_document_staff_function_to_head_of_department(self, db: Session, department: uuid.UUID, staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности прямого начальника
        """
        position = position_service.get_id_by_name(db, PositionNameEnum.HEAD_OF_DEPARTMENT.value)
        # Получаем штатную единицу прямого начальника
        staff_unit = db.query(self.model).filter(
            self.model.position_id == position,
            self.model.staff_division_id == department
        ).first()
        
        if staff_unit is None:
            raise BadRequestException('В данном подразделении нет прямого начальника')
        
        # Добавляем должностную функцию прямому начальнику
        return self.add_document_staff_function(db, StaffUnitFunctions(staff_unit_id=staff_unit.id, staff_function_ids=staff_function_ids))

    def _add_document_staff_function_to_irrelevant_head(self, db: Session, department: uuid.UUID, staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности непосредственного начальника
        """
        
        # Получаем список должностей непосредственных начальников
        positions = [
            position_service.get_id_by_name(db, PositionNameEnum.MANAGEMENT_HEAD.value),
            position_service.get_id_by_name(db, PositionNameEnum.HEAD_OF_OTDEL.value)
        ]
        
        staff_units = []
        
        # Получаем список всех дочерных групп
        child_groups = staff_division_service.get_all_child_groups(db, department)
        
        # Получаем список staff unit непосредственных начальников
        for child_group in child_groups:
            staff_unit = db.query(self.model).filter(
                self.model.position_id.in_(positions),
                self.model.staff_division_id == child_group.id
            ).first()
            
            if staff_unit is not None:
                staff_units.append(staff_unit)
        
        if len(staff_units) == 0:
            raise BadRequestException('В данном подразделении нет ни одного начальника')
        
        # Добавляем должностную функцию непосредственным начальникам
        for staff_unit in staff_units:
            self.add_document_staff_function(db, StaffUnitFunctions(staff_unit_id=staff_unit.id, staff_function_ids=staff_function_ids))
    
staff_unit_service = StaffUnitService(StaffUnit)
