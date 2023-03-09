import datetime
import uuid

from pydantic import BaseModel


class GeneralUserInformationBase(BaseModel):
    height: int
    blood_group: str
    age_group: int
    profile_id: uuid.UUID
    weight: int
 
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
