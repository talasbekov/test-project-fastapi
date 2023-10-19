from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Properties, Profile
from schemas import PropertiesCreate, PropertiesUpdate
from services import profile_service
from services.base import ServiceBase


class PropertiesService(
        ServiceBase[Properties, PropertiesCreate, PropertiesUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Properties with id: {id} is not found!")
        return rank

    def create(self, db: Session, obj_in: PropertiesCreate):
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['purchase_date'] = datetime.strptime(obj_in_data['purchase_date'],
                                                '%Y-%m-%dT%H:%M:%S.%f%z')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(self, db: Session, db_obj: Properties,
               obj_in: PropertiesUpdate):
        return super().update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str):
        return super().delete(db, id)

    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        profile: Profile = profile_service.get_by_user_id(db, user_id)
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with user_id: {user_id} is not found!")

        properties = db.query(self.model).filter(
            self.model.profile_id == profile.additional_profile.id
        ).offset(skip).limit(limit).all()

        return properties


properties_service = PropertiesService(Properties)
