import uuid
from typing import List, Optional

from pydantic import BaseModel
from .academic_degree import AcademicDegreeRead
from .academic_title import AcademicTitleRead
from .course import CourseRead
from .education import EducationRead
from .language_proficiency import LanguageProficiencyRead


class EducationalProfileBase(BaseModel):
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EducationalProfileCreate(EducationalProfileBase):
    pass


class EducationalProfileUpdate(EducationalProfileBase):
    pass


class EducationalProfileRead(EducationalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]

    academic_degree: Optional[List[AcademicDegreeRead]]
    academic_title: Optional[List[AcademicTitleRead]]
    education: Optional[List[EducationRead]]
    course: Optional[List[CourseRead]]
    language_proficiency: Optional[List[LanguageProficiencyRead]]

