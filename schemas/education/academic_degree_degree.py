import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class AcademicDegreeDegreeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AcademicDegreeDegreeCreate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeUpdate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeRead(AcademicDegreeDegreeBase, ReadNamedModel):
    pass
