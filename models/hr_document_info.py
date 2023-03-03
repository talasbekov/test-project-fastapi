import enum
import uuid

from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import Model


class HrDocumentInfo(Model, Base):
    
    __tablename__ = "hr_document_infos"

    hr_document_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"), nullable=False)

    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    signed_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    comment = Column(TEXT())

    is_signed = Column(Boolean())

    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    hr_document_id = Column(UUID(as_uuid=True), ForeignKey("hr_documents.id"), nullable=False)

    hr_document_step = relationship("HrDocumentStep", cascade="all,delete")
    signed_by = relationship("User", cascade="all, delete", foreign_keys=signed_by_id)
    assigned_to = relationship("User", cascade="all, delete", foreign_keys=assigned_to_id)
    hr_document = relationship("HrDocument", cascade="all,delete")
