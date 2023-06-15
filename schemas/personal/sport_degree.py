import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl

from .sport_type import SportTypeRead
from schemas import NamedModel, ReadNamedModel


class SportDegreeBase(NamedModel):
    assignment_date: datetime.date
    sport_type_id: uuid.UUID
    document_link: Optional[AnyUrl]
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SportDegreeCreate(SportDegreeBase):
    pass


class SportDegreeUpdate(SportDegreeBase):
    pass


class SportDegreeRead(SportDegreeBase, ReadNamedModel):
    assignment_date: Optional[datetime.date]
    sport_type_id: Optional[uuid.UUID]
    sport_type: Optional[SportTypeRead]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
