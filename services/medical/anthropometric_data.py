from sqlalchemy.orm import Session
from services import ServiceBase

from exceptions import client
from models.medical import AnthropometricData
from schemas.medical import AnthropometricDataCreate,AnthropometricDataRead,AnthropometricDataUpdate

class AnthropometricDataService(ServiceBase[AnthropometricData,AnthropometricDataUpdate,AnthropometricDataCreate]):
    def get_by_id(self,db: Session,id: str):
        anthropometric_data = super().get(db,id)
        if anthropometric_data is None:
            raise client.NotFoundException(detail="Anthropometric data is not found!")
        return anthropometric_data
        

anthropometric_data_service = AnthropometricDataService(AnthropometricData)
