from sqlalchemy.orm import Session

from exceptions import client
from models.medical import UserLiberation
from schemas.medical import UserLiberationCreate, UserLiberationUpdate
from services import ServiceBase


class UserLiberationService(
        ServiceBase[UserLiberation, UserLiberationCreate, UserLiberationUpdate]):
    def get_by_id(self, db: Session, id: str):
        user_liberations = super().get(db, id)
        if user_liberations is None:
            raise client.NotFoundException(
                detail="User liberation is not found!")
        return user_liberations


user_liberations_service = UserLiberationService(UserLiberation)
