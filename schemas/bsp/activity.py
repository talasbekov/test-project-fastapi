import uuid
from typing import Optional, List

from pydantic import validator

from schemas import NamedModel


class ActivityBase(NamedModel):
    parent_group_id: Optional[uuid.UUID]
    instructions: Optional[dict]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass


class ActivityChildRead(ActivityBase):
    id: Optional[uuid.UUID]
    children: Optional[List]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []

    class Config:
        orm_mode = True


class ActivityRead(ActivityBase):
    id: Optional[uuid.UUID]
    children: Optional[List['ActivityChildRead']]

    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children
