import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.orm import relationship, backref

from core import Base


class RoleName(enum.Enum):
    AGREER = "Согласующий"
    EXPERT = "Эксперт"
    APPROVER = "Утверждающий"
    NOTIFIER = "Уведомляемый"
    INITIATOR = "Инициатор"


class Role(Base):

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
