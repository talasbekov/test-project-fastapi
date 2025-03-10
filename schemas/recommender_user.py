from typing import Optional

from schemas import ReadModel


class RecommenderUserBase(ReadModel):
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


class RecommenderUserRead(RecommenderUserBase):
    id: Optional[str]
