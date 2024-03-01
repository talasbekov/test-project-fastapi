from sqlalchemy.orm import Session

from exceptions import client
from models.medical import MedicalProfile, Liberation
from schemas.medical import MedicalProfileCreate, MedicalProfileUpdate
from services import ServiceBase


class MedicalProfileService(
        ServiceBase[MedicalProfile, MedicalProfileUpdate, MedicalProfileCreate]):
    def get_by_id(self, db: Session, id: str):
        medical_profile = super().get(db, id)
        if medical_profile is None:
            raise client.NotFoundException(
                detail="Medical profile is not found!")
        return medical_profile

    def get_liberation_ids(self, db: Session, user_liberation):
        liberated_data = db.query(Liberation).filter(
            Liberation.id.in_(user_liberation['liberation_ids'])).all()
        if len(liberated_data) != len(user_liberation['liberation_ids']):
            raise ValueError("Some liberation IDs not found")
        return liberated_data


medical_profile_service = MedicalProfileService(MedicalProfile)
