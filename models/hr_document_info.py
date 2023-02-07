import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
from sqlalchemy.orm import relationship, backref

from core import Base


class HrDocumentInfo(Base):
    
    __tablename__ = "hr_document_infos"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    hr_document_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"), nullable=False)
    signed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    comment = Column(TEXT())
    is_signed = Column(Boolean())

    signee = relationship("User", cascade="all, delete")
    hr_document_step = relationship("HrDocumentStep", cascade="all,delete")
