import enum

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model
from .association import hr_document_equipments, hr_documents_users


class HrDocumentStatusEnum(str, enum.Enum):
    INITIALIZED = "Иницилизирован"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершен"
    CANCELED = "Отменен"
    ON_REVISION = "На доработке"


class HrDocument(Model, Base):

    __tablename__ = "hr_documents"

    hr_document_template_id = Column(
        UUID(as_uuid=True), ForeignKey("hr_document_templates.id"), nullable=True)
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    properties = Column(JSON(none_as_null=True))
    reg_number = Column(String, unique=True)
    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    status_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_statuses.id"))
    last_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"))

    document_template = relationship("HrDocumentTemplate", back_populates="documents")
    equipments = relationship("Equipment", secondary=hr_document_equipments,
                              back_populates="hr_documents")
    users = relationship(
        "User",
        secondary=hr_documents_users,
        back_populates="hr_documents"
    )
    last_step = relationship("HrDocumentStep")
    status = relationship("HrDocumentStatus", cascade="all, delete")
