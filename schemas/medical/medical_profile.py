import uuid

from pydantic import BaseModel
from schemas.medical import (AnthropometricDataRead, DispensaryRegistrationRead, GeneralUserInformationRead,
                             HospitalDataRead, UserLiberationsRead)

from typing import List

class MedicalProfileBase(BaseModel):
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class MedicalProfileCreate(MedicalProfileBase):
    pass


class MedicalProfileUpdate(MedicalProfileBase):
    pass 


class MedicalProfileRead(MedicalProfileBase):
    id: uuid.UUID
    general_user_informations: List[GeneralUserInformationRead]
    dispensary_registrations: List[DispensaryRegistrationRead]
    anthropometric_datas: List[AnthropometricDataRead]
    hospital_datas: List[HospitalDataRead]
    user_liberations: List[UserLiberationsRead]