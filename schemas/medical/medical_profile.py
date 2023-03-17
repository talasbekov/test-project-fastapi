import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas.medical import (AnthropometricDataRead, DispensaryRegistrationRead, GeneralUserInformationRead,
                             HospitalDataRead, UserLiberationsRead)


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
    id: Optional[uuid.UUID]
    general_user_informations: Optional[List[GeneralUserInformationRead]]
    dispensary_registrations: Optional[List[DispensaryRegistrationRead]]
    anthropometric_datas: Optional[List[AnthropometricDataRead]]
    hospital_datas: Optional[List[HospitalDataRead]]
    user_liberations: Optional[List[UserLiberationsRead]]
