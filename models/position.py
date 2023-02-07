import uuid

from sqlalchemy import Column, TEXT, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True, default=uuid.uuid4)
    description = Column(TEXT, nullable=True)
    permission = relationship("Permission", secondary="position_permission_table",
                              back_populates="positions")
