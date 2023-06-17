import enum

from sqlalchemy import Column, Enum, String, TEXT, UUID, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from models import NamedModel, isActiveModel


class HrDocumentTemplateEnum(str, enum.Enum):
    STAFF_LIST = "Приказ об изменении штатного расписания"
    DISPOSITION = "Приказ о выводе в распоряжение"
    STAFF_UNIT = "Приказ о назначении на должность (штатное расписание)"


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

    # Properties
    path = Column(String(255))
    pathKZ = Column(String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(JSON(none_as_null=True))
    description = Column(TEXT())
    actions = Column(JSON(none_as_null=True))
    maintainer_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"))
    is_visible = Column(Boolean(), default=True)
    is_due_date_required = Column(Boolean(), default=False)
    is_initial_comment_required = Column(Boolean(), default=False)

    # Relationships
    documents = relationship("HrDocument", cascade="all,delete", back_populates="document_template")
    maintainer = relationship("StaffUnit", foreign_keys=[maintainer_id])
    steps = relationship("HrDocumentStep", back_populates='steps', cascade='all,delete')
