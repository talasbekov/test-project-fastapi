import uuid

from pydantic import BaseModel
from typing import Any, Optional, Union


class GroupBase(BaseModel):
    parent_group_id: Union[uuid.UUID, None]
    name: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: uuid.UUID
    children: Any

    class Config:
        orm_mode = True
