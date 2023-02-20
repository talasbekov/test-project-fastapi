import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from core import Base

from .association import hr_document_equipments, hr_documents_users


class HrDocumentStatus(enum.IntEnum):
    INITIALIZED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELED = 4
    ON_REVISION = 5


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
    signed_at = Column(TIMESTAMP(timezone=True), nullable=False)

    document_template = relationship("HrDocumentTemplate", back_populates="documents", cascade="all,delete")
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
