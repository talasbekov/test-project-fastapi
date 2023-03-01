import uuid

from sqlalchemy import TEXT, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import TimeBaseModel


class StaffUnit(TimeBaseModel, Base):

    __tablename__ = "staff_units"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=True)
    max_rank_id = Column(UUID(as_uuid=True), ForeignKey("ranks.id"),
                         nullable=True)
