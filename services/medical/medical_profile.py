from sqlalchemy.orm import Session

import uuid
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

    def get_by_profile_id(self, db: Session, profile_id: str):
        medical_profile = db.query(self.model).filter(
            self.model.profile_id == profile_id).one()
        # if not medical_profile:
        #     raise NotFoundException(
        #         "Course profile with id: {profile_id} not found!")
        return medical_profile

    def get_liberation_ids(self, db: Session, user_liberation):
        valid_ids = [id for id in user_liberation['liberation_ids'] if self.is_valid_uuid(id)]
        print("Valid ids:",valid_ids)

        if not valid_ids:
            print("No valid liberation IDs found.")
            return []
        liberated_data = db.query(Liberation).filter(
            Liberation.id.in_(user_liberation['liberation_ids'])).all()
        # missing_ids = set(user_liberation['liberation_ids']) - {item.id for item in liberated_data}
        missing_ids = set(valid_ids) - {item.id for item in liberated_data}
        if missing_ids:
            print(f"Missing liberation IDs: {missing_ids}")

        if len(liberated_data) != len(user_liberation['liberation_ids']):
            print("Liberated Data:",liberated_data)
            raise ValueError("Some liberation IDs not found")
        return liberated_data
    
    def is_valid_uuid(self, id_string):
        try:
            uuid.UUID(str(id_string))
            return True
        except ValueError:
            return False


medical_profile_service = MedicalProfileService(MedicalProfile)
