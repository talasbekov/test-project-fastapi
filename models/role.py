import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class RoleName(enum.Enum):
    AGREER = 1
    EXPERT = 2
    APPROVER = 3
    NOTIFIER = 4
    INITIATOR = 5


class Role(Base):

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
