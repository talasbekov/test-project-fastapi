from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


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


class AcademicDegreeDegreeReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[AcademicDegreeDegreeRead]]