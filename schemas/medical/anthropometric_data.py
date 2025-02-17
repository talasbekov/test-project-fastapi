import uuid
from typing import Optional

from pydantic import BaseModel


class AnthropometricDataBase(BaseModel):
    head_circumference: int
    shoe_size: int
    neck_circumference: int
    shape_size: int
    bust_size: int
    profile_id: str


class AnthropometricDataCreate(AnthropometricDataBase):
    pass


class AnthropometricDataUpdate(AnthropometricDataBase):
    pass


class AnthropometricDataRead(AnthropometricDataBase):
    id: Optional[str]
    head_circumference: Optional[int]
    shoe_size: Optional[int]
    neck_circumference: Optional[int]
    shape_size: Optional[int]
    bust_size: Optional[int]
    profile_id: Optional[str]

    class Config:
        orm_mode = True
