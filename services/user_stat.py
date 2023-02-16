from sqlalchemy.orm import Session

from .base import ServiceBase

from models import UserStat
from schemas import UserStatCreate, UserStatUpdate
from exceptions import NotFoundException


class UserStatService(ServiceBase[UserStat, UserStatCreate, UserStatUpdate]):
    def get_by_id(self, db: Session, id: str):
        user_stat = super().get(db, id)
        if user_stat is None:
            raise NotFoundException(detail="Statistics of user is not found!")
        return user_stat


user_stat_service = UserStatService(UserStat)
