import uuid

from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from core import Base


class Rank(Base):

    __tablename__ = "ranks"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)