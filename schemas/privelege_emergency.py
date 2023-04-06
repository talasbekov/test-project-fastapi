import uuid
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class PrivelegeEmergency(BaseModel):
    form: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PrivelegeEmergencyCreate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyUpdate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyRead(PrivelegeEmergency):

    id: Optional[uuid.UUID] 

     
