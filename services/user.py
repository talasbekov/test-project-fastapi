import types

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import StaffDivision, User
from schemas import (StaffDivisionUpdate, UserCreate, UserPermission, UserRead,
                     UserUpdate, UserGroupUpdate)
from services import permission_service, staff_division_service

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

    def update_user_group(self,
                          db: Session,
                          body: UserGroupUpdate
                          ) -> User:
        user = self.get_by_id(db, body.user_id)

        staff_division_service.get_by_id(db, body.group_id)

        user.staff_division_id = body.group_id
        db.add(user)
        db.flush()

        return user
    
    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
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



user_service = UserService(User)
