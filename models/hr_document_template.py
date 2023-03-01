import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import TimeBaseModel


class SubjectType(enum.IntEnum):
    CANDIDATE = 1
    EMPLOYEE = 2
    PERSONNEL = 3
    STAFF = 4


class HrDocumentTemplate(TimeBaseModel, Base):

    __tablename__ = "hr_document_templates"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255))
    path = Column(String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(JSON(none_as_null=True))

    documents = relationship("HrDocument", back_populates="document_template")
