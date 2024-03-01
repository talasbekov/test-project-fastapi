import enum
import json

from sqlalchemy import Column, Enum, String, ForeignKey, Boolean
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

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
    __tablename__ = "hr_erp_hr_document_templates"

    # Properties
    path = Column(String(255))
    pathKZ = Column('pathkz', String(255))
    subject_type = Column(Enum(SubjectType))
    properties = Column(CLOB)
    description = Column(CLOB)
    actions = Column(CLOB)
    maintainer_id = Column(String(), ForeignKey("hr_erp_staff_units.id"))
    is_visible = Column(Boolean(), default=True)
    is_due_date_required = Column(Boolean(), default=False)
    is_initial_comment_required = Column(Boolean(), default=False)
    is_draft = Column(Boolean())

    # Relationships
    documents = relationship(
        "HrDocument",
        cascade="all,delete",
        back_populates="document_template")
    maintainer = relationship("StaffUnit", foreign_keys=[maintainer_id])
    steps = relationship("HrDocumentStep",
                         back_populates='hr_document_template',
                         cascade='all,delete')

@listens_for(HrDocumentTemplate, 'before_update')
def json_fields_update_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)
    if isinstance(target.properties, dict):
        target.properties = json.dumps(target.properties)
    if isinstance(target.actions, dict):
        target.actions = json.dumps(target.actions)

@listens_for(HrDocumentTemplate, 'before_insert')
def json_fields_insert_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)
    if isinstance(target.properties, dict):
        target.properties = json.dumps(target.properties)
    if isinstance(target.actions, dict):
        target.actions = json.dumps(target.actions)