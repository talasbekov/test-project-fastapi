import uuid
from typing import Optional, List

from schemas import NamedModel, RankRead, ReadModel, CustomBaseModel
from pydantic import BaseModel, validator

class PositionBase(NamedModel):
    category_code: str
    form: str
    max_rank_id: Optional[str]

    # make category_code uppercase
    @validator('category_code')
    def category_code_to_upper(cls, v):
        if v is not None:
            return v.upper()
        return
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PositionCreate(PositionBase):
    type_id: Optional[str]
    position_order: Optional[int]

class PositionUpdate(PositionBase):
    position_order: Optional[int]

class PositionTypeRead(NamedModel):
    pass

class PositionReadShort(ReadModel):
    id: str
    type: Optional[PositionTypeRead]
    category_code: Optional[str]
    max_rank: Optional[RankRead]

class PositionRead(PositionBase, ReadModel):
    id: Optional[str]
    category_code: Optional[str]
    form: Optional[str]
    position_order: Optional[int]
    max_rank_id: Optional[str]
    max_rank: Optional[RankRead]
    name: Optional[str]
    nameKZ: Optional[str]

    @validator("id", pre=True, always=True)
    def default_uuid(cls, v):
        return v if v is not None else str(uuid.uuid4())

    @validator("category_code", "form", "name", "nameKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("position_order", pre=True, always=True)
    def default_int(cls, v):
        return v if v is not None else 999999

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    
class PositionPaginationRead(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[PositionRead]]
