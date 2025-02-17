import uuid
from typing import Optional
from pydantic import validator

from schemas import Model, ReadModel


class RecommenderUserBase(Model):
    document_link: Optional[str]
    recommendant: Optional[str]
    researcher: Optional[str]
    user_by_id: Optional[str]
    researcher_id: Optional[str]
    user_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RecommenderUserCreate(RecommenderUserBase):
    pass


class RecommenderUserUpdate(RecommenderUserBase):
    pass


class RecommenderUserRead(RecommenderUserBase, ReadModel):
    id: Optional[str]

    @validator("user_by_id", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else " "