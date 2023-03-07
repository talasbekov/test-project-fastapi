from pydantic import BaseModel
import uuid


class AdditionalProfileBase(BaseModel):
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AdditionalProfileCreate(AdditionalProfileBase):
    pass


class AdditionalProfileUpdate(AdditionalProfileBase):
    pass


class AdditionalProfileRead(AdditionalProfileBase):
    id: uuid.UUID
    profile_id: uuid.UUID

    

