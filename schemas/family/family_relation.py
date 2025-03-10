from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, Model


class FamilyRelationBase(NamedModel):
    family_order: Optional[int]


class FamilyRelationCreate(FamilyRelationBase):
    pass


class FamilyRelationUpdate(FamilyRelationBase):
    pass


class FamilyRelationRead(FamilyRelationBase, ReadNamedModel):

    class Config:
        orm_mode = True


class FamilyRelationReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[FamilyRelationRead]]