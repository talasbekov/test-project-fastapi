import uuid

from sqlalchemy import TIMESTAMP, Column, String, text
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from models import Model


class Jurisdiction(Model, Base):

    __tablename__ = "jurisdictions"

    name_kz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
