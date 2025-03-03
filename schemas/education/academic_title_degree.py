from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class AcademicTitleDegreeBase(NamedModel):
    pass


class AcademicTitleDegreeCreate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeUpdate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeRead(AcademicTitleDegreeBase, ReadNamedModel):

    class Config:
        orm_mode = True
        

class AcademicTitleDegreeReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[AcademicTitleDegreeRead]]
