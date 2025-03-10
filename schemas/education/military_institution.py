from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, Model


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

class MilitaryInstitutionReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[MilitaryInstitutionRead]]