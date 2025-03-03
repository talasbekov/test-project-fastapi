from typing import Optional, List
from pydantic import validator, BaseModel

from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class FamilyRelationBase(NamedModel):
    family_order: Optional[int]

    @validator("family_order", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else 1


class FamilyRelationCreate(FamilyRelationBase):
    pass


class FamilyRelationUpdate(FamilyRelationBase):
    pass


class FamilyRelationRead(FamilyRelationBase, ReadNamedModel):

    class Config:
        orm_mode = True

class FamilyRelationReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[FamilyRelationRead]]