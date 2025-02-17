from datetime import datetime
from typing import Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PrivilegeEmergency, FormEnum
from schemas import PrivelegeEmergencyCreate, PrivelegeEmergencyUpdate
from .base import ServiceBase


class PrivelegeEmergencyService(
        ServiceBase[PrivilegeEmergency,
                    PrivelegeEmergencyCreate,
                    PrivelegeEmergencyUpdate]):

    def create(self, db: Session,
               obj_in: Union[PrivelegeEmergencyCreate, Dict[str, Any]]) -> PrivilegeEmergency:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_from'] = datetime.strptime(
            obj_in_data['date_from'], '%Y-%m-%d')
        obj_in_data['date_to'] = datetime.strptime(
            obj_in_data['date_to'], '%Y-%m-%d')
        obj_in_data['form'] = FormEnum[obj_in_data['form']]
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: PrivilegeEmergency,
        obj_in: PrivelegeEmergencyUpdate
    ) -> PrivilegeEmergency:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.form = FormEnum[obj_in.form]
        setattr(db_obj, 'updated_at', datetime.now())
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"PrivilegeEmergency with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        privelege_emergency = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return privelege_emergency

    def get_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        privelege_emergency = db.query(
            self.model).filter(
            self.model.user_id == user_id,
            self.model.date_from <= date_till,
            self.model.date_to <= date_till
        ).first()
        return privelege_emergency


privelege_emergency_service = PrivelegeEmergencyService(PrivilegeEmergency)
