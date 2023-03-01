import enum
import uuid

from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import TimeBaseModel


class HrDocumentInfo(TimeBaseModel, Base):
    
    __tablename__ = "hr_document_infos"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    hr_document_step_id = Column(UUID(as_uuid=True), ForeignKey("hr_document_steps.id"), nullable=False)
    signed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    comment = Column(TEXT())
    is_signed = Column(Boolean())
    signed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    hr_document_id = Column(UUID(as_uuid=True), ForeignKey("hr_documents.id"), nullable=False)
    
    signee = relationship("User", cascade="all, delete")
    hr_document_step = relationship("HrDocumentStep", cascade="all,delete")
    hr_document = relationship("HrDocument", cascade="all,delete")
