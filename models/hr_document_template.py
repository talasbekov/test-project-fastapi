import enum
import json

from sqlalchemy import Column, Enum, String, ForeignKey, Boolean
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import NamedModel, isActiveModel
from .association import hr_document_equipments, hr_documents_users


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

class ActionType(str, enum.Enum):
    ADD_BADGE = "add_badge"
    DELETE_BADGE = "delete_badge"
    GRANT_LEAVE = "grant_leave"
    STOP_LEAVE = "stop_leave"
    RENEW_CONTRACT = "renew_contract"
    ADD_PENALTY = "add_penalty"
    DELETE_PENALTY = "delete_penalty"
    ADD_BLACK_BERET = "add_black_beret"
    DELETE_BLACK_BERET = "delete_black_beret"
    TEMPORARY_STATUS_CHANGE = "temporary_status_change"
    ADD_SECONDMENT = "add_secondment"
    POSITION_CHANGE = "position_change"
    INCREASE_RANK = "increase_rank"
    DECREASE_RANK = "decrease_rank"
    STATUS_CHANGE = "status_change"
    SICK_LEAVE = "sick_leave"
    APPLY_CANDIDATE = "apply_candidate"

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
    # last_step_id = Column(String(),
    #                       ForeignKey("hr_erp_hr_document_steps.id"))
    is_visible = Column(Boolean(), default=True)
    is_due_date_required = Column(Boolean(), default=False)
    is_initial_comment_required = Column(Boolean(), default=False)
    is_draft = Column(Boolean())
    # hr_erp_hr_documents_id = Column(String(), ForeignKey('hr_erp_hr_documents.id'))

    # Relationships
    documents = relationship(
        "HrDocument",
        cascade="all,delete",
        back_populates="document_template")
    maintainer = relationship("StaffUnit", foreign_keys=[maintainer_id])
    # last_step = relationship("HrDocumentStep", back_populates='hr_document_template', cascade='all,delete')
    # users = relationship(
    #     "User",
    #     secondary=hr_documents_users,
    #     back_populates="hr_documents")
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