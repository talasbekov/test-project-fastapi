import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.orm import relationship

from core import Base


class SubjectType(enum.IntEnum):
    CANDIDATE = 1
    EMPLOYEE = 2
    PERSONNEL = 3
    STAFF = 4


class HrDocumentTemplate(Base):

    __tablename__ = "hr_document_templates"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(255))
    path = Column(String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(JSON(none_as_null=True))
    document = relationship("HrDocument", back_populates="document_template")

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
