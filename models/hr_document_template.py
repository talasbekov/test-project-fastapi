import enum

from sqlalchemy import Column, Enum, String, TEXT, UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from models import NamedModel, isActiveModel


class LanguageEnum(str, enum.Enum):
    ru = "ru"
    kz = "kz"


class SubjectType(enum.IntEnum):
    CANDIDATE = 1
    EMPLOYEE = 2
    PERSONNEL = 3
    STAFF = 4


class HrDocumentTemplate(NamedModel, isActiveModel):
    __tablename__ = "hr_document_templates"

    path = Column(String(255))
    pathKZ = Column(String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(JSON(none_as_null=True))
    description = Column(TEXT())
    actions = Column(JSON(none_as_null=True))
    maintainer_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"))

    documents = relationship(
        "HrDocument", cascade="all,delete", back_populates="document_template"
    )
    maintainer = relationship(
        'StaffUnit', foreign_keys=[maintainer_id]
    )
