import uuid

from pydantic import BaseModel
from typing import List, Dict, Any

class GroupBase(BaseModel):
    parent_group_id: uuid.UUID
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
