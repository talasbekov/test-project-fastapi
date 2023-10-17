from datetime import datetime
from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceID
from schemas import ServiceIDCreate, ServiceIDUpdate

from .base import ServiceBase


class ServiceIDService(
        ServiceBase[ServiceID, ServiceIDCreate, ServiceIDUpdate]):

    def create(self, db: Session,
               obj_in: Union[ServiceIDCreate, Dict[str, Any]]) -> ServiceID:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_to'] = datetime.strptime(obj_in_data['date_to'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ServiceID,
        obj_in: ServiceIDUpdate
    ) -> ServiceID:
        obj_data = jsonable_encoder(db_obj)
        if obj_data['date_to']:
            obj_data['date_to'] = datetime.strptime(obj_data['date_to'][:10], '%Y-%m-%d')
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"ServiceID with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        service_id = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return service_id


service_id_service = ServiceIDService(ServiceID)
