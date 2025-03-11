from typing import List, Optional, Union
from schemas import Model
from schemas.medical import (AnthropometricDataRead,
                             DispensaryRegistrationRead,
                             GeneralUserInformationRead,
                             HospitalDataRead,
                             UserLiberationRead,
                             GeneralUserInformationRead)


class MedicalProfileBase(Model):
    profile_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MedicalProfileCreate(MedicalProfileBase):
    pass


class MedicalProfileUpdate(MedicalProfileBase):
    pass


class MedicalProfileRead(MedicalProfileBase):
    id: Optional[str]
    general_user_info: Optional[List[GeneralUserInformationRead]]
    dispensary_registrations: Union[Optional[List[DispensaryRegistrationRead]], str]
    anthropometric_datas: Optional[List[AnthropometricDataRead]]
    hospital_datas: Union[Optional[List[HospitalDataRead]], str]
    user_liberations: Union[Optional[List[UserLiberationRead]], str]
    general_user_info: Optional[List[GeneralUserInformationRead]]
