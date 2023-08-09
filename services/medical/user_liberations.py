from sqlalchemy.orm import Session

from exceptions import client
from models.medical import UserLiberation
from schemas.medical import UserLiberationCreate, UserLiberationUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class UserLiberationService(
        ServiceBase[UserLiberation, UserLiberationCreate, UserLiberationUpdate]):
    def get_by_id(self, db: Session, id: str):
        user_liberations = super().get(db, id)
        if user_liberations is None:
            raise client.NotFoundException(
                detail="User liberation is not found!")
        return user_liberations

    def create(self, db: Session,
            obj_in: Union[UserLiberationCreate, Dict[str, Any]]) -> UserLiberation:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['start_date'] = datetime.strptime(obj_in_data['start_date'], '%Y-%m-%dT%H:%M:%S.%f%z')
        obj_in_data['end_date'] = datetime.strptime(obj_in_data['end_date'], '%Y-%m-%dT%H:%M:%S.%f%z')
        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        db.flush()
        return db_obj

user_liberations_service = UserLiberationService(UserLiberation)
