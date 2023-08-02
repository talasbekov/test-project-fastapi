from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TEXT

from models import NamedModel


class Event(NamedModel):

    __tablename__ = "events"

    user_id = Column(String(), ForeignKey("users.id"))
    description = Column(TEXT())
    date_since = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
