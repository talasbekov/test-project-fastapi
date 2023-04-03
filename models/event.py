from sqlalchemy import TIMESTAMP, Column, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, UUID

from models import NamedModel


class Event(NamedModel):

    __tablename__ = "events"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    description = Column(TEXT())
    date_since = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
