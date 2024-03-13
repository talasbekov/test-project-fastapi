from typing import Optional, List

from schemas import NamedModel, BaseModel, RankRead, ReadModel
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

class PositionTypeUpdate(NamedModel):
    pass

class PositionReadShort(ReadModel):
    id: str
    type: Optional[PositionTypeRead]
    category_code: Optional[str]
    max_rank: Optional[RankRead]

class PositionRead(PositionBase, ReadModel):
    category_code: Optional[str]
    form: Optional[str]
    position_order: Optional[int]
    max_rank_id: Optional[str]
    max_rank: Optional[RankRead]
    name: Optional[str]
    nameKZ: Optional[str]
    type_id: Optional[str]

    @validator('max_rank', always=True)
    def shorten_max_rank(cls, v, values, **kwargs):
        if 'category_code' in values and values['category_code'].startswith('C_RG'):
            v.name = v.name[:-6]
            v.nameKZ = v.nameKZ[:-6]
            return v
        return v
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        max_rank = orm_obj.max_rank
        if orm_obj.category_code.startswith("C_RG"):
            max_rank = max_rank[:-6]
        return cls(
            id=orm_obj.id,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            category_code=orm_obj.category_code,
            form=orm_obj.form,
            position_order=orm_obj.position_order,
            max_rank_id=orm_obj.max_rank_id,
            max_rank=orm_obj.max_rank,
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
            type_id=orm_obj.type_id
        )
    
class PositionPaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[PositionRead]]
