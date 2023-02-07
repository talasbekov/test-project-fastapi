import uuid

from sqlalchemy import Column, text, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"), nullable=True, default=uuid.uuid4)
    description = Column(text, nullable=True)
