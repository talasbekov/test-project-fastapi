from sqlalchemy.orm import Session

from .base import ServiceBase

from models import UserStat
from schemas import UserStatCreate, UserStatUpdate
from exceptions import NotFoundException


class UserStatService(ServiceBase[UserStat, UserStatCreate, UserStatUpdate]):
    def get_by_id(self, db: Session, id: str):
        userstat = super().get(db, id)
        if userstat is None:
            raise NotFoundException(detail="Statistics of user is not found!")


user_stat_service = UserStatService(UserStat)
