from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class FamilyRelationBase(NamedModel):
    family_order: int
    pass


class FamilyRelationCreate(FamilyRelationBase):
    pass


class FamilyRelationUpdate(FamilyRelationBase):
    pass


class FamilyRelationRead(FamilyRelationBase, ReadNamedModel):

    class Config:
        orm_mode = True

class FamilyRelationReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[FamilyRelationRead]]