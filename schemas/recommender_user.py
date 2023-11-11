import uuid
from typing import Optional

from schemas import Model, ReadModel


class RecommenderUserBase(Model):
    document_link: Optional[str]
    recommendant: Optional[str]
    researcher: Optional[str]
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
