import types
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from exceptions import NotFoundException
from models import StaffDivision, User, StaffUnit, Jurisdiction, JurisdictionEnum, DocumentStaffFunction, \
    StaffDivisionEnum
from schemas import (UserCreate, UserUpdate)
from services import (staff_division_service, staff_unit_service, jurisdiction_service, document_staff_function_service)
from .base import ServiceBase

CALLABLES = types.FunctionType, types.MethodType


class UserService(ServiceBase[User, UserCreate, UserUpdate]):

    def get_by_id(self, db: Session, id: str) -> User:

        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")

        return user

    def get_all(self, db: Session, filter: str, skip: int, limit: int) -> List[User]:
        if filter is not None:
            key_words = filter.lower().split()
            users = (
                db.query(self.model)
                .filter((or_(*[func.lower(self.model.first_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(self.model.last_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(self.model.father_name).contains(name) for name in key_words]))
                        )
                .order_by(self.model.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
                )
        else:
            users = super().get_multi(db, skip, limit)

        return users

    def get_all_active(self, db: Session, filter: str, skip: int, limit: int) -> List[User]:
        users = self._get_users_by_filter_is_active(db, filter, skip, limit, True)

        return users

    def get_all_archived(self, db: Session, filter: str, skip: int, limit: int) -> List[User]:
        users = self._get_users_by_filter_is_active(db, filter, skip, limit, False)

        return users

    def get_by_email(self, db: Session, email: str):

        user = db.query(self.model).filter(User.email == email).first()

        return user

    def get_by_call_sign(self, db: Session, call_sign: str):

        user = db.query(self.model).filter(User.call_sign == call_sign).first()

        return user

    def get_by_id_number(self, db: Session, id_number: str):

        user = db.query(self.model).filter(self.model.id_number == id_number).first()

        return user

    def update_user_patch(self, db: Session, id: str, body: UserUpdate) -> User:

        user = self.get_by_id(db, id)

        if body.email is not None:
            user.email = body.email
        if body.first_name is not None:
            user.first_name = body.first_name
        if body.last_name is not None:
            user.last_name = body.last_name
        if body.father_name is not None:
            user.father_name = body.father_name
        if body.icon is not None:
            user.icon = body.icon
        if body.call_sign is not None:
            user.call_sign = body.call_sign
        if body.id_number is not None:
            user.id_number = body.id_number
        if body.phone_number is not None:
            user.phone_number = body.phone_number
        if body.address is not None:
            user.address = body.address
        if body.service_phone_number is not None:
            user.service_phone_number = body.service_phone_number
        if body.cabinet is not None:
            user.cabinet = body.cabinet
        if body.is_military is not None:
            user.is_military = body.is_military
        if body.supervised_by is not None:
            user.supervised_by = body.supervised_by
        if body.personal_id is not None:
            user.personal_id = body.personal_id
        if body.date_birth is not None:
            user.date_birth = body.date_birth
        if body.iin is not None:
            user.iin = body.iin

        db.add(user)
        db.flush()

        return user

    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if
                  (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
        return fields

    def get_by_staff_unit(self, db: Session, staff_unit_id):

        users = db.query(self.model).filter(
            self.model.actual_staff_unit_id == staff_unit_id
        ).all()

        return users
    
    def get_by_iin(self, db: Session, iin: str):

        user = db.query(self.model).filter(
            self.model.iin == iin
        ).first()

        return user

    def get_by_jurisdiction(
            self, db: Session,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ):
        current_user = self.get_by_id(db, user_id)

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, current_user.actual_staff_unit_id)

        document_staff_functions: List[DocumentStaffFunction] = []

        for i in staff_unit.staff_functions:
            document_staff_functions.append(document_staff_function_service.get_by_id(db, i.id))

        jurisdictions: List[Jurisdiction] = []
        for i in document_staff_functions:
            jurisdictions.append(jurisdiction_service.get_by_id(db, i.jurisdiction_id))

        staff_division: StaffDivision = staff_division_service.get_by_id(db, staff_unit.staff_division_id)

        for i in jurisdictions:
            if i.name == JurisdictionEnum.ALL_SERVICE.value:
                return super().get_multi(db, skip=skip, limit=limit)

            if i.name == JurisdictionEnum.PERSONNEL.value:
                return self._get_users_by_personnel_jurisdiction(db, staff_division)

            if i.name == JurisdictionEnum.SUPERVISED_EMPLOYEES.value:
                return db.query(self.model).filter(
                    self.model.supervised_by.isnot(None)
                ).all()

            if i.name == JurisdictionEnum.COMBAT_UNIT.value:
                return self._get_users_by_combat_unit_jurisdiction(db)

            if i.name == JurisdictionEnum.STAFF_UNIT.value:
                return self._get_users_by_staff_unit_jurisdiction(db)

            if i.name == JurisdictionEnum.CANDIDATES.value:
                return self._get_users_by_candidates_jurisdiction(db)

    def _get_users_by_personnel_jurisdiction(self, db: Session, staff_division: StaffDivision) -> List[User]:
        # Получаем все дочерние штатные группы пользователя, включая саму группу
        staff_divisions: List[StaffDivision] = staff_division_service.get_child_groups(db, staff_division.id)
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(staff_unit_service.get_by_staff_division_id(db, i.id))

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_combat_unit_jurisdiction(self, db: Session):
        staff_divisions = db.query(StaffDivision).filter(
            StaffDivision.is_combat_unit == True
        ).all()

        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(i.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_staff_unit_jurisdiction(self, db: Session):
        staff_divisions = db.query(StaffDivision).filter(
            StaffDivision.is_combat_unit == False
        ).all()

        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(i.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_candidates_jurisdiction(self, db: Session):
        staff_division = db.query(StaffDivision).filter(
            StaffDivision.name == StaffDivisionEnum.CANDIDATES.value
        ).first()

        staff_units: List[StaffUnit] = []
        staff_units.extend(staff_division.staff_units)

        users: List[User] = []
        for i in staff_units:
            users.extend(i.actual_users)

        return users

    def _get_users_by_filter_is_active(self, db: Session, filter: str, skip: int, limit: int, is_active: bool)\
            -> List[User]:
        if filter is not None:
            key_words = filter.lower().split()
            users = (
                db.query(self.model)
                .filter((or_(*[func.lower(self.model.first_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(self.model.last_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(self.model.father_name).contains(name) for name in key_words]))
                        )
                .filter(self.model.is_active.is_(is_active))
                .order_by(self.model.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
                )
        else:
            users = (
                db.query(self.model)
                .filter(self.model.is_active.is_(is_active))
                .order_by(self.model.created_at.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )

        return users

user_service = UserService(User)
