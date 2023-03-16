from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class HrDocumentStatus(Model, Base):

    __tablename__ = "hr_document_statuses"

    name_kz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
