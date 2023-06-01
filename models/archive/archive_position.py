import enum

from sqlalchemy import Column, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel
from models.position import CategoryCodeEnum


class ArchivePosition(NamedModel):

    __tablename__ = "archive_positions"

    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)
    max_rank = relationship("Rank", cascade="all,delete")
    category_code = Column(Enum(CategoryCodeEnum))
    origin_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=True)
