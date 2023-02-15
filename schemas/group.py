import uuid

from pydantic import BaseModel
from typing import Any, Optional, Union, List, ForwardRef


class GroupBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    description: Optional[str]


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    children: Optional[List['GroupRead']]

    class Config:
        orm_mode = True
