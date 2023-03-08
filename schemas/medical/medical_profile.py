import datetime
import uuid

from pydantic import BaseModel


class MedicalProfileBase(BaseModel):
    profile_id: uuid.UUID


class MedicalProfileCreate(MedicalProfileBase):
    pass


class MedicalProfileUpdate(MedicalProfileBase):
    pass 


class MedicalProfileRead(MedicalProfileBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
