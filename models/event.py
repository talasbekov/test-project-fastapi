import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.orm import relationship, backref

from core import Base


class Event(Base):

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(String(255))
    desciption = Column(TEXT())
    date_since = Column(TIMESTAMP(timezone=True))
    date_to = Column(TIMESTAMP(timezone=True))
