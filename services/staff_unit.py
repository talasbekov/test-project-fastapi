import datetime
import uuid
import json

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from exceptions.client import BadRequestException, NotFoundException
from models import (StaffUnit, Position, User, EmergencyServiceHistory,
                    ArchiveStaffUnit,
                    StaffDivision, PositionNameEnum, StaffDivisionEnum, PositionType, Rank)
from schemas import (StaffUnitCreate, StaffUnitUpdate,
                     StaffUnitFunctions, StaffUnitRead,
                     StaffUnitCreateWithPosition, StaffUnitFunctionsByPosition,
                     StaffUnitMatreshkaOptionRead, StaffUnitFromArchiveCreate
                     )
from services import (service_staff_function_service,
                      document_staff_function_service,
                      staff_division_service, position_service)
from .base import ServiceBase


class StaffUnitService(
        ServiceBase[StaffUnit, StaffUnitCreate, StaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(
                detail=f"StaffUnit  with position id: {id} is not found!")
        if isinstance(position.requirements, str):
            position.requirements = json.loads(position.requirements)
        if isinstance(position.staff_division.description, str):
            position.staff_division.description = json.loads(position.staff_division.description)
        return position
    
    def get_by_staff_division_id(self, db: Session, id: str):
        stmt = select(StaffUnit).where(StaffUnit.staff_division_id == id)
        staff_unit = db.execute(stmt).first()
        if staff_unit is None:
            raise NotFoundException(
                detail=f"StaffUnit within staff_division with id: {id} is not found!")
        else:
            staff_unit = staff_unit[0]
            
        if isinstance(staff_unit.requirements, str):
            staff_unit.requirements = json.loads(staff_unit.requirements)
        if isinstance(staff_unit.staff_division.description, str):
            staff_unit.staff_division.description = json.loads(staff_unit.staff_division.description)
        return staff_unit

    def create_with_position(self, db: Session,
                             staff_unit_with_position: StaffUnitCreateWithPosition):

        position = Position(type_id=staff_unit_with_position.type_id,
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
        for staff_unit in staff_units:
            if staff_unit.requirements:
                staff_unit.requirements = json.loads(staff_unit.requirements)
        return {'total': total, 'objects': staff_units}

    def add_service_staff_function(
            self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)

        for id in body.staff_function_ids:
            staff_function = service_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_service_staff_function(
            self, db: Session, body: StaffUnitFunctions):
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

    def add_document_staff_function(
            self, db: Session, body: StaffUnitFunctions):
        staff_unit = self.get_by_id(db, body.staff_unit_id)
        
        if isinstance(staff_unit.staff_division.description, dict):
            staff_unit.staff_division.description = (
                json.dumps(staff_unit.staff_division.description)
            )
        if isinstance(staff_unit.requirements, list):
            staff_unit.requirements = json.dumps(staff_unit.requirements)

        for id in body.staff_function_ids:
            staff_function = document_staff_function_service.get_by_id(db, id)
            if staff_function not in staff_unit.staff_functions:
                staff_unit.staff_functions.append(staff_function)

        db.add(staff_unit)
        db.flush()

    def remove_document_staff_function(
            self, db: Session, body: StaffUnitFunctions):
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

    def get_by_option(self, db: Session,
                      type: str, id: str, skip: int, limit: int):
        staff_units = super().get_multi(db, skip, limit)
        return [StaffUnitRead.from_orm(item).dict() for item in staff_units]

    def create_relation(self, db: Session, user: User,
                        staff_unit_id: str):
        staff_unit = self.get_by_id(db, staff_unit_id)
        if isinstance(staff_unit.staff_division.description, dict):
            staff_unit.staff_division.description = json.dumps(staff_unit.staff_division.description)
        if isinstance(staff_unit.requirements, list):
            staff_unit.requirements = json.dumps(staff_unit.requirements)
        db.execute(text(f"UPDATE HR_ERP_USERS SET staff_unit_id = '{staff_unit.id}' WHERE id = '{user.id}'"))
        db.add(staff_unit)
        db.flush()
        return staff_unit

    def exists_relation(self, db: Session, user_id: str,
                        staff_unit_id: str):
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
            position = db.query(Position).join(PositionType).filter(PositionType.name == name).first()
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

    def _get_free_by_staff_division_id(
            self, db: Session, staff_division_id: str):
        return (
            db.query(self.model)
            .filter(
                self.model.staff_division_id == staff_division_id,
                self.model.users == None
            )
            .first())

    def get_last_history(self, db: Session, user_id: str):
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
                            staff_division_id: str):
        res = super().create(
            db, StaffUnitFromArchiveCreate(
                position_id=archive_staff_unit.position_id,
                staff_division_id=staff_division_id,
                curator_of_id=archive_staff_unit.curator_of_id,
                is_active=True,
                user_replacing_id=archive_staff_unit.user_replacing_id,
                requirements=archive_staff_unit.requirements
            )
        )
        return res

    def update_from_archive(self, db: Session, archive_staff_unit: ArchiveStaffUnit,
                            staff_division_id: str):
        staff_unit = self.get_by_id(db, archive_staff_unit.origin_id)
        res = self._update(
            db,
            db_obj=staff_unit,
            obj_data=staff_unit.__dict__,
            obj_in=StaffUnitUpdate(
                position_id=archive_staff_unit.position_id,
                curator_of_id=archive_staff_unit.curator_of_id,
                staff_division_id=staff_division_id,
                is_active=True,
                user_replacing_id=archive_staff_unit.user_replacing_id,
                requirements=archive_staff_unit.requirements
            )
        )
        return res

    def create_or_update_from_archive(self, db: Session,
                                      archive_staff_unit: ArchiveStaffUnit,
                                      staff_division_id: str):
        if archive_staff_unit.origin_id is None:
            return self.create_from_archive(
                db, archive_staff_unit, staff_division_id)
        return self.update_from_archive(
            db, archive_staff_unit, staff_division_id)

    def make_all_inactive(self, db: Session,
                          exclude_ids: list[str] = []):
        (db.query(self.model)
         .filter(
            self.model.staff_division_id.not_in(exclude_ids)
        )
            .update({self.model.is_active: False}))
        db.flush()

    def delete_all_inactive(self, db: Session,
                            exclude_ids: list[str] = []):
        db.query(self.model).filter(
            self.model.staff_division_id.not_in(exclude_ids),
            self.model.is_active == False
        ).update({self.model.staff_division_id: None})
        db.flush()

    def get_all(self, db: Session, users: list[str]):
        return db.query(self.model).filter(
            self.model.users.any(User.id.in_(users))
        ).all()

    def get_service_staff_functions(
            self, db: Session, staff_unit_id: str):
        staff_unit = self.get_by_id(db, staff_unit_id)
        return service_staff_function_service.get_by_staff_unit(db, staff_unit)

    def get_document_staff_functions(
            self, db: Session, staff_unit_id: str):
        staff_unit = self.get_by_id(db, staff_unit_id)
        return document_staff_function_service.get_by_staff_unit(
            db, staff_unit)

    def has_staff_function(self,
                           db: Session,
                           staff_unit_id: str,
                           staff_function_id: str):
        return db.query(StaffUnit).filter(
            StaffUnit.id == staff_unit_id,
            StaffUnit.staff_functions.any(id=staff_function_id)
        ).first() is not None

    # TODO Нужно закончить реализацию для должностей: пгс, начальники
    def add_document_staff_function_by_position(self,
                                                db: Session,
                                                body: StaffUnitFunctionsByPosition,
                                                role_id: str):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности
        """
        current_user_staff_unit = self.get_by_id(db, role_id)
        current_user_department = (staff_division_service
                                   .get_department_id_from_staff_division_id(db,
                                                                             current_user_staff_unit.staff_division_id))

        if body.position.lower() == 'куратор':
            return self._add_document_staff_function_to_curator(db,
                                                                current_user_department,
                                                                body.staff_function_ids)
        elif body.position.lower() == 'прямой начальник':
            return self._add_document_staff_function_to_head_of_department(db,
                                                                           current_user_department,
                                                                           body.staff_function_ids)
        elif body.position.lower() == 'непосредственный начальник':
            return self._add_document_staff_function_to_irrelevant_head(db,
                                                                        current_user_department,
                                                                        body.staff_function_ids)
        elif body.position.lower() == 'пгс':
            return self._add_document_staff_function_to_pgs(db,
                                                            current_user_department,
                                                            body.staff_function_ids)
        elif body.position.lower() == 'все сотрудники':
            return self._add_document_staff_function_to_all(db,
                                                            current_user_department,
                                                            body.staff_function_ids)
        else:
            raise BadRequestException('Должность не найдена')

    def _update(
        self,
        db: Session,
        *,
        db_obj: StaffUnit,
        obj_data: dict,
        obj_in: StaffUnitUpdate
    ) -> StaffUnit:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj
    
    def _add_document_staff_function_to_curator(self,
                                                db: Session,
                                                department: str,
                                                staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию
            в штатную единицу по должности куратора
        """
        staff_division = staff_division_service.get_by_name(db,
                                                            StaffDivisionEnum.SERVICE.value)

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
                self.add_document_staff_function(db,
                                                 StaffUnitFunctions(staff_unit_id=staff_unit.staff_unit.id,
                                                                    staff_function_ids=staff_function_ids))

    def _add_document_staff_function_to_head_of_department(self,
                                                           db: Session,
                                                           department: str,
                                                           staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию
            в штатную единицу по должности прямого начальника
        """
        head_of_department = PositionNameEnum.HEAD_OF_DEPARTMENT.value
        position = position_service.get_id_by_name_like(db, head_of_department)
        # Получаем штатную единицу прямого начальника
        staff_unit = db.query(self.model).filter(
            self.model.position_id == position,
            self.model.staff_division_id == department
        ).first()

        if staff_unit is None:
            raise BadRequestException(
                'В данном подразделении нет прямого начальника')

        # Добавляем должностную функцию прямому начальнику
        return self.add_document_staff_function(db,
                                                StaffUnitFunctions(staff_unit_id=staff_unit.id,
                                                                   staff_function_ids=staff_function_ids))

    def _add_document_staff_function_to_irrelevant_head(self,
                                                        db: Session,
                                                        department: str,
                                                        staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию в штатную единицу по должности
            непосредственного начальника
        """

        # Получаем список должностей непосредственных начальников
        positions = [
            position_service.get_id_by_name_like(
                db, PositionNameEnum.MANAGEMENT_HEAD.value),
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_OTDEL.value),
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_DEPARTMENT.value),
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_SERVICE.value)
        ]

        staff_units = []

        # Получаем список всех дочерных групп
        child_groups = staff_division_service.get_all_child_groups(
            db, department)

        # Получаем список staff unit непосредственных начальников
        for child_group in child_groups:
            staff_unit = db.query(self.model).filter(
                self.model.position_id.in_(positions),
                self.model.staff_division_id == child_group.id
            ).first()

            if staff_unit is not None:
                staff_units.append(staff_unit)

        if len(staff_units) == 0:
            raise BadRequestException(
                'В данном подразделении нет ни одного начальника')

        # Добавляем должностную функцию непосредственным начальникам
        for staff_unit in staff_units:
            staff_functions = StaffUnitFunctions(staff_unit_id=staff_unit.id,
                                                 staff_function_ids=staff_function_ids)
            self.add_document_staff_function(db, staff_functions)

    # def _add_document_staff_function_to_all_heads(self,
    #                                                     db: Session,
    #                                                     department: str,
    #                                                     staff_function_ids: list):
    #     """
    #         Эта функция добавляет должностную функцию в штатную единицу по должности
    #         непосредственного начальника
    #     """
    #
    #     # Получаем список должностей непосредственных начальников
    #     positions = [
    #         position_service.get_id_by_name_like(
    #             db, PositionNameEnum.MANAGEMENT_HEAD.value),
    #         position_service.get_id_by_name_like(
    #             db, PositionNameEnum.HEAD_OF_OTDEL.value),
    #         position_service.get_id_by_name_like(
    #             db, PositionNameEnum.HEAD_OF_DEPARTMENT.value),
    #         position_service.get_id_by_name_like(
    #             db, PositionNameEnum.HEAD_OF_SERVICE.value)
    #     ]
    #
    #     staff_units = []
    #
    #     # Получаем список всех дочерных групп
    #     child_groups = staff_division_service.get_all_child_groups(
    #         db, department)
    #
    #     # Получаем список staff unit непосредственных начальников
    #     for child_group in child_groups:
    #         staff_unit = db.query(self.model).filter(
    #             self.model.position_id.in_(positions),
    #             self.model.staff_division_id == child_group.id
    #         ).first()
    #
    #         if staff_unit is not None:
    #             staff_units.append(staff_unit)
    #
    #     if len(staff_units) == 0:
    #         raise BadRequestException(
    #             'В данном подразделении нет ни одного начальника')
    #
    #     # Добавляем должностную функцию непосредственным начальникам
    #     for staff_unit in staff_units:
    #         staff_functions = StaffUnitFunctions(staff_unit_id=staff_unit.id,
    #                                              staff_function_ids=staff_function_ids)
    #         self.add_document_staff_function(db, staff_functions)

    def _add_document_staff_function_to_pgs(self,
                                            db: Session,
                                            department: str,
                                            staff_function_ids: list):
        """
            Эта функция добавляет должностную функцию
            в штатную единицу по должности пгс
        """
        positions = [
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_SERVICE.value),
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_SERVICE_INSTEAD.value),
            position_service.get_id_by_name_like(
                db, PositionNameEnum.HEAD_OF_SERVICE_SHORT.value),
        ]
        # Получаем штатную единицу пгс
        staff_units = db.query(self.model).filter(
            self.model.position_id.in_(positions),
            self.model.staff_division_id == department
        ).all()

        if staff_units is None:
            raise BadRequestException(
                'В данном подразделении нет Политического гос. служащего')

        # Добавляем должностную функцию пгс
        for staff_unit in staff_units:
            staff_functions = StaffUnitFunctions(staff_unit_id=staff_unit.id,
                                                 staff_function_ids=staff_function_ids)
            self.add_document_staff_function(db, staff_functions)

    def _add_document_staff_function_to_all(self,
                                            db: Session,
                                            department: str,
                                            staff_function_ids: list):
    
        # Получаем штатную единицу пгс
        staff_units = db.query(self.model).all()

        if staff_units is None:
            raise BadRequestException(
                'ай ай ай стафф юнитов не существует вообще че делать???')

        # Добавляем должностную функцию пгс
        for staff_unit in staff_units:
            staff_functions = StaffUnitFunctions(staff_unit_id=staff_unit.id,
                                                 staff_function_ids=staff_function_ids)
            self.add_document_staff_function(db, staff_functions)

    def _add_filter_to_query(self, staff_unit_query, filter):
        key_words = filter.lower().split()
        staff_units = (
            staff_unit_query
            .join(StaffUnit.users)
            .filter(
                and_(func.concat(func.concat(func.concat(func.lower(User.first_name), ' '),
                                             func.concat(func.lower(User.last_name), ' ')),
                                 func.lower(User.father_name))
                     .contains(name) for name in key_words)
            )
        )
        return staff_units

    def update_staff_unit(self, db: Session, staff_division_id: str, staff_unit_id: str, postion_id: str, actual_position_id: str, rank_id: str, user: User):
        staff_unit = db.query(StaffUnit).filter(StaffUnit.id == staff_unit_id).first()
        if postion_id is not None:
            position = db.query(Position).filter(Position.id == postion_id).first()
            if position:
                staff_unit.position_id = postion_id
        if actual_position_id is not None:
            position = db.query(Position).filter(Position.id == actual_position_id).first()
            if position:
                staff_unit.actual_position_id = actual_position_id
        if staff_division_id is not None:
            staff_division = db.query(StaffDivision).filter(StaffDivision.id == staff_division_id).first()
            if staff_division:      
                staff_unit.staff_division_id = staff_division_id
        staff_unit.updated_at = datetime.datetime.now()
        # setattr(staff_unit, 'updated_at', datetime.datetime.now())
        rank = db.query(Rank).filter(Rank.id == rank_id).first()
        if rank:
            setattr(user, 'rank_id', rank_id)
            setattr(user, 'updated_at', datetime.datetime.now())
        db.add(staff_unit)
        db.add(user)
        db.flush()
        return "success"

staff_unit_service = StaffUnitService(StaffUnit)
