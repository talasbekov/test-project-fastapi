from typing import Optional, List

from schemas import NamedModel, ReadNamedModel


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


class LanguageReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[LanguageRead]]