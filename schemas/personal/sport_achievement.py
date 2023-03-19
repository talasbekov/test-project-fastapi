import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel

from .sport_type import SportTypeRead


class SportAchievementBase(BaseModel):
    name: str
    assignment_date: datetime.date
    sport_type_id: uuid.UUID
    document_link: AnyUrl
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



class SportAchievementCreate(SportAchievementBase):
    pass


class SportAchievementUpdate(SportAchievementBase):
    pass


class SportAchievementRead(SportAchievementBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    assignment_date: Optional[datetime.date]
    sport_type_id: Optional[uuid.UUID]
    sport_type: Optional[SportTypeRead]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]
