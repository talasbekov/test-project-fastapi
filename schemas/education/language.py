from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class LanguageBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    pass


class LanguageRead(LanguageBase, ReadNamedModel):
    pass


class LanguageReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[LanguageRead]]