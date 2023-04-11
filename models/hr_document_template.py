import enum

from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from models import NamedModel


class SubjectType(enum.IntEnum):
    CANDIDATE = 1
    EMPLOYEE = 2
    PERSONNEL = 3
    STAFF = 4


class HrDocumentTemplate(NamedModel):

    __tablename__ = "hr_document_templates"

    path = Column(String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(JSON(none_as_null=True))
    description = Column(String(255))
    documents = relationship("HrDocument", cascade="all,delete", back_populates="document_template")
