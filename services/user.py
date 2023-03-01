import datetime
import types
from typing import Optional

from sqlalchemy.orm import Session

from exceptions import InvalidOperationException, NotFoundException
from models import StaffDivision, User
from schemas import (StaffDivisionUpdate, UserCreate, UserGroupUpdate,
                     UserPermission, UserRead, UserServiceFunction, UserUpdate)
from services import (service_function_service, staff_division_service,
                      staff_unit_service)

from .base import ServiceBase

CALLABLES = types.FunctionType, types.MethodType


class UserService(ServiceBase[User, UserCreate, UserUpdate]):

    def get_by_id(self, db: Session, id: str) -> User:

        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")

        return user

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
        if body.staff_division_id is not None:
            user.staff_division_id = staff_division_service.get_by_id(db, body.staff_division_id)
        if body.staff_unit_id is not None:
            user.staff_unit_id = staff_unit_service.get_by_id(db, body.staff_unit_id)
        if body.staff_unit_id is not None:
            user.staff_unit_id = staff_unit_service.get_by_id(db, body.staff_unit_id)
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
        if body.birthday is not None:
            user.birthday = body.birthday
        if body.status is not None:
            user.status = body.status
        if body.status_till is not None:
            user.status_till = body.status_till

        db.add(user)
        db.flush()

        return user

    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if
                  (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
        return fields

    def add_permission(self, db: Session, body: UserPermission):
        user = self.get_by_id(db, body.user_id)

        for id in body.permission_ids:
            permission = permission_service.get_by_id(db, id)
            if permission not in user.permissions:
                user.permissions.append(permission)

        db.add(user)
        db.flush()

    def remove_permission(self, db: Session, body: UserPermission):
        user = self.get_by_id(db, body.user_id)

        for id in body.permission_ids:
            permission = permission_service.get(db, id)
            if permission is None:
                continue
            try:
                user.permissions.remove(permission)
            except ValueError as e:
                continue

        db.add(user)
        db.flush()

    def get_by_staff_unit(self, db: Session, staff_unit_id):

        users = db.query(self.model).filter(
            self.model.actual_staff_unit_id == staff_unit_id
        ).all()

        return users

    def add_service_function(self, db: Session, body: UserServiceFunction):
        user = self.get_by_id(db, body.user_id)

        for id in body.service_function_ids:
            service_function = service_function_service.get_by_id(db, id)
            if service_function not in user.service_functions:
                user.service_functions.append(service_function)

        db.add(user)
        db.flush()

    def remove_service_function(self, db: Session, body: UserServiceFunction):
        user = self.get_by_id(db, body.user_id)

        for id in body.service_function_ids:
            service_function = service_function_service.get(db, id)
            if service_function is None:
                continue
            try:
                user.service_functions.remove(service_function)
            except ValueError as e:
                continue

        db.add(user)
        db.flush()


user_service = UserService(User)
