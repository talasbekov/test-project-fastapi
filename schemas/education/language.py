from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, Model


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


class LanguageReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[LanguageRead]]