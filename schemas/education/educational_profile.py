import uuid
from typing import List, Optional

from pydantic import BaseModel, validator

from .academic_degree import AcademicDegreeRead
from .academic_title import AcademicTitleRead
from .course import CourseRead
from .education import EducationRead
from .language_proficiency import LanguageProficiencyRead
from .. import CustomBaseModel


class EducationalProfileBase(CustomBaseModel):
    profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EducationalProfileCreate(EducationalProfileBase):
    pass


class EducationalProfileUpdate(EducationalProfileBase):
    pass


class EducationalProfileRead(EducationalProfileBase):
    id: Optional[str]
    profile_id: Optional[str]

    academic_degree: Optional[List[AcademicDegreeRead]]
    academic_title: Optional[List[AcademicTitleRead]]
    education: Optional[List[EducationRead]]
    course: Optional[List[CourseRead]]
    language_proficiency: Optional[List[LanguageProficiencyRead]]

    @validator("academic_title", "academic_degree")
    def sort_by_assignment_date(cls, v):
        return sorted(v, key=lambda x: x.assignment_date)
    
    @validator("education", "course")
    def sort_by_end_date(cls, v):
        return sorted(v, key=lambda x: x.end_date)
