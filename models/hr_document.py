import enum
import json

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, TEXT
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import Model
from .association import hr_document_equipments, hr_documents_users


class HrDocumentStatusEnum(str, enum.Enum):
    INITIALIZED = "Иницилизирован"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершен"
    CANCELED = "Отменен"
    ON_REVISION = "На доработке"
    DRAFT = "Черновик"


class HrDocument(Model):
    __tablename__ = "hr_erp_hr_documents"

    # Properties
    parent_id = Column(
        String(),
        ForeignKey("hr_erp_hr_documents.id"),
        nullable=True)

    hr_document_template_id = Column(
        String(),
        ForeignKey("hr_erp_hr_document_templates.id"),
        nullable=True)
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    properties = Column(CLOB)
    reg_number = Column(String, unique=True)
    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    initialized_by_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=True)
    initialized_at = Column(TIMESTAMP(timezone=True), nullable=True)
    initial_comment = Column(TEXT(), nullable=True)
    status_id = Column(String(),
                       ForeignKey("hr_erp_hr_document_statuses.id"))

    last_step_id = Column(String(),
                          ForeignKey("hr_erp_hr_document_steps.id"))
    old_history_id = Column(String(), ForeignKey("hr_erp_histories.id"))

    # Relationships
    children = relationship("HrDocument", cascade="all,delete")

    document_template = relationship(
        "HrDocumentTemplate",
        back_populates="documents",
        lazy="joined")
    equipments = relationship(
        "Equipment",
        secondary=hr_document_equipments,
        back_populates="hr_documents")
    users = relationship(
        "User",
        secondary=hr_documents_users,
        back_populates="hr_documents")
    last_step = relationship("HrDocumentStep")
    status = relationship("HrDocumentStatus")
    initialized_by = relationship("User")
    hr_document_infos = relationship(
        "HrDocumentInfo",
        back_populates="hr_document",
        cascade="all,delete")
    old_history = relationship("History", foreign_keys=[old_history_id])
    detailed_notifications = relationship("DetailedNotification", back_populates="hr_document", cascade="all,delete")

@listens_for(HrDocument, 'before_update')
def json_fields_update_listener(mapper, connection, target):
    if isinstance(target.properties, dict):
        target.properties = json.dumps(target.properties)

@listens_for(HrDocument, 'before_insert')
def json_fields_insert_listener(mapper, connection, target):
    if isinstance(target.properties, dict):
        target.properties = json.dumps(target.properties)