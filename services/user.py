from sqlalchemy.orm import Session

from .base import ServiceBase

from models import User
from schemas import UserCreate, UserUpdate
from exceptions import NotFoundException


class UserService(ServiceBase[User, UserCreate, UserUpdate]):
    def get_by_id(self, db: Session, id: str):
        user = super().get(db, id)
        if user is None:
            raise NotFoundException(detail="User is not found!")
        
    def get_by_email(self, db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        return user


user_service = UserService(User)
