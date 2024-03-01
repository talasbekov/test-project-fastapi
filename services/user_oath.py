from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models import UserOath
from schemas import UserOathCreate, UserOathUpdate
from .base import ServiceBase



class UserOathService(ServiceBase[UserOath, UserOathCreate, UserOathUpdate]):
    def create(self, db: Session,
               obj_in: Union[UserOathCreate, Dict[str, Any]]) -> UserOath:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date'] = datetime.strptime(
            obj_in_data['date'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj


user_oath_service = UserOathService(UserOath)
