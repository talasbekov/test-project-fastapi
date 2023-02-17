import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, text, ForeignKey, Enum, String
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from core import Base
from .association import hr_documents_users, hr_document_equipments


class HrDocumentStatus(str, enum.Enum):
    INITIALIZED = "Иницилизирован"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершен"
    CANCELED = "Отменен"
    ON_REVISION = "На доработке"


class HrDocument(Base):

    __tablename__ = "hr_documents"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    hr_document_template_id = Column(
        UUID(as_uuid=True), ForeignKey("hr_document_templates.id"), nullable=True)
    status = Column(Enum(HrDocumentStatus))
    due_date = Column(TIMESTAMP(timezone=True), nullable=False)
    properties = Column(JSON(none_as_null=True))
    reg_number = Column(String, unique=True)

    document_template = relationship("HrDocumentTemplate", back_populates="document", cascade="all,delete")
    equipments = relationship("HrDocument", secondary="hr_document_equipments",
                              back_populates="equipments")
    users = relationship(
        "User",
        secondary=hr_documents_users,
        back_populates="hr_documents",
        cascade="all,delete"
    )

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
