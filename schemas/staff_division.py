import datetime
import uuid
from typing import List, Optional, Any

from pydantic import BaseModel, EmailStr, Field, validator

from schemas import (PositionRead, RankRead, StaffFunctionRead,
                     NamedModel, ReadModel, ReadNamedModel,
                     BadgeRead, StatusRead, StaffDivisionTypeRead)


class StaffDivisionBase(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    description: Optional[NamedModel]
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)

class StaffDivisionBaseSchedule(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    # description: Optional[NamedModel]
    # is_combat_unit: Optional[bool] = Field(None, nullable=True)
    # leader_id: Optional[str] = Field(None, nullable=True)
    # is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)

class StaffDivisionBaseMinimized(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)


class StaffDivisionCreate(StaffDivisionBase):
    description: Optional[Any]
    pass


class StaffDivisionUpdate(StaffDivisionBase):
    description: Optional[Any]
    pass


class StaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: str


class UserRead(ReadModel):
    badges: Optional[List[BadgeRead]]
    icon: Optional[str] = Field(None, nullable=True)
    address: Optional[str] = Field(None, nullable=True)
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[str]
    is_military: Optional[bool]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    last_signed_at: Optional[datetime.datetime]
    staff_unit_id: Optional[str]
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

class UserReadSchedule(ReadModel):
    # badges: Optional[List[BadgeRead]]
    icon: Optional[str] = Field(None, nullable=True)
    # address: Optional[str] = Field(None, nullable=True)
    # cabinet: Optional[str]
    # service_phone_number: Optional[str]
    # supervised_by: Optional[str]
    # is_military: Optional[bool]
    # rank: Optional[RankRead]
    # email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    # last_signed_at: Optional[datetime.datetime]
    # staff_unit_id: Optional[str]
    # call_sign: Optional[str]
    # id_number: Optional[str]
    # personal_id: Optional[str]
    # badges: Optional[List[BadgeRead]]
    # date_birth: Optional[datetime.date]
    # iin: Optional[str]
    # statuses: Optional[List[StatusRead]]
    # status_till: Optional[datetime.datetime]

    class Config:
        orm_mode = True

class MatreshkaUserRead(ReadModel):
    icon: Optional[str] = Field(None, nullable=True)
    supervised_by: Optional[str]
    is_military: Optional[bool]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    id_number: Optional[str]
    personal_id: Optional[str]

    class Config:
        orm_mode = True


class HrVacancyRead(ReadModel):
    is_active: Optional[bool]
    staff_unit_id: Optional[str]

    class Config:
        orm_mode = True


class UserReplacingStaffUnitRead(ReadModel):
    position_id: str
    staff_division_id: str
    is_active: Optional[bool] = True
    requirements: Optional[List[dict]]
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
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
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]
    hr_vacancy: Optional[List[Optional[HrVacancyRead]]]
    requirements: Optional[List[dict]]
    staff_functions: Optional[List[StaffFunctionRead]]
    user_replacing: Optional[UserReplacingRead]
    user_replacing_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class StaffUnitReadSchedule(ReadModel):
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
    users: Optional[List[Optional[UserReadSchedule]]]
    # actual_users: Optional[List[Optional[UserRead]]]
    # hr_vacancy: Optional[List[Optional[HrVacancyRead]]]
    # requirements: Optional[List[dict]]
    # staff_functions: Optional[List[StaffFunctionRead]]
    # user_replacing: Optional[UserReplacingRead]
    # user_replacing_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class StaffUnitOptionRead(ReadModel):
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffUnitMatreshkaOptionRead(ReadModel):
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[NamedModel]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
    users: Optional[List[Optional[MatreshkaUserRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffUnitMatreshkaOptionReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[StaffUnitMatreshkaOptionRead]]


# class StaffDivisionRead(StaffDivisionBase, ReadNamedModel):
#     is_combat_unit: Optional[bool] = Field(None, nullable=True)
#     count_vacancies: Optional[int]
#     children: Optional[List['StaffDivisionRead']]
#     staff_units: Optional[List['StaffUnitRead']]
#     type: Optional[StaffDivisionTypeRead]
#
#     class Config:
#         orm_mode = True



class StaffDivisionChildRead(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    id: Optional[str]
    children: Optional[List]
    staff_units: Optional[List]
    type: Optional[StaffDivisionTypeRead]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return []

    class Config:
        orm_mode = True

class StaffDivisionChildReadSchedule(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    # is_combat_unit: Optional[bool] = Field(None, nullable=True)
    # leader_id: Optional[str] = Field(None, nullable=True)
    # is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    id: Optional[str]
    children: Optional[List]
    staff_units: Optional[List]
    # type: Optional[StaffDivisionTypeRead]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return []

    class Config:
        orm_mode = True

class StaffDivisionChildReadMinimized(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    id: Optional[str]
    children: Optional[List]
    type: Optional[StaffDivisionTypeRead]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []
    class Config:
        orm_mode = True


class StaffDivisionRead(StaffDivisionBase):
    id: Optional[str]
    children: Optional[List['StaffDivisionChildRead']]
    staff_units: Optional[List['StaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]
    count_vacancies: Optional[int]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return staff_units

    class Config:
        orm_mode = True

class StaffDivisionReadSchedule(StaffDivisionBaseSchedule):
    id: Optional[str]
    children: Optional[List['StaffDivisionChildReadSchedule']]
    staff_units: Optional[List['StaffUnitReadSchedule']]
    # type: Optional[StaffDivisionTypeRead]
    # count_vacancies: Optional[int]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return staff_units

    class Config:
        orm_mode = True

class StaffDivisionReadMinimized(StaffDivisionBaseMinimized):
    id: Optional[str]
    children: Optional[List['StaffDivisionChildReadMinimized']]
    type: Optional[StaffDivisionTypeRead]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children
    class Config:
        orm_mode = True


class StaffDivisionReadWithoutStaffUnit(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    id: Optional[str]
    type: Optional[StaffDivisionTypeRead]
    count_vacancies: Optional[int]

    class Config:
        orm_mode = True


class StaffDivisionOptionChildRead(ReadNamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    staff_units: Optional[List]
    children: Optional[List]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffDivisionOptionRead(ReadNamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    children: Optional[List[StaffDivisionOptionChildRead]]
    staff_units: Optional[List[StaffUnitOptionRead]]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children

    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return staff_units

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffUnitDivisionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool] = Field(None, nullable=True)

    class Config:
        orm_mode = True


class ShortStaffUnitDivisionRead(ReadNamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)

    class Config:
        orm_mode = True


class StaffDivisionStepChildRead(StaffDivisionBase):
    id: Optional[str]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True


class StaffDivisionStepRead(StaffDivisionBase):
    id: Optional[str]
    children: Optional[List['StaffDivisionStepChildRead']]
    staff_units: Optional[List['StaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True


class StaffDivisionMatreshkaStepChildRead(ReadNamedModel):
    id: Optional[str]
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    type: Optional[StaffDivisionTypeRead]
    name: str
    nameKZ: Optional[str] = Field(None, nullable=True)
    is_parent: Optional[bool]

    class Config:
        orm_mode = True


class StaffDivisionMatreshkaStepRead(ReadNamedModel):
    id: Optional[str]
    children: Optional[List['StaffDivisionMatreshkaStepChildRead']]
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)
    type: Optional[StaffDivisionTypeRead]
    name: str
    nameKZ: Optional[str] = Field(None, nullable=True)
    is_parent: Optional[bool]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children

    class Config:
        orm_mode = True


class StaffDivisionVacancyRead(BaseModel):
    id: Optional[str]
    staff_division_number: Optional[int] = Field(None, nullable=True)
    type: Optional[StaffDivisionTypeRead]
    count_vacancies: Optional[int]
    name: str
    nameKZ: Optional[str] = Field(None, nullable=True)

    class Config:
        orm_mode = True


class StaffDivisionNamedModel(BaseModel):
    id: Optional[str]
    name: str
    nameKZ: Optional[str] = Field(None, nullable=True)
