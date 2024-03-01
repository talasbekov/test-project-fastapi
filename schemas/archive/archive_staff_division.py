import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from schemas import NamedModel, StaffDivisionTypeRead, ReadModel, PositionRead
from .archive_staff_unit import ArchiveStaffUnitRead



class ArchiveStaffDivisionBase(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    description: Optional[NamedModel]
    staff_list_id: str
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[str] = Field(None, nullable=True)
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)


class ArchiveStaffDivisionCreate(ArchiveStaffDivisionBase):
    description: Optional[str]
    origin_id: Optional[str]


class ArchiveStaffDivisionUpdate(ArchiveStaffDivisionBase):
    origin_id: Optional[str]


class NewArchiveStaffDivisionCreate(ArchiveStaffDivisionBase):
    pass


class NewArchiveStaffDivisionUpdate(ArchiveStaffDivisionBase):
    pass


class ArchiveStaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: str


# class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
#     id: Optional[str]
#     children: Optional[List['ArchiveStaffDivisionRead']]
#     staff_units: Optional[List['ArchiveStaffUnitRead']]
#     type: Optional[StaffDivisionTypeRead]
#
#     class Config:
#         orm_mode = True

class ArchiveUserReadSchedule(ReadModel):
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


class ArchiveStaffUnitReadSchedule(ReadModel):
    staff_division_id: Optional[str]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
    users: Optional[List[Optional[ArchiveUserReadSchedule]]]
    # actual_users: Optional[List[Optional[UserRead]]]
    # hr_vacancy: Optional[List[Optional[HrVacancyRead]]]
    # requirements: Optional[List[dict]]
    # staff_functions: Optional[List[StaffFunctionRead]]
    # user_replacing: Optional[UserReplacingRead]
    # user_replacing_id: Optional[str]

class ArchiveStaffDivisionBaseSchedule(NamedModel):
    parent_group_id: Optional[str] = Field(None, nullable=True)
    # description: Optional[NamedModel]
    # is_combat_unit: Optional[bool] = Field(None, nullable=True)
    # leader_id: Optional[str] = Field(None, nullable=True)
    # is_active: Optional[bool] = True
    type_id: Optional[str] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)



class ArchiveStaffDivisionReadSchedule(ArchiveStaffDivisionBaseSchedule):
    id: Optional[str]
    children: Optional[List['ArchiveStaffDivisionChildReadSchedule']]
    staff_units: Optional[List['ArchiveStaffUnitReadSchedule']]

    @classmethod
    def update_forward_refs(cls):
        cls.__annotations__['children'] = List[ArchiveStaffDivisionChildReadSchedule]
        cls.__annotations__['staff_units'] = List[ArchiveStaffUnitReadSchedule]
    # type: Optional[StaffDivisionTypeRead]
    # count_vacancies: Optional[int]
        
    @classmethod
    def from_orm(cls, obj):
        return super().from_orm(obj)
    
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

class ArchiveStaffDivisionChildReadSchedule(NamedModel):
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



class ArchiveStaffDivisionChildRead(ArchiveStaffDivisionBase):
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


class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
    id: Optional[str]
    children: Optional[List['ArchiveStaffDivisionChildRead']]
    # staff_units: Optional[List['ArchiveStaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]
    
    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children
        
    # @validator('staff_units')
    # def validate_staff_units(cls, staff_units):
    #     if staff_units == []:
    #         return None
    #     else:
    #         return staff_units

    class Config:
        orm_mode = True

class ArchiveStaffDivisionReadSecond(ArchiveStaffDivisionBase):
    id: Optional[str]
    children: Optional[List['ArchiveStaffDivisionChildRead']]
    staff_units: Optional[List['ArchiveStaffUnitReadSchedule']]
    type: Optional[StaffDivisionTypeRead]
    
    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children
        
    # @validator('staff_units')
    # def validate_staff_units(cls, staff_units):
    #     if staff_units == []:
    #         return None
    #     else:
    #         return staff_units

    class Config:
        orm_mode = True

class ArchiveStaffDivisionStepChildRead(ArchiveStaffDivisionBase):
    id: Optional[str]
    type: Optional[StaffDivisionTypeRead]
    description: Optional[NamedModel]

    class Config:
        orm_mode = True

class ArchiveStaffDivisionStepRead(ArchiveStaffDivisionBase):
    id: Optional[str]
    children: Optional[List['ArchiveStaffDivisionStepChildRead']]
    staff_units: Optional[List['ArchiveStaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True
