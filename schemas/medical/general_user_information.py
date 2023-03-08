import datetime
import uuid

from pydantic import BaseModel

from models.medical.general_user_information import BloodType,AgeGroup

class GeneralUserInformationBase(BaseModel):
    height: int
    blood_group: BloodType
    age_group: AgeGroup
    profile_id: uuid.UUID
 
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class GeneralUserInformationCreate(GeneralUserInformationBase):
    pass


class GeneralUserInformationUpdate(GeneralUserInformationBase):
    pass


class GeneralUserInformationRead(GeneralUserInformationBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
