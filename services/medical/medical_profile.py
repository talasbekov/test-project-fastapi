from sqlalchemy.orm import Session

from exceptions import client
from models.medical import MedicalProfile
from schemas.medical import MedicalProfileCreate, MedicalProfileUpdate
from services import ServiceBase


class MedicalProfileService(ServiceBase[MedicalProfile,MedicalProfileUpdate,MedicalProfileCreate]):
    def get_by_id(self,db: Session,id: str):
        medical_profile = super().get(db,id)
        if medical_profile is None:
            raise client.NotFoundException(detail="Medical profile is not found!")
        return medical_profile
        

medical_profile_service = MedicalProfileService(MedicalProfile)
