import uuid
from typing import Optional

from pydantic import BaseModel


class AnthropometricDataBase(BaseModel):
    head_circumference: int
    shoe_size: int
    neck_circumference: int
    shape_size: int
    bust_size: int
    profile_id: uuid.UUID


class AnthropometricDataCreate(AnthropometricDataBase):
    pass


class AnthropometricDataUpdate(AnthropometricDataBase):
    pass


class AnthropometricDataRead(AnthropometricDataBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
