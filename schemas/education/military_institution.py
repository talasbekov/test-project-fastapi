from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class MilitaryInstitutionBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MilitaryInstitutionCreate(MilitaryInstitutionBase):
    pass


class MilitaryInstitutionUpdate(MilitaryInstitutionBase):
    pass


class MilitaryInstitutionRead(MilitaryInstitutionBase, ReadNamedModel):
    pass

class MilitaryInstitutionReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[MilitaryInstitutionRead]]