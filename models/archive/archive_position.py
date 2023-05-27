import enum

from sqlalchemy import Column, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class ArchivePosition(NamedModel):

    __tablename__ = "archive_positions"

    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)
    max_rank = relationship("Rank", cascade="all,delete")
    category_code = Column(String, nullable=False)
    origin_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
