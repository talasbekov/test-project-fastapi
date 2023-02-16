import types

from sqlalchemy.orm import Session

from .base import ServiceBase

from models import User, Group
from services import group_service
from schemas import UserCreate, UserUpdate, UserRead, GroupUpdate
from exceptions import NotFoundException

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
                          id: str,
                          group_id: str,
                          ) -> User:
        user = self.get_by_id(db, id)

        group_service.get_by_id(db, group_id)

        user.group_id = group_id
        db.add(user)
        db.flush()

        return user
    
    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
        return fields



user_service = UserService(User)
