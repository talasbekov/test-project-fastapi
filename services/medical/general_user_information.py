from sqlalchemy.orm import Session
from services import ServiceBase

from exceptions import client
from models.medical import GeneralUserInformation
from schemas.medical import GeneralUserInformationRead,GeneralUserInformationCreate,GeneralUserInformationUpdate

class GeneraUserlInformationService(ServiceBase[GeneralUserInformation,GeneralUserInformationCreate,GeneralUserInformationUpdate]):
    def get_by_id(self,db: Session,id: str):
        general_user_information = super().get(db,id)
        if general_user_information is None:
            raise client.NotFoundException(detail="General user information is not found!")
        return general_user_information
        

general_user_information_service = GeneraUserlInformationService(GeneralUserInformation)
