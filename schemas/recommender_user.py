import uuid
from typing import Optional

from pydantic import BaseModel, AnyUrl


class RecommenderUserBase(BaseModel):
    document_link: Optional[str]
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class RecommenderUserCreate(RecommenderUserBase):
    pass


class RecommenderUserUpdate(RecommenderUserBase):
    pass


class RecommenderUserRead(RecommenderUserBase):
    id: Optional[uuid.UUID]
