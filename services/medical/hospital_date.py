from sqlalchemy.orm import Session

from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from exceptions import client
from models.medical import HospitalData
from schemas.medical import HospitalDataCreate, HospitalDataUpdate
from services import ServiceBase


class HospitalDataService(
        ServiceBase[HospitalData, HospitalDataCreate, HospitalDataUpdate]):
    
    def create(self, db: Session,
               obj_in: Union[HospitalDataCreate, Dict[str, Any]]) -> HospitalData:
        obj_in_data = jsonable_encoder(obj_in)
        format_string = "%Y-%m-%dT%H:%M:%S.%f%z"
        start_date = obj_in_data.get('start_date', None)
        if start_date is not None:
            obj_in_data['start_date'] = datetime.strptime(obj_in_data['start_date'], format_string)
        end_date = obj_in_data.get('end_date', None)
        if end_date is not None:
            obj_in_data['end_date'] = datetime.strptime(obj_in_data['end_date'], format_string)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj
    
    
    def get_by_id(self, db: Session, id: str):
        hospital_data = super().get(db, id)
        if hospital_data is None:
            raise client.NotFoundException(
                detail="Hospital data is not found!")
        return hospital_data


hospital_data_service = HospitalDataService(HospitalData)
