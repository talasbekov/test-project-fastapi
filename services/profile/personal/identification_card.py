from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from typing import Union, Dict, Any
from datetime import datetime

from exceptions.client import NotFoundException
from models import IdentificationCard, PersonalProfile, Profile
from schemas import IdentificationCardCreate, IdentificationCardUpdate
from services.base import ServiceBase


class IdentificationCardService(
        ServiceBase[IdentificationCard,
                    IdentificationCardCreate,
                    IdentificationCardUpdate]):

    def get_by_id(self, db: Session, id: str):
        identification_card = super().get(db, id)
        if identification_card is None:
            raise NotFoundException(
                detail=f"IdentificationCard with id: {id} is not found!")
        return identification_card

    def create(self, db: Session,
               obj_in: Union[IdentificationCardCreate, Dict[str, Any]]) -> IdentificationCard:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_to'] = datetime.strptime(
            obj_in_data['date_to'], '%Y-%m-%d')
        obj_in_data['date_of_issue'] = datetime.strptime(
            obj_in_data['date_of_issue'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_user_id(self, db: Session, user_id: str):
        identification_card = (db.query(IdentificationCard)
                               .join(PersonalProfile)
                               .join(Profile)
                               .filter(Profile.user_id == user_id)
                               .first())

        return identification_card


identification_card_service = IdentificationCardService(IdentificationCard)
