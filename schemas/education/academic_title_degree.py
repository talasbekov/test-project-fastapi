from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class AcademicTitleDegreeBase(NamedModel):
    pass


class AcademicTitleDegreeCreate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeUpdate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeRead(AcademicTitleDegreeBase, ReadNamedModel):

    class Config:
        orm_mode = True
        

class AcademicTitleDegreeReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[AcademicTitleDegreeRead]]
