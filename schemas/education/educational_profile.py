import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas.education import (AcademicDegreeRead, AcademicTitleRead,
                               CourseRead, EducationRead,
                               LanguageProficiencyRead)


class EducationalProfileBase(BaseModel):
    profile_id: Optional[uuid.UUID]


class EducationalProfileCreate(EducationalProfileBase):
    pass


class EducationalProfileUpdate(EducationalProfileBase):
    pass


class EducationalProfileRead(EducationalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]

    academic_degree = Optional[List[AcademicDegreeRead]]
    academic_title = Optional[List[AcademicTitleRead]]
    education = Optional[List[EducationRead]]
    course = Optional[List[CourseRead]]
    language_proficiency = Optional[List[LanguageProficiencyRead]]

    class Config:
        orm_mode = True
