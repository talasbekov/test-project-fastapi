import types

from sqlalchemy.orm import Session

from .base import ServiceBase

from models import User, Group
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

        user = db.query(User).filter(User.email == email).first()

        return user

    def update_user_group(self,
                          db: Session,
                          id: str,
                          group_id: str,
                          ) -> User:
        user = self.get_by_id(db, id)

        group = db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise NotFoundException(detail="Group is not found!")

        user.group_id = group_id
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_fields(self):
        fields = [key for key, value in User.__dict__.items() if (not 'id' in key and not isinstance(value, CALLABLES) and not key.startswith('_'))]
        return fields



user_service = UserService(User)
