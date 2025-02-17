from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PersonalReserve, ReserveEnum
from schemas import PersonnalReserveCreate, PersonnalReserveUpdate
from .base import ServiceBase


class PersonnalReserveService(
        ServiceBase[PersonalReserve, PersonnalReserveCreate, PersonnalReserveUpdate]):
    
    def create(self, db: Session,
               obj_in: Union[PersonnalReserveCreate, Dict[str, Any]]) -> PersonalReserve:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['reserve_date'] = datetime.strptime(
            obj_in_data['reserve_date'], '%Y-%m-%d')
        obj_in_data['reserve'] = ReserveEnum[obj_in_data['reserve']]
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: PersonalReserve,
        obj_in: PersonnalReserveUpdate
    ) -> PersonalReserve:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.reserve = ReserveEnum[obj_in.reserve]
        setattr(db_obj, 'updated_at', datetime.now())
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"PersonalReserve with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        personnal_reserve = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return personnal_reserve

    def get_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        personnal_reserve = db.query(
            self.model).filter(
            self.model.user_id == user_id,
            self.model.reserve_date <= date_till
        ).first()
        return personnal_reserve


personnal_reserve_service = PersonnalReserveService(PersonalReserve)
