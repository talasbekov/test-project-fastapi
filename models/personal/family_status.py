from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class FamilyStatus(Model, Base):

    __tablename__ = "family_statuses"

    name_kz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
