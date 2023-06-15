import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from schemas import (PositionRead, RankRead, StaffFunctionRead,
                    Model, NamedModel, ReadModel, ReadNamedModel,
                    BadgeRead, RankRead, StatusRead, StaffDivisionTypeRead)



class StaffDivisionBase(NamedModel):
    parent_group_id: Optional[uuid.UUID]
    description: Optional[NamedModel]
    is_combat_unit: Optional[bool]
    leader_id: Optional[uuid.UUID]
    is_active: Optional[bool] = True
    type_id: Optional[uuid.UUID] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)


class StaffDivisionCreate(StaffDivisionBase):
    pass


class StaffDivisionUpdate(StaffDivisionBase):
    pass


class StaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: uuid.UUID

class UserRead(ReadModel):
    badges: Optional[List[BadgeRead]]
    icon: Optional[str]
    address: Optional[str]
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[uuid.UUID]
    is_military: Optional[bool]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    last_signed_at: Optional[datetime.datetime]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    personal_id: Optional[str]
    badges: Optional[List[BadgeRead]]
    date_birth: Optional[datetime.date]
    iin: Optional[str]
    statuses: Optional[List[StatusRead]]
    status_till: Optional[datetime.datetime]
    class Config:
        orm_mode = True
        
        
class HrVacancyRead(ReadModel):
    is_active: Optional[bool]
    staff_unit_id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True

class UserReplacingStaffUnitRead(ReadModel):
    position_id: uuid.UUID
    staff_division_id: uuid.UUID
    is_active: Optional[bool] = True
    requirements: Optional[List[dict]]
    staff_division_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]
    hr_vacancy: Optional[List[Optional[HrVacancyRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserReplacingRead(UserRead):
    staff_unit: Optional[UserReplacingStaffUnitRead]
    
    class Config:
        arbitrary_types_allowed = True

class StaffUnitRead(ReadModel):
    staff_division_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]
    hr_vacancy: Optional[List[Optional[HrVacancyRead]]]
    requirements: Optional[List[dict]]
    staff_functions: Optional[List[StaffFunctionRead]]
    user_replacing: Optional[UserReplacingRead]
    user_replacing_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class StaffDivisionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]
    count_vacancies: Optional[int]
    children: Optional[List['StaffDivisionRead']]
    staff_units: Optional[List['StaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True


class StaffDivisionOptionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]
    staff_units: Optional[List[StaffUnitRead]]
    children: Optional[List['StaffDivisionOptionRead']]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffUnitDivisionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]

    class Config:
        orm_mode = True
