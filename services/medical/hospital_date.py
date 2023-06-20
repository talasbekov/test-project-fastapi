from sqlalchemy.orm import Session

from exceptions import client
from models.medical import HospitalData
from schemas.medical import HospitalDataCreate, HospitalDataUpdate
from services import ServiceBase


class HospitalDataService(
        ServiceBase[HospitalData, HospitalDataCreate, HospitalDataUpdate]):
    def get_by_id(self, db: Session, id: str):
        hospital_data = super().get(db, id)
        if hospital_data is None:
            raise client.NotFoundException(
                detail="Hospital data is not found!")
        return hospital_data


hospital_data_service = HospitalDataService(HospitalData)
