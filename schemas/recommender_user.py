import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class RecommenderUserBase(Model):
    document_link: Optional[str]
    user_by_id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RecommenderUserCreate(RecommenderUserBase):
    pass


class RecommenderUserUpdate(RecommenderUserBase):
    pass


class RecommenderUserRead(RecommenderUserBase, ReadModel):
    pass
