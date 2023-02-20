import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class RoleName(str, enum.Enum):
    AGREER = "Утверждающий"
    EXPERT = "Эксперт"
    APPROVER = "Согласующий"
    NOTIFIER = "Увемдомляемый"
    INITIATOR = "Инициатор"


class Role(Base):

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    can_cancel = Column(Boolean(), nullable=False)
