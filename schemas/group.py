import uuid

from pydantic import BaseModel
from typing import Any, Optional, Union



class GroupBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: Optional[str]
    description: Optional[str]


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupRead(GroupBase):
    id: uuid.UUID
    children: Any

    class Config:
        orm_mode = True
