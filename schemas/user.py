import uuid

from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas import BadgeRead, GroupRead, PositionRead, RankRead


class UserBase(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    father_name: Optional[str]
    group_id: uuid.UUID
    position_id: uuid.UUID
    call_sign: str
    id_number: str
    phone_number: Optional[str]
    address: Optional[str]
    birthday: Optional[str]


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID
    badges: List[BadgeRead]
    position: PositionRead
    actual_position: PositionRead
    group: GroupRead
    rank: RankRead

    class Config:
        orm_mode = True
