from sqlalchemy.orm import Session

from exceptions import client
from models.medical import UserLiberation
from schemas.medical import UserLiberationsCreate, UserLiberationsUpdate
from services import ServiceBase


class UserLiberationsService(ServiceBase[UserLiberation,UserLiberationsCreate,UserLiberationsUpdate]):
    def get_by_id(self,db: Session,id: str):
        user_liberations = super().get(db,id)
        if user_liberations is None:
            raise client.NotFoundException(detail="Medical profile is not found!")
        return user_liberations
        

user_liberations_service = UserLiberationsService(UserLiberation)
