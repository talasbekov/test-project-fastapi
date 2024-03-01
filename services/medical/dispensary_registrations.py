from sqlalchemy.orm import Session

from exceptions import client
from models.medical import DispensaryRegistration
from schemas.medical import DispensaryRegistrationUpdate
from services import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class DispensaryRegistrationService(
        ServiceBase[DispensaryRegistration,
                    DispensaryRegistrationUpdate,
                    DispensaryRegistrationUpdate]):
    def get_by_id(self, db: Session, id: str):
        dispensary_registration = super().get(db, id)
        if dispensary_registration is None:
            raise client.NotFoundException(
                detail="Dispensary registration is not found!")
        return dispensary_registration

    def create(self, db: Session,
            obj_in: Union[DispensaryRegistrationUpdate, Dict[str, Any]]) -> DispensaryRegistration:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data['start_date'] is not None:
            obj_in_data['start_date'] = datetime.strptime(obj_in_data['start_date'],
                                                          '%Y-%m-%dT%H:%M:%S.%f%z')
        if obj_in_data['end_date'] is not None:
            obj_in_data['end_date'] = datetime.strptime(obj_in_data['end_date'],
                                                        '%Y-%m-%dT%H:%M:%S.%f%z')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

dispensary_registration_service = DispensaryRegistrationService(
    DispensaryRegistration)
