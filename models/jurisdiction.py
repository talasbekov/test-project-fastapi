import uuid

from sqlalchemy import Column, String, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import TimeBaseModel


class Jurisdiction(TimeBaseModel, Base):
    __tablename__ = "jurisdictions"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String(150))
