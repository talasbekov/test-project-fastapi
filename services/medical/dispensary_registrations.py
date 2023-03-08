from sqlalchemy.orm import Session
from services import ServiceBase

from exceptions import client
from models.medical import DispensaryRegistration
from schemas.medical import DispensaryRegistrationCreate,DispensaryRegistrationRead,DispensaryRegistrationUpdate

class DispensaryRegistrationService(ServiceBase[DispensaryRegistration,DispensaryRegistrationUpdate,DispensaryRegistrationUpdate]):
    def get_by_id(self,db: Session,id: str):
        dispensary_registration = super().get(db,id)
        if dispensary_registration is None:
            raise client.NotFoundException(detail="Dispensary registration is not found!")
        return dispensary_registration
        

dispensary_registration_service = DispensaryRegistrationService(DispensaryRegistration)
